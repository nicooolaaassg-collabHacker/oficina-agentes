#!/usr/bin/env python3
"""Servidor local de "La oficina de Claude".

Sirve la página en http://localhost:4545 y le manda en directo (Server-Sent
Events) lo que el hook va escribiendo en ~/.claude/oficina/events.jsonl.

Uso:  python3 scripts/server.py [puerto]   (o /oficina desde Claude Code)
"""
import http.server
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = Path.home() / ".claude" / "oficina" / "events.jsonl"
CONFIG = Path.home() / ".claude" / "oficina" / "config.json"


def config():
    try:
        return json.loads(CONFIG.read_text())
    except (OSError, ValueError):
        return {}


PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("OFICINA_PORT") or config().get("port") or 4545)
# macOS solo deja usar puertos por debajo de 1024 sin permisos escuchando en todas las redes;
# en ese caso se sigue atendiendo únicamente a este ordenador (ver allowed)
BIND = "0.0.0.0" if PORT < 1024 else "127.0.0.1"
HOSTS = {"localhost", "127.0.0.1", str(os.environ.get("OFICINA_HOST") or config().get("host") or "").lower()}
REPLAY = 400
# La meta "oficina-live" le dice a la página que está servida por este servidor (modo en directo)
HEAD = b'<!doctype html>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="oficina-live" content="1">\n'


def size():
    try:
        return LOG.stat().st_size
    except OSError:
        return 0


def last_lines(n):
    """Las últimas n líneas completas del registro y el byte donde acaba."""
    end = size()
    if not end:
        return [], 0
    with open(LOG, "rb") as f:
        f.seek(max(0, end - 400_000))
        data = f.read(end - f.tell())
    cut = data.rfind(b"\n") + 1
    return [l for l in data[:cut].splitlines() if l.strip()][-n:], end - (len(data) - cut)


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def allowed(self):
        # Solo este ordenador, y solo con un nombre conocido (evita que una web ajena lea la oficina)
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0].strip("[]").lower()
        local = self.client_address[0] in ("127.0.0.1", "::1")
        return local and (host in HOSTS or host.endswith(".localhost"))

    def do_GET(self):
        if not self.allowed():
            self.send_error(403)
            return
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            body = HEAD + (ROOT / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/events":
            self.stream()
        else:
            self.send_error(404)

    def send(self, chunk):
        self.wfile.write(chunk)
        self.wfile.flush()

    def stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        last = self.headers.get("Last-Event-ID", "")
        try:
            if last.isdigit():
                pos = int(last)
            else:
                # Al conectar: el historial reciente, sin animar, y luego lo nuevo en directo
                lines, pos = last_lines(REPLAY)
                self.send(b"".join(b"event: replay\ndata: " + l + b"\n\n" for l in lines))
            self.send(b"event: ready\nid: %d\ndata: {}\n\n" % pos)
            ping = time.time()
            while True:
                end = size()
                if end < pos:  # el hook recortó el archivo: seguimos desde el final
                    pos = end
                if end > pos:
                    with open(LOG, "rb") as f:
                        f.seek(pos)
                        data = f.read(end - pos)
                    cut = data.rfind(b"\n") + 1
                    if cut:
                        pos += cut
                        lines = [l for l in data[:cut].splitlines() if l.strip()]
                        out = [b"data: " + l + b"\n\n" for l in lines[:-1]]
                        if lines:
                            out.append(b"id: %d\ndata: " % pos + lines[-1] + b"\n\n")
                        self.send(b"".join(out))
                        ping = time.time()
                if time.time() - ping > 15:
                    self.send(b": ping\n\n")
                    ping = time.time()
                time.sleep(0.15)
        except (BrokenPipeError, ConnectionResetError):
            pass


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer((BIND, PORT), Handler)
    server.daemon_threads = True
    print(f"La oficina de Claude: http://localhost:{PORT}  (Ctrl+C para parar)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

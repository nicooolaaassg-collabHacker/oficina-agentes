#!/usr/bin/env python3
"""Arranca el servidor de La oficina de Claude en segundo plano (si no está ya
en marcha) y abre la página en el navegador.

Uso:  python3 scripts/start.py [--no-open]

La dirección se cambia en ~/.claude/oficina/config.json, por ejemplo
{"host": "mioficina", "port": 80}, o con OFICINA_HOST y OFICINA_PORT.
"""
import json
import os
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

DIR = Path.home() / ".claude" / "oficina"
LOG = DIR / "server.log"
try:
    CFG = json.loads((DIR / "config.json").read_text())
except (OSError, ValueError):
    CFG = {}
HOST = os.environ.get("OFICINA_HOST") or CFG.get("host") or "oficina.localhost"
PORT = int(os.environ.get("OFICINA_PORT") or CFG.get("port") or 4545)
URL = f"http://{HOST}" + ("" if PORT == 80 else f":{PORT}")


def running():
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


if not running():
    LOG.parent.mkdir(parents=True, exist_ok=True)
    subprocess.Popen(
        [sys.executable, str(Path(__file__).with_name("server.py")), str(PORT)],
        stdin=subprocess.DEVNULL,
        stdout=open(LOG, "a"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for _ in range(30):
        if running():
            break
        time.sleep(0.1)

if running():
    print(f"La oficina de Claude está en {URL}")
    if HOST != "localhost":
        print(f"Si no abre, prueba http://localhost:{PORT}")
    if "--no-open" not in sys.argv:
        webbrowser.open(URL)
else:
    print(f"No se pudo arrancar el servidor en el puerto {PORT}. Mira {LOG}")
    sys.exit(1)

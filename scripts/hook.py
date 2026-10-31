#!/usr/bin/env python3
"""Hook de Claude Code para "La oficina de Claude".

Lee el evento que Claude Code manda por stdin y añade una línea resumida a
~/.claude/oficina/events.jsonl. El servidor de la oficina lee ese archivo y lo
envía a la página. No imprime nada y nunca falla, para no molestar a la sesión.
"""
import json
import os
import sys
import time

DIR = os.path.join(os.path.expanduser("~"), ".claude", "oficina")
LOG = os.path.join(DIR, "events.jsonl")
KEYS = os.path.join(DIR, "keys.json")
ROOT_FILE = os.path.join(DIR, "root.txt")
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_BYTES = 3_000_000


def cut(s, n):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def lines(s, n=6, w=70):
    out = []
    for ln in str(s or "").splitlines():
        if ln.strip():
            out.append(ln.rstrip()[:w])
        if len(out) >= n:
            break
    return out


def plan_of(ti):
    p = {}
    for key in ("todos", "items"):
        if isinstance(ti.get(key), list):
            p["items"] = [
                {"content": cut(t.get("content") or t.get("subject") or t.get("activeForm"), 80), "status": t.get("status", "pending")}
                for t in ti[key] if isinstance(t, dict)
            ][:12]
    for key in ("advance", "done", "start"):
        if key in ti:
            p[key] = ti[key]
    return p


def summarize(d):
    ev = d.get("hook_event_name", "")
    e = {
        "ts": round(time.time(), 3),
        "ev": ev,
        "sid": str(d.get("session_id", ""))[:8],
        "proj": os.path.basename(str(d.get("cwd", "")).rstrip("/")) or "",
    }
    if d.get("agent_id"):
        e["agent"] = str(d["agent_id"])[:16]
    if d.get("agent_type"):
        e["atype"] = cut(d["agent_type"], 30)

    tool = d.get("tool_name")
    if tool:
        e["tool"] = tool
        e["tid"] = str(d.get("tool_use_id", ""))[-10:]
        ti = d.get("tool_input") if isinstance(d.get("tool_input"), dict) else {}
        path = ti.get("file_path") or ti.get("notebook_path") or ti.get("path")
        if path:
            e["file"] = os.path.basename(str(path).rstrip("/")) or str(path)
        if tool in ("Bash", "PowerShell"):
            e["cmd"] = cut(ti.get("command"), 90)
            e["desc"] = cut(ti.get("description"), 70)
        elif tool in ("Grep", "Glob"):
            e["pat"] = cut(ti.get("pattern"), 50)
        elif tool == "WebFetch":
            e["url"] = cut(str(ti.get("url", "")).split("//")[-1].split("/")[0], 50)
        elif tool == "WebSearch":
            e["q"] = cut(ti.get("query"), 70)
        elif tool in ("Agent", "Task"):
            e["desc"] = cut(ti.get("description"), 70)
            e["atype"] = cut(ti.get("subagent_type") or "general-purpose", 30)
        elif tool == "Skill":
            e["desc"] = cut(ti.get("skill"), 50)
        if ev == "PreToolUse":
            if tool == "Edit":
                e["snip"] = lines(ti.get("new_string"))
            elif tool == "Write":
                e["snip"] = lines(ti.get("content"))
            elif tool == "MultiEdit" and isinstance(ti.get("edits"), list) and ti["edits"]:
                e["snip"] = lines(ti["edits"][0].get("new_string"))
            p = plan_of(ti)
            if p:
                e["plan"] = p
        resp = d.get("tool_response")
        if ev == "PostToolUseFailure" or (isinstance(resp, dict) and (resp.get("is_error") or resp.get("interrupted"))):
            e["err"] = True

    if ev == "UserPromptSubmit":
        e["prompt"] = cut(d.get("prompt"), 140)
    elif ev == "Notification":
        e["msg"] = cut(d.get("message"), 120)
    elif ev in ("SessionStart", "SessionEnd"):
        e["why"] = cut(d.get("source") or d.get("reason"), 20)
    return e


def remember_keys(d):
    # Ayuda a depurar: qué campos trae cada tipo de evento (sin sus valores)
    try:
        with open(KEYS) as f:
            known = json.load(f)
    except Exception:
        known = {}
    ev = d.get("hook_event_name", "?")
    keys = sorted(set(known.get(ev, [])) | set(d.keys()))
    if keys != known.get(ev):
        known[ev] = keys
        with open(KEYS, "w") as f:
            json.dump(known, f, indent=1)


def main():
    d = json.load(sys.stdin)
    os.makedirs(DIR, exist_ok=True)
    remember_keys(d)
    # Para que /oficina encuentre el plugin aunque no conozca su carpeta
    try:
        with open(ROOT_FILE) as f:
            known_root = f.read().strip()
    except OSError:
        known_root = ""
    if known_root != PLUGIN_ROOT:
        with open(ROOT_FILE, "w") as f:
            f.write(PLUGIN_ROOT)
    with open(LOG, "a") as f:
        f.write(json.dumps(summarize(d), ensure_ascii=False) + "\n")
    if os.path.getsize(LOG) > MAX_BYTES:
        with open(LOG, "rb") as f:
            f.seek(-MAX_BYTES // 3, 2)
            tail = f.read()
        with open(LOG, "wb") as f:
            f.write(tail[tail.find(b"\n") + 1:])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)

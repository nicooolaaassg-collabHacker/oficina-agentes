---
description: Abre La oficina de Claude para ver en directo a Claude y sus agentes trabajando
allowed-tools: Bash
---

Abre La oficina de Claude. Ejecuta exactamente este comando con la herramienta Bash, sin cambiarlo:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-$(cat ~/.claude/oficina/root.txt)}/scripts/start.py"
```

Después responde con una sola frase: el enlace que imprime (normalmente http://oficina.localhost:4545) y que ahí se ve en directo lo que hacen sus sesiones de Claude Code y sus agentes. No hagas nada más.

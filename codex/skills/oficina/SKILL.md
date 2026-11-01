---
name: oficina
description: Abre La oficina de agentes, una página local donde se ve en directo lo que hacen Codex, Claude Code y sus agentes. Úsala cuando el usuario pida abrir o ver la oficina.
---

Ejecuta exactamente este comando, sin cambiarlo:

```bash
python3 "$(cat ~/.claude/oficina/root.txt)/scripts/start.py"
```

Arranca un servidor local en segundo plano, así que necesita permiso para salir del sandbox: si el sandbox lo bloquea, pide permiso para ejecutarlo fuera.

Después responde con una sola frase: el enlace que imprime (normalmente http://oficina.localhost:4545) y que ahí se ve en directo lo que hacen sus sesiones y sus agentes. No hagas nada más.

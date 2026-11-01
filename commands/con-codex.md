---
description: Reparte una tarea entre Claude y Codex; los dos trabajan a la vez y se ven en La oficina
argument-hint: <la tarea que queréis hacer entre los dos>
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

Haz esta tarea junto con Codex (el agente de OpenAI que el usuario tiene instalado en este ordenador):

$ARGUMENTS

Tú diriges. Sigue estos pasos:

1. **Comprueba que Codex está instalado** con `command -v codex || ls ~/.local/bin/codex`. Si no aparece, no sigas: dile al usuario que instale Codex e inicie sesión, y que para verlo en la oficina instale también el plugin `oficina-agentes` en Codex (lo explica el README del plugin).

2. **Reparte el trabajo.** Elige para Codex una parte que pueda hacer solo, sin esperar a la tuya: por ejemplo los tests, una investigación, una revisión o un archivo concreto. Que cada uno toque archivos distintos, para no pisaros. Si la tarea es tan pequeña que no se puede repartir, díselo al usuario y hazla tú.

3. **Dale el encargo a Codex en segundo plano** (Bash con `run_in_background: true`), desde la carpeta del proyecto:

   ```bash
   codex exec -C "<carpeta del proyecto>" --skip-git-repo-check -s workspace-write "<encargo>"
   ```

   - Si `codex` no está en el PATH, usa `~/.local/bin/codex`.
   - Si el encargo necesita buscar en internet, pon `--search` antes de `exec`: `codex --search exec …`.
   - El encargo tiene que ser completo y en español: qué hacer, qué archivos puede crear o cambiar, cuáles no debe tocar, dónde dejar el resultado y que responda con una frase al terminar.
   - Nunca uses `--dangerously-bypass-approvals-and-sandbox` ni ninguna opción para saltarse la aprobación de hooks.

4. **Haz tu parte mientras tanto.** Codex aparece en La oficina como un muñeco turquesa con antena, al lado del tuyo, si tiene el plugin instalado y sus hooks aprobados. No esperes a Codex mirando su salida en bucle: cuando termine, te llegará el aviso.

5. **Junta el trabajo.** Lee lo que ha hecho Codex, compruébalo (ejecuta sus tests, revisa sus archivos o sus fuentes) y corrige lo que haga falta.

6. **Cuéntale al usuario** en pocas frases qué hizo cada uno, qué comprobaste y dónde está el resultado. Si Codex falló o se quedó sin cuota, dilo y explica qué hiciste tú en su lugar.

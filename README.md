# La oficina de Claude

Mira en directo a Claude Code, a Codex y a sus agentes trabajando dentro de un ordenador pixel art.

> Proyecto de la comunidad, no oficial. No está hecho ni respaldado por Anthropic.

Cada sesión de Claude Code es un muñeco naranja y cada sesión de Codex, uno turquesa con antena. Cuando lanzan un agente, aparece otro muñeco más pequeño a su lado. Lo que hacen de verdad se ve en la pantalla:

- un comando o una búsqueda se escribe en una terminal,
- leer un archivo es ir a por su icono y cogerlo,
- editar o crear un archivo abre un editor con el principio del código,
- mirar la web abre un navegador,
- cuando un agente termina, vuelve con quien lo lanzó, le entrega el trabajo y se va,
- al acabar el turno, cierra las ventanas, celebra y espera tu mensaje.

A la derecha tienes tu último mensaje, el plan (cuando hay uno), qué está haciendo cada agente y un registro con cada herramienta que usan.

## Instalación

Necesitas Claude Code y Python 3 (viene con macOS; en Linux suele estar instalado).

En una sesión de Claude Code en la terminal:

```
/plugin install oficina-agentes --marketplace nicooolaaassg-collabHacker/oficina-agentes
```

Responde `y` para añadir el marketplace y elige el ámbito de usuario (el primero) con Enter.

Desde una terminal normal:

```bash
claude plugin install oficina-agentes --marketplace nicooolaaassg-collabHacker/oficina-agentes
```

En la app de escritorio, donde `/plugin` no funciona: pulsa **+** junto a la caja de texto, luego **Plugins**, **Add marketplace** con `nicooolaaassg-collabHacker/oficina-agentes`, y después **Add plugin**.

### En Codex

Necesitas Codex (la app de terminal de OpenAI) y Python 3. En una terminal normal:

```bash
codex plugin marketplace add nicooolaaassg-collabHacker/oficina-agentes
```

```bash
codex plugin add oficina-agentes@oficina-agentes
```

Codex no deja que un plugin haga nada hasta que apruebas sus hooks. Abre `codex`, escribe `/hooks` y pulsa `t` (aprobar todos); los contadores pasan a `1/1`. Tendrás que volver a hacerlo cada vez que actualices el plugin, porque Codex pide aprobar los hooks de nuevo cuando cambian.

Si usas los dos, Claude Code y Codex aparecen juntos en la misma oficina.

## Uso

Escribe en Claude Code:

```
/oficina
```

En Codex, pídeselo: «abre la oficina» (usa la skill `oficina` del plugin).

Se abre `http://oficina.localhost:4545` en tu navegador (si no carga, usa `http://localhost:4545`). Esa dirección solo existe en tu ordenador mientras la oficina está en marcha. Déjala abierta y sigue trabajando con Claude Code como siempre: cualquier sesión que abras, de Claude Code o de Codex, aparecerá en la oficina.

### Claude y Codex trabajando juntos

Si tienes los dos instalados, Claude puede repartir una tarea con Codex:

```
/con-codex haz una calculadora en Python; tú el código y Codex los tests
```

Claude elige una parte que Codex pueda hacer solo (tests, una investigación, una revisión…), se la encarga, hace la suya mientras tanto y al final junta y comprueba el trabajo de los dos. En la oficina ves al naranja y al turquesa trabajando a la vez. Gasta de los dos planes: el de Claude y el de ChatGPT.

Si prefieres arrancarla a mano, desde la carpeta del plugin:

```bash
python3 scripts/start.py
```

### Cambiar la dirección

Crea `~/.claude/oficina/config.json` con el nombre y el puerto que quieras:

```json
{ "host": "mioficina", "port": 80 }
```

Con el puerto 80 la dirección queda sin número: `http://mioficina`. Un nombre que no acabe en `.localhost` hay que dárselo de alta una vez en tu ordenador (pide la contraseña de administrador):

```bash
sudo sh -c 'echo "127.0.0.1 mioficina" >> /etc/hosts'
```

Escríbelo siempre con `http://` delante, o el navegador lo buscará en internet. En Linux, el puerto 80 necesita permisos de administrador; usa otro, como 8080.

## Privacidad

Todo se queda en tu ordenador:

- Los hooks del plugin apuntan un resumen de cada acción en `~/.claude/oficina/events.jsonl`: el nombre de la herramienta, el comando, el nombre del archivo, las primeras líneas de lo que se escribe y tu mensaje recortado. El archivo se recorta solo cuando pasa de 3 MB.
- El servidor solo atiende a tu propio ordenador: rechaza las peticiones que llegan de otros equipos o con un nombre que no conoce, así que nadie de fuera puede abrir la página.
- No se envía nada a internet. La página solo descarga las tipografías de Google Fonts.

Para borrar todo lo apuntado: `rm -rf ~/.claude/oficina`.

## Desinstalar

```
/plugin uninstall oficina-agentes
```

En Codex:

```bash
codex plugin remove oficina-agentes@oficina-agentes
```

Si tenías la oficina abierta, cierra el servidor con `pkill -f "oficina.*server.py"` o reinicia el ordenador.

## Cómo funciona

| Archivo | Qué hace |
|---|---|
| `hooks/hooks.json` | Engancha `scripts/hook.py` a los eventos de Claude Code y de Codex (herramientas, agentes, mensajes, fin de turno) |
| `scripts/hook.py` | Resume cada evento en una línea de `~/.claude/oficina/events.jsonl` y traduce las herramientas de Codex a las de Claude |
| `scripts/server.py` | Sirve la página y le envía los eventos nuevos en directo (Server-Sent Events) |
| `scripts/start.py` | Arranca el servidor en segundo plano si no está en marcha y abre el navegador |
| `commands/oficina.md` | El comando `/oficina` |
| `commands/con-codex.md` | El comando `/con-codex`, para repartir una tarea con Codex |
| `codex/skills/oficina/SKILL.md` | La skill para abrir la oficina desde Codex |
| `.codex-plugin/plugin.json` | Lo que necesita Codex para instalar el plugin |
| `index.html` | La oficina. Si la abres sin servidor, enseña una simulación con tareas de ejemplo |

Los hooks van en segundo plano (`async`), así que no ralentizan tus sesiones.

## English

**Claude's Office** is an unofficial community Claude Code plugin (not made or endorsed by Anthropic) that shows your Claude Code and Codex sessions and their subagents working live, as pixel-art characters moving around a desktop. Install it with `/plugin install oficina-agentes --marketplace nicooolaaassg-collabHacker/oficina-agentes`, (in Codex: `codex plugin marketplace add nicooolaaassg-collabHacker/oficina-agentes`, `codex plugin add oficina-agentes@oficina-agentes`, then approve its hooks with `/hooks` and `t`), then type `/oficina` (or ask Codex to "abre la oficina") to open `http://oficina.localhost:4545` on your own machine (address configurable in `~/.claude/oficina/config.json`). With both installed, `/con-codex <task>` lets Claude hand part of a task to Codex and work alongside it. Everything stays on your machine: events are logged to `~/.claude/oficina/events.jsonl` and the server only answers requests from your own computer. The interface is in Spanish.

## Licencia

MIT

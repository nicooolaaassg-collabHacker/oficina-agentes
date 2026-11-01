# La oficina de Claude

Mira en directo a Claude Code y a sus agentes trabajando dentro de un ordenador pixel art.

> Proyecto de la comunidad, no oficial. No está hecho ni respaldado por Anthropic.

Cada sesión de Claude Code es un muñeco naranja. Cuando Claude lanza un agente, aparece otro muñeco más pequeño a su lado. Lo que hacen de verdad se ve en la pantalla:

- un comando o una búsqueda se escribe en una terminal,
- leer un archivo es ir a por su icono y cogerlo,
- editar o crear un archivo abre un editor con el principio del código,
- mirar la web abre un navegador,
- cuando un agente termina, vuelve con Claude, le entrega el trabajo y se va,
- al acabar el turno, Claude cierra las ventanas, celebra y espera tu mensaje.

A la derecha tienes tu último mensaje, el plan (cuando Claude hace uno), qué está haciendo cada agente y un registro con cada herramienta que usan.

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

## Uso

Escribe en Claude Code:

```
/oficina
```

Se abre http://oficina.localhost:4545 en tu navegador (si no carga, usa http://localhost:4545). Déjala abierta y sigue trabajando con Claude Code como siempre: cualquier sesión que abras aparecerá en la oficina.

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
- El servidor solo escucha en `127.0.0.1`, así que nadie de fuera puede abrir la página.
- No se envía nada a internet. La página solo descarga las tipografías de Google Fonts.

Para borrar todo lo apuntado: `rm -rf ~/.claude/oficina`.

## Desinstalar

```
/plugin uninstall oficina-agentes
```

Si tenías la oficina abierta, cierra el servidor con `pkill -f "oficina.*server.py"` o reinicia el ordenador.

## Cómo funciona

| Archivo | Qué hace |
|---|---|
| `hooks/hooks.json` | Engancha `scripts/hook.py` a los eventos de Claude Code (herramientas, agentes, mensajes, fin de turno) |
| `scripts/hook.py` | Resume cada evento en una línea de `~/.claude/oficina/events.jsonl` |
| `scripts/server.py` | Sirve la página y le envía los eventos nuevos en directo (Server-Sent Events) |
| `scripts/start.py` | Arranca el servidor en segundo plano si no está en marcha y abre el navegador |
| `commands/oficina.md` | El comando `/oficina` |
| `index.html` | La oficina. Si la abres sin servidor, enseña una simulación con tareas de ejemplo |

Los hooks van en segundo plano (`async`), así que no ralentizan tus sesiones.

## English

**Claude's Office** is an unofficial community Claude Code plugin (not made or endorsed by Anthropic) that shows your Claude Code sessions and their subagents working live, as pixel-art characters moving around a desktop. Install it with `/plugin install oficina-agentes --marketplace nicooolaaassg-collabHacker/oficina-agentes`, then type `/oficina` to open http://oficina.localhost:4545 (address configurable in `~/.claude/oficina/config.json`). Everything stays on your machine: events are logged to `~/.claude/oficina/events.jsonl` and the server only listens on `127.0.0.1`. The interface is in Spanish.

## Licencia

MIT

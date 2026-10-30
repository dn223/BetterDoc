# BetterDoc

Una skill para agentes de IA (Claude Code, Codex CLI y otros) que crea documentos **solo con lo que pides**.

- **Primero pregunta.** Antes de escribir, el agente se detiene y te pregunta qué estructura quieres, qué tan extenso, si debe seguir normas APA, si lleva portada y en qué formato.
- **Sin relleno.** No agrega secciones que no pediste, ni colores, ni emojis, ni frases de relleno.
- **Sin inventar.** Si falta un dato (un nombre, una fecha, una referencia), lo deja como `[dato]` y te avisa.
- **PDF listo.** Genera el PDF con un estilo plano en blanco y negro o con formato APA 7.

## Instalación

Necesitas `git`. Para generar PDF también necesitas Python 3 y Google Chrome o Microsoft Edge.

### Windows

```powershell
git clone https://github.com/dn223/BetterDoc
cd BetterDoc
powershell -ExecutionPolicy Bypass -File install.ps1
```

### macOS / Linux

```sh
git clone https://github.com/dn223/BetterDoc
cd BetterDoc
sh install.sh
```

El instalador copia la skill a las carpetas que encuentre:

| Agente | Carpeta |
|---|---|
| Claude Code | `~/.claude/skills/betterdoc` |
| Codex CLI | `~/.codex/skills/betterdoc` |

¿Usas otro agente que lee skills desde otra carpeta? Pásala como argumento: `install.ps1 -Destino <carpeta>` o `sh install.sh <carpeta>`.

### Opción fácil: que tu agente lo instale

Pégale esto a tu agente:

> Instala la skill de https://github.com/dn223/BetterDoc siguiendo su README.

### Agentes sin soporte de skills

Copia el contenido de [`AGENTS.md`](AGENTS.md) en el archivo de instrucciones de tu agente (`AGENTS.md`, `GEMINI.md`, reglas del proyecto, etc.) y deja la carpeta del repo a su alcance.

## Uso

Reinicia el agente y pídele un documento con naturalidad:

> Hazme el manual de usuario de este proyecto.

> Necesito un informe en APA sobre energía solar, unas 8 páginas.

El agente te hará preguntas por rondas, como estas:

1. ¿Qué tipo de documento es y para quién?
2. ¿Estructura plana y directa, académica o según una rúbrica?
3. ¿Qué tan extenso?
4. ¿Normas APA 7 obligatorias?
5. ¿Lleva portada? ¿Con qué datos?
6. ¿PDF, Word o Markdown?

Después te muestra un resumen y espera tu "sí" antes de escribir. Si no quieres preguntas, di **"rápido"** o **"usa lo de siempre"** y usará los valores por defecto (estructura plana, 6 a 12 páginas, sin normas, PDF en blanco y negro).

## Generar un PDF a mano

```sh
python scripts/generar_pdf.py documento.md --portada templates/portada.json --tipo "Manual de usuario"
python scripts/generar_pdf.py ensayo.md --estilo apa7 --portada portada.json
```

| Opción | Qué hace |
|---|---|
| `--estilo plano` | Blanco y negro, Arial, títulos en negrita (por defecto). |
| `--estilo apa7` | Times New Roman 12, doble espacio, márgenes de 2.54 cm, número de página arriba a la derecha y sangría francesa en Referencias. |
| `--portada archivo.json` | Agrega portada. Copia `templates/portada.json` y llénalo. |
| `--final` | No genera el PDF si quedan datos `[por completar]`. |

## Qué contiene

```
SKILL.md                 Instrucciones de la skill
references/preguntas.md  Cuestionario y valores por defecto
references/apa7.md       Reglas de APA 7 para estudiantes
templates/               Estilos (plano, apa7) y portada de ejemplo
scripts/generar_pdf.py   Conversor de Markdown a PDF
install.ps1, install.sh  Instaladores
AGENTS.md                Versión para agentes sin skills
```

## Licencia

MIT. Úsala, compártela y modifícala libremente.

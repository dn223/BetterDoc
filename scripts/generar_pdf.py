"""Convierte un documento Markdown a PDF con Chrome o Edge (modo headless).

Ejemplos:
    python generar_pdf.py manual.md
    python generar_pdf.py manual.md --salida Manual.pdf --portada portada.json --tipo "Manual de usuario"
    python generar_pdf.py ensayo.md --estilo apa7 --portada portada.json --final

Requisitos: Python 3.9+, `pip install markdown`, y Google Chrome o Microsoft Edge.
Los bloques ```mermaid se dibujan con mermaid.js (requiere internet al generar).
"""

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Falta el paquete 'markdown'. Instálalo con: pip install markdown")

PLANTILLAS = Path(__file__).resolve().parent.parent / "templates"
MERMAID_JS = "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"
TITULOS_AVISO = {"NOTA": "Nota", "IMPORTANTE": "Importante", "PENDIENTE": "Pendiente"}
NAVEGADORES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
# Texto entre corchetes que no es un enlace ni una casilla: [Nombre del docente]
PENDIENTE = re.compile(r"\[(?!\s?\]|x\])[^\]\n]{2,80}\](?!\()")


def buscar_navegador():
    for ruta in NAVEGADORES:
        if Path(ruta).exists():
            return ruta
    for nombre in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge", "microsoft-edge"):
        encontrado = shutil.which(nombre)
        if encontrado:
            return encontrado
    sys.exit("No se encontró Google Chrome, Chromium ni Microsoft Edge para imprimir el PDF.")


def sin_codigo(texto):
    return re.sub(r"```.*?```|`[^`\n]*`", "", texto, flags=re.S)


def textos(valor):
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for v in valor.values():
            yield from textos(v)
    elif isinstance(valor, list):
        for v in valor:
            yield from textos(v)


def buscar_pendientes(texto, portada):
    encontrados = PENDIENTE.findall(sin_codigo(texto))
    for valor in textos(portada or {}):
        encontrados += PENDIENTE.findall(valor)
    return sorted(set(encontrados))


def preprocesar(texto):
    """Convierte bloques Mermaid y avisos `> [!TIPO]` a HTML antes de Markdown."""
    texto = re.sub(
        r"```mermaid\n(.*?)```",
        lambda m: '<pre class="mermaid">\n' + html.escape(m.group(1)) + "</pre>",
        texto,
        flags=re.S,
    )

    def aviso(m):
        tipo = m.group(1).upper()
        cuerpo = re.sub(r"^> ?", "", m.group(2), flags=re.M)
        return (
            f'<div class="aviso {tipo.lower()}" markdown="1">\n'
            f'<div class="aviso-titulo">{TITULOS_AVISO.get(tipo, tipo.title())}</div>\n\n'
            f"{cuerpo}\n</div>\n"
        )

    return re.sub(r"^> \[!(\w+)\]\n((?:>.*\n?)*)", aviso, texto, flags=re.M)


def fila(etiqueta, valor):
    return f"<tr><td>{etiqueta}</td><td>{html.escape(str(valor))}</td></tr>" if valor else ""


def portada_plana(d, tipo, subtitulo):
    filas = "".join(
        fila(etiqueta, d.get(clave))
        for clave, etiqueta in [
            ("carrera", "Carrera"),
            ("asignatura", "Asignatura"),
            ("grupo", "Grupo"),
            ("docente", "Docente"),
            ("periodo", "Período"),
        ]
    )
    integrantes = ""
    if d.get("integrantes"):
        con_carnet = any(i.get("carnet") for i in d["integrantes"])
        encabezado = "<tr><th>Integrante</th>" + ("<th>Carné</th>" if con_carnet else "") + "</tr>"
        cuerpo = "".join(
            f"<tr><td>{html.escape(i['nombre'])}</td>"
            + (f"<td>{html.escape(i.get('carnet', ''))}</td>" if con_carnet else "")
            + "</tr>"
            for i in d["integrantes"]
        )
        integrantes = f'<div class="integrantes-titulo">Integrantes</div><table class="integrantes">{encabezado}{cuerpo}</table>'
    pie = ", ".join(html.escape(d[k]) for k in ("lugar", "fecha") if d.get(k))
    return f"""
<section class="portada">
  <div class="institucion">{html.escape(d.get('institucion', ''))}</div>
  <div class="facultad">{html.escape(d.get('facultad', ''))}</div>
  <div class="tipo">{html.escape(tipo)}</div>
  <h1 class="titulo">{html.escape(d.get('titulo', ''))}</h1>
  <div class="subtitulo">{html.escape(subtitulo)}</div>
  <table class="datos">{filas}</table>
  {integrantes}
  <div class="pie">{pie}</div>
</section>"""


def portada_apa(d):
    autores = "<br>".join(html.escape(i["nombre"]) for i in d.get("integrantes", []))
    afiliacion = ", ".join(html.escape(d[k]) for k in ("facultad", "institucion") if d.get(k))
    lineas = [
        f'<div class="titulo">{html.escape(d.get("titulo", ""))}</div>',
        '<div class="blanco"></div>',
        f"<div>{autores}</div>",
        f"<div>{afiliacion}</div>",
        f"<div>{html.escape(d.get('asignatura', ''))}</div>",
        f"<div>{html.escape(d.get('docente', ''))}</div>",
        f"<div>{html.escape(d.get('fecha', ''))}</div>",
    ]
    return '<section class="portada">' + "".join(lineas) + "</section>"


def construir_html(texto, args, portada):
    usar_indice = args.indice if args.indice is not None else args.estilo == "plano"
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "attr_list", "md_in_html", "sane_lists"],
        extension_configs={"toc": {"toc_depth": "1-2", "permalink": False}},
    )
    cuerpo = md.convert(preprocesar(texto))
    titulo = (portada or {}).get("titulo") or args.entrada.stem
    pie = " — ".join(x for x in (titulo, args.tipo) if x).replace('"', "'")
    css = (PLANTILLAS / f"{args.estilo}.css").read_text(encoding="utf-8").replace("__PIE__", pie)
    if portada:
        bloque_portada = portada_apa(portada) if args.estilo == "apa7" else portada_plana(portada, args.tipo, args.subtitulo)
    else:
        bloque_portada = ""
    indice = f'<section class="indice"><h2>Contenido</h2><div class="toc">{md.toc}</div></section>' if usar_indice else ""
    mermaid = (
        f'<script src="{MERMAID_JS}"></script>'
        '<script>if (window.mermaid) mermaid.initialize({startOnLoad: true, theme: "neutral"});</script>'
        if 'class="mermaid"' in cuerpo
        else ""
    )
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title>
<style>{css}</style></head>
<body>
{bloque_portada}
{indice}
<main>{cuerpo}</main>
{mermaid}
</body></html>"""


def imprimir(navegador, html_path, pdf_path):
    subprocess.run(
        [
            navegador, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=20000",
            f"--print-to-pdf={pdf_path}", html_path.as_uri(),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("entrada", type=Path, help="archivo Markdown")
    parser.add_argument("--salida", type=Path, help="PDF de salida (por defecto, mismo nombre que la entrada)")
    parser.add_argument("--estilo", choices=["plano", "apa7"], default="plano")
    parser.add_argument("--portada", type=Path, help="JSON con los datos de portada")
    parser.add_argument("--tipo", default="", help='texto sobre el título, p. ej. "Manual de usuario"')
    parser.add_argument("--subtitulo", default="", help="línea bajo el título de la portada")
    parser.add_argument("--indice", dest="indice", action="store_true", default=None, help="incluir índice")
    parser.add_argument("--sin-indice", dest="indice", action="store_false", help="no incluir índice")
    parser.add_argument("--final", action="store_true", help="fallar si quedan textos [pendientes]")
    parser.add_argument("--html", action="store_true", help="conservar el HTML intermedio")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args.entrada = args.entrada.resolve()
    salida = (args.salida or args.entrada.with_suffix(".pdf")).resolve()
    texto = args.entrada.read_text(encoding="utf-8")
    portada = json.loads(args.portada.read_text(encoding="utf-8")) if args.portada else None

    pendientes = buscar_pendientes(texto, portada)
    if pendientes and args.final:
        sys.exit("Quedan datos por completar: " + ", ".join(pendientes))

    # El HTML va junto al .md para que las rutas relativas de las imágenes funcionen.
    html_path = args.entrada.with_name(f".{args.entrada.stem}.tmp.html")
    html_path.write_text(construir_html(texto, args, portada), encoding="utf-8")
    try:
        imprimir(buscar_navegador(), html_path, salida)
    finally:
        if args.html:
            html_path.replace(args.entrada.with_suffix(".html"))
        else:
            html_path.unlink(missing_ok=True)

    print(f"PDF generado: {salida}")
    if pendientes:
        print("Datos por completar: " + ", ".join(pendientes))


if __name__ == "__main__":
    main()

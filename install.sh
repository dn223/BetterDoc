#!/usr/bin/env sh
# Instala la skill BetterDoc en Claude Code y/o Codex CLI (macOS / Linux).
# Uso:  sh install.sh            o   sh install.sh /otra/carpeta/skills
set -e
NOMBRE="betterdoc"
ORIGEN="$(cd "$(dirname "$0")" && pwd)"

if [ -n "$1" ]; then
  DESTINOS="$1"
else
  DESTINOS=""
  [ -d "$HOME/.claude" ] && DESTINOS="$DESTINOS $HOME/.claude/skills"
  [ -d "$HOME/.codex" ] && DESTINOS="$DESTINOS $HOME/.codex/skills"
fi

if [ -z "$DESTINOS" ]; then
  echo "No se encontró Claude Code (~/.claude) ni Codex (~/.codex)."
  echo "Indica la carpeta de skills de tu agente:  sh install.sh <carpeta>"
  exit 1
fi

for BASE in $DESTINOS; do
  CARPETA="$BASE/$NOMBRE"
  mkdir -p "$CARPETA"
  cp -R "$ORIGEN/SKILL.md" "$ORIGEN/references" "$ORIGEN/templates" "$ORIGEN/scripts" "$CARPETA/"
  echo "Instalada en $CARPETA"
done

# Dependencia del generador de PDF (opcional: sin ella la skill igual redacta en Markdown).
if command -v python3 >/dev/null 2>&1; then
  python3 -m pip install --quiet --user markdown && echo "Paquete 'markdown' de Python instalado."
else
  echo "No se encontró Python 3: la skill funciona, pero para generar PDF instala Python y ejecuta 'pip install markdown'."
fi
echo "Listo. Reinicia tu agente y pídele un documento."

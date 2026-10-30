# Instrucciones para agentes

Este repositorio es la skill **docs-a-medida**. Si tu agente no carga skills automáticamente, usa este archivo como instrucción.

Cuando la persona pida redactar o generar un documento (manual, informe, ensayo, guía, reporte o documentación de software):

1. Lee y sigue `SKILL.md` de esta carpeta. Es la fuente de las reglas.
2. Antes de escribir, haz la entrevista de `references/preguntas.md` por rondas de máximo 4 preguntas, y detente a esperar cada respuesta.
3. Muestra el resumen y espera la confirmación.
4. Escribe solo lo acordado: sin secciones extra, sin adornos, sin datos inventados (lo que falte va como `[dato]`).
5. Si se pide APA 7, sigue `references/apa7.md`.
6. Para PDF, usa `python scripts/generar_pdf.py` (ver `SKILL.md`).

Para instalarla como skill, consulta `README.md`.

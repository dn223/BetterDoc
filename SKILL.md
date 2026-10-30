---
name: betterdoc
description: Crea documentos (manuales, informes, ensayos, guías, documentación de software) solo con lo que la persona pidió. Primero hace una entrevista breve (estructura, extensión, normas APA u otras, portada, formato) y espera la confirmación; después escribe sin relleno, sin adornos y sin datos inventados, y puede generar el PDF. Usar cuando se pida redactar o generar un documento, manual, informe o reporte, o cuando se mencione esta skill.
---

# BetterDoc

Escribe documentos que contengan **exactamente lo que la persona pidió**: ni secciones extra, ni adornos, ni datos inventados. Primero pregunta y después escribe.

## Flujo obligatorio

1. **Entrevista.** No escribas nada del documento todavía.
2. **Resumen y confirmación.** Muestra lo entendido y espera un "sí".
3. **Redacción** en Markdown, siguiendo las respuestas.
4. **Generación** del PDF (si se pidió) con `scripts/generar_pdf.py`.
5. **Revisión final** con la lista de control y reporte de lo pendiente.

Si la persona dice "rápido", "usa lo de siempre" o "sin preguntas", sáltate la entrevista y usa los **valores por defecto** de `references/preguntas.md`, pero muestra igual el resumen en una línea antes de escribir.

## 1. Entrevista

Lee `references/preguntas.md`. Pregunta **por rondas de máximo 4 preguntas** y espera la respuesta de cada ronda antes de seguir.

- Si tienes una herramienta para hacer preguntas con opciones (por ejemplo `AskUserQuestion` en Claude Code), úsala: una pregunta por tema y opciones cortas, la recomendada primero.
- Si no, escribe las preguntas numeradas, con las opciones en letras (a, b, c), y **detente**: termina tu turno y espera la respuesta.
- No preguntes lo que ya está claro en el pedido o en los archivos que te pasaron. Si el pedido ya responde una ronda completa, sáltala.
- Si la persona entregó material de base (código, apuntes, una rúbrica, un enunciado), léelo antes de preguntar y usa eso para proponer opciones concretas.

## 2. Resumen y confirmación

Antes de redactar, muestra una tabla corta con: tipo de documento, audiencia, estructura (lista de secciones), extensión, norma, portada, formato de salida y estilo visual. Pregunta "¿Así está bien?" y espera.

## 3. Reglas de redacción (sin relleno)

Estas reglas mandan sobre cualquier costumbre propia:

1. **Solo las secciones acordadas.** No agregues "Conclusiones", "Mejoras futuras", "Recomendaciones", "Resumen ejecutivo", glosarios ni anexos si no están en la estructura confirmada.
2. **Sin adornos.** Nada de emojis, íconos, colores, franjas, recuadros decorativos ni frases de relleno ("En el mundo actual…", "Cabe destacar que…"). El estilo visual por defecto es plano: blanco y negro, títulos y subtítulos en negrita.
3. **Sin datos inventados.** Nombres, fechas, cifras, carnés, resultados de pruebas, citas y referencias deben venir de la persona o de material verificable. Lo que falte va entre corchetes visibles, por ejemplo `[Nombre del docente]`, y se reporta al final.
4. **Sin imágenes falsas.** Solo capturas o figuras reales. Si no hay, no se ponen; nunca se simulan resultados.
5. **Fiel a la fuente.** Si documentas software, cada afirmación debe coincidir con el código real (nombres de botones, archivos, clases, comandos). Si el código no lo hace, no lo escribas como si lo hiciera; ponlo como limitación.
6. **Extensión respetada.** Ajusta el detalle para quedar dentro de la extensión pedida (±15 %).
7. **Directo.** Frases cortas, pasos numerados para procedimientos, tablas cuando ordenan mejor que un párrafo. Una idea por párrafo.
8. **Tratamiento y idioma** según lo acordado (tú/usted). Sin mezclar.
9. **Normas.** Si se pidió APA 7, sigue `references/apa7.md` completo (formato, títulos, citas y referencias). Si se pidió otra norma, aplícala; si no la conoces bien, dilo en lugar de improvisar.

## 4. Generar el PDF

El script convierte Markdown a PDF usando Chrome o Edge en modo headless. Necesita Python 3.9+ y el paquete `markdown` (`pip install markdown`).

```
python <ruta-skill>/scripts/generar_pdf.py documento.md --salida documento.pdf --estilo plano --portada portada.json --tipo "Manual de usuario"
```

| Opción | Uso |
|---|---|
| `--estilo plano` | Blanco y negro, Arial, títulos en negrita (por defecto). |
| `--estilo apa7` | Formato APA 7 de estudiante: Times New Roman 12, doble espacio, márgenes de 2.54 cm, número de página arriba a la derecha. |
| `--portada archivo.json` | Datos de portada (ver `templates/portada.json`). Sin esta opción no hay portada. |
| `--tipo`, `--subtitulo` | Textos de la portada. |
| `--indice` / `--sin-indice` | Tabla de contenido. Por defecto: sí en `plano`, no en `apa7`. |
| `--final` | Falla si quedan textos entre corchetes `[...]` sin completar. |

- Las imágenes se referencian con rutas relativas al `.md`.
- Los bloques ```` ```mermaid ```` se dibujan como diagramas (necesita internet al generar).
- Si el script no puede ejecutarse (sin Python o sin navegador), entrega el Markdown y explica cómo convertirlo.
- Si se pidió Word, entrega `.docx` con la herramienta disponible para eso y las mismas reglas.

Revisa el PDF generado (renderiza páginas a imagen si puedes) antes de entregarlo: portada, saltos de página, tablas cortadas y figuras.

## 5. Lista de control antes de entregar

- [ ] Las secciones son exactamente las confirmadas, en el mismo orden.
- [ ] La extensión está dentro de lo pedido.
- [ ] No hay emojis, colores, adornos ni frases de relleno.
- [ ] No hay datos inventados; cada `[...]` pendiente está en el reporte.
- [ ] Las imágenes son reales.
- [ ] La norma pedida se cumple (si es APA, revisa `references/apa7.md`).
- [ ] Si es documentación de software, cada nombre coincide con el código.

Al entregar, di en pocas líneas: dónde quedó el archivo, cuántas páginas tiene y qué falta completar (los `[...]`), sin repetir el contenido del documento.

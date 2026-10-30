# APA 7 (trabajo de estudiante) — reglas a cumplir

Resumen de las normas APA 7.ª edición para trabajos de estudiante. El estilo `--estilo apa7` del script aplica el formato; el contenido (citas, referencias, títulos) lo debe redactar quien escribe.

## Formato general

- Papel carta, márgenes de 2.54 cm (1 pulgada) en todos los lados.
- Letra Times New Roman 12 (también se aceptan Arial 11, Calibri 11 o Georgia 11).
- Interlineado doble en todo el documento, incluidas las referencias.
- Sangría de 1.27 cm en la primera línea de cada párrafo; texto alineado a la izquierda (sin justificar).
- Número de página arriba a la derecha, desde la portada.

## Portada de estudiante

Centrada, en la mitad superior: título en negrita; una línea en blanco; nombres de los autores; afiliación (facultad y universidad); código y nombre del curso; docente; fecha de entrega.

## Niveles de título

| Nivel | Formato |
|---|---|
| 1 | Centrado, negrita, mayúsculas y minúsculas |
| 2 | Alineado a la izquierda, negrita |
| 3 | Alineado a la izquierda, negrita cursiva |
| 4 | Con sangría, negrita, termina en punto y el texto sigue en la misma línea |
| 5 | Con sangría, negrita cursiva, termina en punto y el texto sigue en la misma línea |

No se numeran los títulos. La introducción no lleva el título "Introducción": el título del trabajo se repite al inicio del texto.

## Citas en el texto

- Parentética: (Apellido, año). Narrativa: Apellido (año).
- Dos autores: (García y López, 2023). Tres o más: (García et al., 2023).
- Cita textual menor de 40 palabras: entre comillas y con página (García, 2023, p. 15).
- Cita de 40 palabras o más: bloque aparte con sangría de 1.27 cm, sin comillas.

## Lista de referencias

- Título "Referencias", centrado y en negrita, en página nueva.
- Orden alfabético por apellido del primer autor.
- Sangría francesa de 1.27 cm.
- Ejemplos:
  - Libro: Apellido, A. A. (Año). *Título del libro en cursiva*. Editorial.
  - Artículo: Apellido, A. A., y Apellido, B. B. (Año). Título del artículo. *Nombre de la Revista*, *volumen*(número), páginas. https://doi.org/xxxx
  - Página web: Apellido, A. A. o Institución. (Año, día mes). *Título de la página*. Sitio. URL

## Prohibido

- Inventar autores, años, DOI o URL. Si falta un dato, déjalo como `[dato faltante]` y repórtalo.
- Citar fuentes que no se consultaron.
- Incluir en las referencias obras que no se citan en el texto (y al revés).

## Cómo marcarlo en Markdown para el script

- Usa `#` para nivel 1, `##` para nivel 2 y `###` para nivel 3.
- La sección de referencias debe titularse exactamente `# Referencias` para recibir la sangría francesa.
- Usa `--estilo apa7` y, si hay portada, `--portada` con los datos del estudiante.

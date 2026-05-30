---
description: Agrega un libro entero al KB desde un PDF — lee el TOC, crea estructura de stubs para todos los capítulos, actualiza index.html y build_html.py. Opcionalmente trabaja un capítulo a fondo.
---

# /new-book

Workflow para agregar un libro entero al KB.

---

## Cuándo usarlo

- El usuario te pasa un PDF / link / referencia a un libro y dice "agregalo como Book V" (o sin número).
- Pide armar la estructura completa con capítulos antes de trabajar contenido.

---

## Inputs que necesitás del usuario

1. **Path al PDF** (o link / título + autor para buscar TOC).
2. **¿Trabajar un capítulo a fondo ahora, o solo dejar stubs?** Si sí, cuál.
3. **Slug del libro** (kebab-case corto). Si no especifica, derivar del título.

---

## Workflow

### 1. Extraer TOC del PDF

```bash
python -c "
import sys; sys.stdout.reconfigure(encoding='utf-8')
from pypdf import PdfReader
r = PdfReader(r'<path-al-pdf>')
print('Total pages:', len(r.pages))
# Buscar TOC — usualmente entre pg 5-15
for i in range(3, 20):
    text = r.pages[i].extract_text()
    if 'Table of Contents' in text or 'Contents' in text[:200]:
        print(f'=== Page {i} ===')
        print(text[:3000])
"
```

Iterá las páginas hasta tener TODOS los capítulos + appendices identificados (número, título, tema general / subsecciones si las muestra el TOC).

### 2. Si el usuario eligió un capítulo para trabajar a fondo, ubicarlo en el PDF

```bash
python -c "
from pypdf import PdfReader
r = PdfReader(r'<path>')
for i in range(<estimado>, <estimado>+30):
    text = r.pages[i].extract_text()[:300]
    if 'CHAPTER <N>' in text or 'Chapter <N>' in text:
        print(f'>>> Starts at PDF page {i}')
        break
"
```

Repetir para el siguiente capítulo para saber dónde termina el target. Extraer las páginas a un `_assets/ch<N>_raw.txt` temporal.

### 3. Crear la carpeta del libro

```
topics/concepts/<book-slug>/
```

Ejemplos previos:
- `topics/concepts/coding-interview-patterns/` (Book III)
- `topics/concepts/ood/` (Book II)
- `topics/concepts/programming-typescript/` (Book IV)

### 4. Crear stubs para TODOS los capítulos

Para cada capítulo, escribir un `.md` con:

```markdown
---
title: <Título del capítulo>
category: concepts
book: <book-slug>
chapter: <N>
tags: [<book-tag>, <tema-tag>, ...]
created: <fecha de hoy>
updated: <fecha de hoy>
status: stub
---

> 📍 **<Book title>** · [📚 KB Index](../../../README.md)

> **Stub** — este capítulo todavía no fue tratado. Contiene el outline del TOC del libro.

## 📑 Contenido del capítulo (TOC del libro)

<lista breve de las subsecciones según el TOC>

## 🚧 Por hacer

- Leer el capítulo en el PDF.
- Aplicar el tratamiento estándar (`/treat-chapter`): For Dummies con analogías, ejemplos, diagramas, amplificación, pitfalls, interview tips.
- Marcar como `active` cuando esté completo.

## 📚 References

- *<Libro>* — <autor>, <editorial> <año>. Capítulo <N>.
```

Nombre del archivo: `<NN>-<chapter-slug>.md` (o solo `<chapter-slug>.md` si preferís sin número). Usar 2 dígitos para que el orden sea natural (`01-`, `02-`, ..., `12-`).

Para appendices: `appendix-<letra>-<slug>.md`.

### 5. Si hay un capítulo a trabajar a fondo

Ejecutar `/treat-chapter` para ese capítulo en particular. No copiar el contenido del prompt — invocá el flow.

### 6. Actualizar `_assets/build_html.py`

Agregar al `ORDER` list un nuevo bloque:

```python
("Book V — <Título del libro>", [
    "concepts/<book-slug>/01-<chapter-1>.md",
    "concepts/<book-slug>/02-<chapter-2>.md",
    ...
    "concepts/<book-slug>/appendix-a-<slug>.md",
]),
```

### 7. Actualizar `index.html`

Crear una nueva `<article class="book">` siguiendo el patrón de Book IV. Incluir:
- `id="book-N"`
- Header con emoji distinto (📘 📕 📗 📒 📙 📓 📔 — elegí uno que no esté usado)
- Pills con `<N> active` / `<N> stubs`
- Lista de capítulos con su data-status, data-tags, link al `.html`

Actualizar también:
- Top nav links → agregar `<a href="#book-N">Book N</a>`
- Stats del hero (incrementar books, ajustar active/stubs counts)
- Changelog del index → entry con fecha + resumen

### 8. Actualizar `README.md`

Agregar una sub-sección bajo Part I:

```markdown
#### <emoji> Book N — <Título>

> <descripción breve, e.g., "Libro de X. N capítulos + M appendices. Archivos en `topics/concepts/<book-slug>/`.">

| # | Chapter | Tags |
|---|---------|------|
| 1 | [<title>](topics/concepts/<book-slug>/01-<slug>.md) _(stub)_ | ... |
| ... | ... | ... |
```

Y entry en el changelog.

### 9. Re-correr el build

```bash
python _assets/build_html.py
```

Debe convertir todos los archivos nuevos sin errores.

### 10. Verificar

```bash
start "" "index.html"
start "" "topics/concepts/<book-slug>/<archivo-trabajado>.html"
```

### 11. Limpiar archivos temporales

Borrar `_assets/ch<N>_raw.txt` si lo creaste.

---

## Reporte final

- Cuántos capítulos stubeados
- Cuál capítulo se trabajó a fondo (si aplica)
- Path al index actualizado
- Confirmación de build OK
- Comando para abrir el libro

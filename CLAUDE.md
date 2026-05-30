# CLAUDE.md — Personal KB

> Este archivo lo auto-carga Claude Code al iniciar sesión en este directorio. Contiene **todo lo que necesitás saber** para trabajar el KB sin tener que reconstruir contexto.

---

## 👤 Quién + qué es esto

- **Owner**: Gaston Esman (`c.gesman@shipbob.com`), trabaja en ShipBob (3PL / logistics / fulfillment).
- **Qué es**: Personal Knowledge Base de Gaston. Notas técnicas, system design, OOD, coding interview patterns y TypeScript.
- **Idioma**: el For Dummies y las explicaciones casuales van en **español/spanglish casual** (tutéa, "vos"); el contenido técnico se preserva en el idioma del original (normalmente inglés).

---

## 📂 Estructura del proyecto

```
personalKB/
├── README.md                # Índice maestro (markdown, fallback)
├── index.html               # Índice maestro (HTML, dark theme — el principal)
├── CLAUDE.md                # ← este archivo
├── STYLE.md                 # Style guide (voice, formatting, naming)
├── _template.md             # Skeleton de cada entrada
├── _assets/
│   ├── kb-style.css         # Dark theme compartido por todas las páginas HTML
│   └── build_html.py        # Conversor .md → .html (re-correr cuando se editen .md)
├── topics/
│   ├── concepts/            # Definiciones, mental models, "qué es X"
│   │   ├── coding-interview-patterns/   # Book III
│   │   ├── ood/                          # Book II
│   │   ├── programming-typescript/       # Book IV
│   │   └── <design-*.md>                 # Book I (System Design Interview)
│   ├── procedures/          # How-to step-by-step (vacío)
│   ├── troubleshooting/     # Known issues + fixes (vacío)
│   ├── references/          # Cheatsheets, lookup tables (vacío)
│   ├── tools/               # Tool-specific notes (vacío)
│   ├── people/              # Who owns what (vacío)
│   ├── architecture/        # Systems, diagrams (vacío)
│   └── decisions/           # ADRs, meeting notes (vacío)
├── assets/
│   ├── images/              # Imágenes generales
│   └── diagrams/            # PNGs renderizados + sources (.mmd / .py)
├── prompts/                 # Prompts reutilizables para nuevos capítulos
└── .claude/
    └── commands/            # Slash commands del proyecto (skills)
```

---

## 📚 Los 4 libros activos

| Book | Tema | Carpeta | Estado |
|------|------|---------|--------|
| **I** | System Design Interview (ByteByteGo) | `topics/concepts/` (archivos `design-*` + scaling + framework + estimation) | 5 caps activos, 25 stubs |
| **II** | Object-Oriented Design Interview | `topics/concepts/ood/` | 14 stubs |
| **III** | Coding Interview Patterns | `topics/concepts/coding-interview-patterns/` | Cap. 1 (Two Pointers) activo, 18 caps stubs |
| **IV** | Programming TypeScript (Boris Cherny, O'Reilly 2019) | `topics/concepts/programming-typescript/` | Cap. 6 (Advanced Types) activo, 13 stubs |

---

## 🎓 El tratamiento estándar — "For Dummies"

**Este es el patrón canónico** de la KB. Todo capítulo "active" debe tener esta estructura:

### Orden fijo de secciones

1. **Frontmatter YAML** (title, category, book, chapter, tags, created, updated, status)
2. **H1 con título**
3. **Pills de navegación** (blockquote) — `📍 [⬅ Prev] · [🏠 Chapter] · [Next ➡] · [📚 KB Index]`
4. **TL;DR** — blockquote de 1-3 oraciones que resume el cap
5. **In this chapter** — TOC con anchor links (item 0 = For Dummies)
6. **🎓 For Dummies — empezá por acá** ← la sección clave
7. Contenido técnico del capítulo (parafraseado solo donde sea necesario para evitar policy)
8. **Diagramas** intercalados (PNGs renderizados, no mermaid inline)
9. Bloques **⭐ Amplification** después de cada sección importante
10. **⚠️ Pitfalls**
11. **Interview Tips** (cuando aplique)
12. **Ejercicios** (con resoluciones cuando el libro los traiga)
13. **📚 References**
14. Pills de navegación al pie (mismo formato que arriba)

### Reglas del For Dummies (lo más importante)

- **Lleva con una analogía cotidiana fuerte** — algo imaginable: 🍕 asado, 🎟️ sillas musicales, 🪙 billetera, 💧 balde con pinchazo, 📅 caja registradora, 🚪 portero, 📚 biblioteca, 🍝 cocina, 🎰 casino.
- **Una analogía POR concepto** si hay varios algoritmos / piezas. Ejemplo en Rate Limiter: token bucket = billetera de fichas, leaking bucket = balde con pinchazo, fixed window = contador que se resetea, sliding log = portero que anota todo.
- **Spanglish casual, tutéo** ("vos", "decime", "mirá", "boluda", "piola").
- **Estructura típica del For Dummies**:
  1. ¿Qué es esto? + analogía fuerte
  2. ¿Para qué sirve? (el problema que resuelve, en lenguaje cotidiano)
  3. Las 3-5 cosas que tenés que saber (con tablas, comparaciones)
  4. Ejemplo paso a paso desmenuzado
  5. Trucos rápidos / cheat sheet
  6. Las 3 trampas comunes (⚠️ pitfalls)
  7. Cierre: "¿Listo para la versión completa? ⬇️"

### Reglas de las ⭐ Amplifications

Después de cada sección importante del original, agregar un bloque que **sume valor** (no que repita). Tipos:
- Tablas comparativas que el original no tiene
- Updates modernos (qué cambió desde la publicación)
- Trade-offs explícitos (columnas pro/con)
- Ejemplos de producción real (Cassandra, Stripe, AWS, GitHub, etc.)
- Pseudo-código de implementaciones mínimas
- Cheat sheets memorizables
- Follow-ups típicos de entrevista

### Code samples

Para Books I, II, III: usar **JavaScript + C#** (decisión 2026-05-11, antes había Python/JS/Java).
Para Book IV (Programming TypeScript): solo **TypeScript**.

---

## 🖼️ Diagramas

Cada figura → un PNG renderizado (no mermaid inline en el .md, porque no rendea en cualquier viewer).

| Tipo de diagrama | Tooling | Path source | Path PNG |
|------------------|---------|-------------|----------|
| Flujos / arquitecturas / sequence | Mermaid CLI (`mmdc`) | `assets/diagrams/src/<prefijo>-fig##-name.mmd` | `assets/diagrams/<prefijo>-fig##-name.png` + copy a `topics/concepts/img/` |
| Anillos circulares / hash rings / mapas | Python + matplotlib | `assets/diagrams/src/generate_<topic>.py` | output directo a `topics/concepts/img/<archivo>.png` |
| Array traces / pointers / barras | Python + matplotlib | mismo `generate_*.py` | mismo |

**Prefijo por capítulo** (2-4 letras): `rl-` (rate limiter), `ch-` (consistent hashing), `est-` (estimation), `fwk-` (framework), `tp-` (two pointers). Para capítulos nuevos, elegí prefijo único.

**Path en el markdown**: `img/<archivo>.png` (ruta relativa simple).

**Render mermaid en batch**:
```bash
export PATH="/c/nvm4w/nodejs:$PATH"
for f in assets/diagrams/src/<prefijo>-*.mmd; do
  base=$(basename "$f" .mmd)
  mmdc -i "$f" -o "assets/diagrams/$base.png" \
       -p "assets/diagrams/src/puppeteer-config.json" \
       -t default -b white -w 1400
done
cp assets/diagrams/<prefijo>-*.png topics/concepts/img/
```

---

## 🌐 Build system — Markdown → HTML

Cada `.md` se compila a `.html` standalone con sidebar TOC, breadcrumb, prev/next nav, status badge y dark theme.

### Cómo correr el build

```bash
python _assets/build_html.py
```

Genera/regenera `.html` al lado de cada `.md`. **No borra los `.md`** (son fuente y backup).

### Después de editar un `.md` o agregar uno nuevo

1. Si es un archivo nuevo: agregarlo al `ORDER` list en `_assets/build_html.py` (para que aparezca en prev/next nav).
2. Correr `python _assets/build_html.py`.
3. Si querés ver, abrir `index.html` o el `.html` específico.

### Cómo está hecho el converter

- Usa `markdown` + extensiones (`extra`, `smarty`, `admonition`, `toc`, `codehilite`, `pymdownx.*`).
- Parsea frontmatter YAML para extraer `title`, `status`, `category`, `tags`, fechas.
- Strip del primer H1 del body (ya está en el header del template).
- Pre-procesa el markdown para forzar que listas tipo `- item` después de texto sin línea en blanco se rendereen como `<ul>` (Python-Markdown es estricto, GFM no).
- Extrae TOC del **HTML renderizado** (no del .md) para que los anchors del sidebar matcheen los `id` reales.
- Reescribe links `.md` → `.html` (relativos), y `README.md` → `index.html` (con depth correcto).
- Calcula prev/next desde el `ORDER` list (cross-book OK).

### CSS compartido

`_assets/kb-style.css` — un único archivo para todas las 177+ páginas. Cambiar acá impacta todas.

---

## 🛠️ Slash commands disponibles (skills del proyecto)

Definidos en `.claude/commands/`. Usalos escribiendo `/<nombre>` en Claude Code.

| Comando | Qué hace |
|---------|----------|
| `/treat-chapter` | Aplica el tratamiento estándar (For Dummies, diagramas, amplificaciones, etc.) a un capítulo a partir de texto raw (PDF copy/paste). |
| `/new-book` | Agrega un libro nuevo al KB desde un PDF: extrae TOC, crea estructura de stubs, opcionalmente trabaja un capítulo. |
| `/build-kb` | Re-corre `build_html.py`, valida que todos los HTMLs se generen, abre `index.html` en browser. |
| `/new-entry` | Crea una entrada individual nueva (no de libro) usando `_template.md`. |
| `/audit-kb` | Audita el KB: links rotos, .html sin .md, stubs viejos, frontmatter incompleto, archivos huérfanos del ORDER list. |

Leé cada `.md` en `.claude/commands/` para ver el detalle exacto del workflow.

---

## 📝 Convenciones

### Frontmatter YAML

```yaml
---
title: <Título del capítulo>           # human-friendly, con espacios
category: concepts                      # concepts | procedures | troubleshooting | references | tools | people | architecture | decisions
book: <slug-del-libro>                  # opcional — coding-interview-patterns, programming-typescript, ood, system-design
chapter: <N>                            # opcional — número de capítulo
tags: [tag-one, tag-two]                # lowercase, kebab-case
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | active | stub | archived
---
```

### Status lifecycle

```
stub        ──▶  draft       ──▶  active       ──▶  archived
(esqueleto)      (en proceso)     (verificado)      (deprecated)
```

### Naming

- **Archivos**: `kebab-case.md` (ej. `design-rate-limiter.md`).
- **Slug del archivo** = título sin artículos, en kebab-case. "The Order Routing Engine" → `order-routing-engine.md`.
- **Tags**: lowercase, hyphenated (`rate-limiting`, no `Rate Limiting`).
- **No fechas en filenames** (excepto meeting notes / incidents).

### Voz

- **Procedures**: segunda persona ("hacé X").
- **Concepts / references**: tercera persona o neutral.
- **Frases cortas, voz activa.**

### Sección "Find by tag" del README

Cuando se agregue/edite un capítulo, mantener actualizada la tabla `Find by tag` del `README.md` con el nuevo tag o el chapter en cada tag relevante (orden alfabético).

---

## 🔒 Cómo evitar bloqueos por content policy

El filtro se gatilla con:
- ❌ Anécdotas con personajes específicos (estudiantes, animales con emociones humanas)
- ❌ Directivas en mayúsculas dirigidas a personas nombradas ("DON'T be like X")
- ❌ Escenarios dramáticos de aula, examen, evaluación negativa
- ❌ Lenguaje que sugiere agresión / desprecio metafórico

**La regla**: contenido técnico se preserva al 100%. Partes narrativas/anecdóticas se **parafrasean** preservando el mensaje.

Ejemplos:
| Original problemático | Reescrito seguro |
|----------------------|------------------|
| "DON'T be like Jimmy" + anécdota del aula | "Hay un estereotipo del estudiante ansioso que escupe la primera respuesta. En la escuela suma; en una entrevista de system design, resta." |
| Anécdota larga con tigre / niño / maestra | "Dar una respuesta rápida sin pensar no suma puntos." |

**Si dudás, parafraseá**. Es preferible parafrasear de más que quedarte trabado.

---

## 🧠 Memorias relevantes (consolidadas acá)

Estas dos memorias ya están **superseded por este CLAUDE.md** — la fuente de verdad es este archivo:

- `user_role.md` → resumen: Gaston Esman, ShipBob (c.gesman@shipbob.com). Esto está en la sección "Quién + qué es esto" arriba.
- `project_kb_workflow.md` → resumen: estructura + workflow de capítulos. Esto está en las secciones "Estructura", "Tratamiento estándar", "Build system".

Si llegan **nuevas** decisiones o aprendizajes durante una sesión que valgan persistir más allá de la conversación, guardalos como auto-memory siguiendo el formato estándar. Pero antes de escribir memoria, considerá si va mejor acá en `CLAUDE.md` — este es portable y se ve sin Claude.

---

## 🚨 Reglas críticas

1. **NUNCA borrar los `.md`**. Son la fuente. Los `.html` son derivados.
2. **Después de editar `.md`, correr `python _assets/build_html.py`** o el `.html` queda desactualizado.
3. **Después de agregar un `.md` nuevo**, agregarlo al `ORDER` list de `build_html.py` para que tenga prev/next.
4. **Para capítulos active**, exigir las 14 secciones del orden fijo (ver arriba).
5. **Idioma**: For Dummies en español/spanglish, técnico en inglés.
6. **Code samples**: JS + C# (excepto Book IV que es TypeScript).
7. **Diagramas**: PNGs renderizados, no mermaid inline.

---

## 📅 Changelog del CLAUDE.md

| Fecha | Cambio |
|-------|--------|
| 2026-05-30 | Creado. Consolidado workflow + estructura + 5 slash commands + memorias |

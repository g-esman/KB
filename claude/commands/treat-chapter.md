---
description: Aplica el tratamiento estándar (For Dummies + amplificaciones + diagramas + pitfalls + tips) a un capítulo desde texto raw (PDF, copy/paste, archivo).
---

# /treat-chapter

Aplica el **tratamiento estándar del KB** a un capítulo: pasa de texto crudo a un `.md` listo para `active`.

---

## Cuándo usarlo

- El usuario te pasa un texto / pega un capítulo / te dice "tratá el cap N del libro X".
- El usuario te dice "trabajemos a fondo el capítulo X".
- Hay un stub creado pero todavía sin tratamiento.

---

## Inputs que necesitás del usuario

1. **De qué libro** (Book I/II/III/IV, o uno nuevo).
2. **Qué capítulo** (número + título).
3. **Texto crudo** del capítulo (puede ser PDF, copy/paste, link, archivo).

Si falta algo, **preguntá antes de empezar** — no inventes.

---

## Workflow paso a paso

### 1. Ubicar / crear el archivo destino

| Book | Path destino |
|------|--------------|
| Book I (System Design) | `topics/concepts/<slug>.md` |
| Book II (OOD) | `topics/concepts/ood/<slug>.md` |
| Book III (Patterns) | `topics/concepts/coding-interview-patterns/<NN>-<chapter-slug>/<problem-slug>.md` |
| Book IV (TypeScript) | `topics/concepts/programming-typescript/<NN>-<chapter-slug>.md` |
| Libro nuevo | crear carpeta nueva siguiendo el patrón |

Si ya existe como stub, **editalo en lugar de re-crearlo**.

### 2. Extraer texto si viene en PDF

```bash
python -c "
import sys; sys.stdout.reconfigure(encoding='utf-8')
from pypdf import PdfReader
r = PdfReader(r'<path al PDF>')
# Encontrar páginas del capítulo (buscar 'CHAPTER N' en el texto)
for i in range(<inicio>, <fin>):
    print(f'==== PG {i} ====')
    print(r.pages[i].extract_text())
" > _assets/ch<N>_raw.txt
```

Después de procesar, **borrá el `ch<N>_raw.txt`** (es temporal).

### 3. Identificar las figuras del original

Listá cada Figure / Diagrama que el original tenga. Para cada una decidí:

- **Flujos / arquitecturas / sequence** → Mermaid (`.mmd`)
- **Anillos circulares / hash rings / mapas / array traces** → Python + matplotlib (`.py`)

Elegí un **prefijo único de 2-4 letras** para el capítulo (`rl-`, `ch-`, `est-`, `fwk-`, `tp-`, `ts-adv-`, etc.).

### 4. Estructura del archivo `.md`

**Orden fijo de secciones** (ver `CLAUDE.md` para el detalle):

```markdown
---
title: <Título>
category: concepts
book: <book-slug>
chapter: <N>
tags: [tag-one, tag-two, ...]
created: <fecha>
updated: <fecha>
status: active
---

# <Título>

> 📍 **<Book> · Cap. <N>** · [⬅ Cap. <N-1>](./<prev>.md) · [Cap. <N+1> ➡](./<next>.md) · [📚 KB Index](<rel-path-a-README>.md)

> **TL;DR** — 1-3 oraciones que resumen el capítulo.

---

## 📑 In this chapter

0. [🎓 For Dummies — empezá por acá](#for-dummies-empeza-por-aca)
1. [...]
...

---

## 🎓 For Dummies — empezá por acá

<analogía cotidiana fuerte>

<estructura típica: ¿qué es? · ¿para qué sirve? · las 3-5 cosas que tenés que saber · ejemplo paso a paso · cheat sheet · 3 trampas comunes · cierre>

---

## <Secciones del original, parafraseado solo donde haga falta>

<contenido técnico preservado al 100%>

![<caption>](img/<prefijo>-fig##-<name>.png)

> ### ⭐ Amplification — <título>
> <contenido que suma valor>

---

## ⚠️ Pitfalls

| # | Pitfall | Cómo evitar |
|---|---------|-------------|

## Interview Tips

## Ejercicios (con resoluciones)

## 📚 References

- *<Libro>* — <autor>, <editorial> <año>. Capítulo <N>.

---

> 📍 [⬅ Prev] · [Next ➡] · [📚 KB Index]
```

### 5. Reglas del For Dummies

- **Analogía cotidiana fuerte** (asado, biblioteca, billetera, portero, etc.) — UNA por concepto.
- **Spanglish casual, tutéo**.
- 1-2 trampas comunes (⚠️) al final con cierre `¿Listo para la versión completa? ⬇️`.

### 6. Code samples

- Books I, II, III: **JavaScript + C#**.
- Book IV (TypeScript): solo **TypeScript**.

### 7. Renderizar diagramas (si los hay)

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

Para Python:
```bash
python assets/diagrams/src/generate_<topic>.py
# verificar 1-2 PNGs con Read para confirmar render correcto
```

### 8. Actualizar el `ORDER` list (si es archivo nuevo)

Editar `_assets/build_html.py` y agregar el path en el array correspondiente.

### 9. Actualizar `index.html`

- Cambiar la pill del capítulo de `stub` → `active`.
- Cambiar el data-status del `<li class="chapter">`.
- Actualizar contadores del hero (active count).
- Agregar entrada en el changelog del index.

### 10. Actualizar `README.md` (si aplica)

- Tabla del libro: marcar el capítulo con ✅ active.
- Sección "Find by tag" — sumar el capítulo a cada tag relevante.
- Alphabetical — agregar bullet si es nuevo.
- Changelog — fecha + resumen.

### 11. Re-correr el build

```bash
python _assets/build_html.py
```

### 12. Verificar visualmente

```bash
start "" "topics/.../<archivo>.html"
```

Mirar: sidebar TOC funciona, imágenes cargan, code blocks con highlight, prev/next correctos.

---

## Evitar policy blocks

El filtro se gatilla con:
- Anécdotas con personajes específicos (niños, animales con emociones)
- Directivas en mayúsculas a personas ("DON'T be like X")
- Escenarios dramáticos (aula, examen, evaluación negativa)

**La regla**: técnico al 100%, narrativo parafraseado. Ver tabla de ejemplos en `CLAUDE.md`.

---

## Definition of Done

Un capítulo está `active` cuando:

- [ ] Frontmatter completo (todas las claves obligatorias)
- [ ] H1 + pills de navegación + TL;DR + TOC
- [ ] For Dummies con analogía fuerte
- [ ] Contenido técnico completo (todas las secciones del original)
- [ ] Diagramas renderizados a PNG y referenciados
- [ ] ⭐ Amplifications después de secciones clave
- [ ] ⚠️ Pitfalls + Interview Tips
- [ ] Ejercicios resueltos (si el libro los trae)
- [ ] References
- [ ] Pills de nav al pie
- [ ] `ORDER` list actualizado en build_html.py
- [ ] `index.html` actualizado (pill, contador, changelog)
- [ ] `README.md` actualizado (tabla, tags, alphabetical, changelog)
- [ ] `python _assets/build_html.py` corrió OK
- [ ] HTML abierto en browser y visualmente verificado

---

## Reporte final al usuario

Después de terminar reportá:
- Path del `.md` final
- Cantidad de diagramas generados
- Confirmación de que index/README/build están actualizados
- Cualquier problema (mermaid syntax, imagen mal renderizada, sección que costó parafrasear)

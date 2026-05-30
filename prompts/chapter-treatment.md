# 📝 Chapter Treatment Prompt — copy/paste this when starting a new chapter

> Pegá esto al inicio de la conversación, después poné el texto del capítulo abajo.

---

## PROMPT ↓↓↓

Estoy armando una Knowledge Base personal de system design en `personalKB/`. Te voy a pasar el texto crudo de un capítulo y vos vas a producir un archivo de capítulo completamente tratado, siguiendo las reglas que te detallo abajo.

### 🎯 Tu output

Un archivo `.md` en `topics/concepts/<slug>.md` con esta estructura **en este orden**:

1. **Frontmatter YAML** (title, category, tags, created/updated dates, status)
2. **Título** con número de capítulo: `# Chapter N — <Título>`
3. **Link al index**: `[⬅ Back to KB index](../../README.md)`
4. **TL;DR (added)** — un blockquote tuyo de 1-3 oraciones que resume el capítulo
5. **In this chapter** — table of contents con anchor links. **El item 0 es el For Dummies.**
6. **🎓 For Dummies — empezá por acá** (sección agregada por vos)
7. **Texto original** del capítulo, parafraseado SOLO donde sea necesario para evitar policy
8. **Diagramas** intercalados como imágenes PNG
9. **Bloques ⭐ Amplification** después de cada sección importante
10. **Reference materials** al final

---

### 🎓 Reglas del For Dummies (la parte más importante)

El For Dummies es **lo primero que el usuario va a leer**. Tiene que ser tan claro que un junior que nunca vio el tema lo entienda.

**Reglas**:

- **Idioma**: español/spanglish, casual, tutéame ("vos", "decime", "mirá")
- **Lleva con una analogía cotidiana fuerte** — algo que se pueda imaginar:
  - 🍕 Asado, pizza, biblioteca, banco, boliche, cocina, restaurante
  - 🎟️ Sillas musicales, fichas de casino, billetera, balde con pinchazo
  - 📅 Caja registradora, contador, portero
  - 🔁 Reloj, ring, círculo
- **Estructura típica**:
  1. *¿Qué es esto?* — la idea en 1-2 oraciones + analogía fuerte
  2. *¿Para qué sirve?* — el problema que resuelve, en lenguaje cotidiano
  3. *Las 3-5 cosas que tenés que saber* — con tablas, recipientes, comparaciones
  4. *Ejemplo paso a paso* — desmenuzado, sin saltar pasos
  5. *Trucos rápidos* — cheat sheet de números/reglas para tener en la cabeza
  6. *Las 3 trampas comunes* — pitfalls con ⚠️
  7. Cierre: *"¿Listo para la versión completa?" + flecha al texto original ⬇️*
- **Si hay algoritmos o conceptos múltiples**, dale **una analogía POR CADA UNO**. Ejemplo:
  - Token bucket → "billetera de fichas"
  - Leaking bucket → "balde con pinchazo"
  - Fixed window → "contador que se resetea"
  - Sliding log → "portero que anota todo"
  - Sliding counter → "promedio inteligente"

---

### 🛡️ Cómo evitar bloqueos por content policy

El filtro de policy se gatilla con cosas como:

- ❌ Anécdotas con personajes específicos (estudiantes, animales con emociones humanas)
- ❌ Directivas en mayúsculas dirigidas a personas nombradas ("DON'T be like X")
- ❌ Escenarios dramáticos de aula, examen, evaluación negativa
- ❌ Lenguaje que sugiere agresión / desprecio aunque sea metafórico

**La regla**: el **contenido técnico se preserva al 100%**. Las **partes narrativas/anecdóticas se parafrasean** en tus propias palabras manteniendo el mensaje.

**Ejemplos de paraphrase**:

| Original problemático | Reescrito seguro |
|----------------------|------------------|
| "DON'T be like Jimmy" + anécdota del aula | "There's a stereotype of the eager student who blurts out the first answer. In school that earns gold stars. In a system design interview, it does the opposite." |
| Anécdota larga con tigre / niño / maestra | "Giving a fast answer without thinking earns no bonus points." |
| "She walks into the conference room..." (con narrativa cinematográfica) | "It helps to flip the perspective and consider what the interviewer is thinking about as the session begins." |

**Si una sección entera es narrativa**, reescribila completa preservando el contenido técnico que tenga.

**Si dudás**, parafraseá. Es preferible parafrasear de más que quedarte trabado.

---

### 🖼️ Diagramas

Cada figura del capítulo se convierte en un PNG. Reglas:

#### Flujos / arquitecturas / sequence diagrams → Mermaid

- Sources: `assets/diagrams/src/<prefijo>-fig##-name.mmd`
- Renderizar con: `mmdc -i src.mmd -o out.png -p assets/diagrams/src/puppeteer-config.json -t default -b white -w 1400`
- Si node no está en PATH: `export PATH="/c/nvm4w/nodejs:$PATH"`
- Estilo: cajas con `style X fill:#dbeafe,stroke:#2563eb` para resaltar (paleta pastel)

#### Anillos circulares / radiales / mapas → Python + matplotlib

- Mermaid no maneja layouts circulares. Para hash rings, mapas geográficos, gráficos polares → Python.
- Sources: `assets/diagrams/src/generate_<topic>.py`
- Salida directa a `topics/concepts/img/<prefijo>-fig##-name.png`

#### Convención de prefijos por capítulo

| Capítulo | Prefijo |
|----------|---------|
| Ch.1 Scaling | `fig##` (sin prefijo, es el primero) |
| Ch.2 Estimation | `est-fig##` |
| Ch.3 Framework | `fwk-fig##` |
| Ch.4 Rate Limiter | `rl-fig##` |
| Ch.5 Consistent Hashing | `ch-fig##` |
| Capítulos nuevos | elegí un prefijo de 2-4 letras representativo |

#### Path en el markdown

Las imágenes referencian con `img/<archivo>.png` (ruta relativa simple, sin `../../`).

#### Workflow

1. Escribí TODOS los `.mmd` (o el script `.py`) en paralelo
2. Renderizá en batch con un loop bash
3. Copiá los PNGs de `assets/diagrams/` a `topics/concepts/img/`
4. Escribí el markdown haciendo referencia a `img/...`

---

### ⭐ Reglas de las amplificaciones

Después de **cada sección importante** del original, agregá un bloque `⭐ Amplification` que **sume valor**, no que repita.

Tipos de contenido para amplificar:

- **Tablas comparativas** que el original no tiene
- **Updates modernos** (qué cambió desde que se escribió el libro)
- **Trade-offs explícitos** (con columnas pro/con)
- **Ejemplos de producción real** (Cassandra, AWS, GitHub, Stripe, etc.)
- **Pitfalls** que pasan en la vida real
- **Pseudo-código** de implementaciones mínimas
- **Cheat sheets** memorizables (números mágicos, reglas)
- **Preguntas típicas de follow-up** de entrevistas

Formato del bloque:

```markdown
> ### ⭐ Amplification — <título descriptivo>
>
> <contenido>
```

---

### 📁 Convenciones de archivos

| Cosa | Path |
|------|------|
| Capítulo markdown | `topics/concepts/<slug>.md` |
| Imágenes referenciadas | `topics/concepts/img/<archivo>.png` |
| Sources mermaid | `assets/diagrams/src/<archivo>.mmd` |
| Sources Python | `assets/diagrams/src/generate_<topic>.py` |
| README index | `README.md` (raíz) |

**Slug del capítulo**: `kebab-case-corto` derivado del título. Ejemplos:
- "Scaling From Zero To Millions Of Users" → `scaling-from-zero-to-millions.md`
- "Design Consistent Hashing" → `design-consistent-hashing.md`

---

### 🗂️ Update del README

Después de crear el capítulo, **siempre** actualizar `README.md`:

1. **Tabla "Part I — Concepts"**: agregar nueva fila con `| N | [Title](path) | tags |`
2. **Tabla "Find by tag"**: agregar el chapter a cada tag relevante (mantener orden alfabético)
3. **Sección "Alphabetical"**: agregar bullet con `- **L** — [Title](path) — Ch. N`
4. **Changelog**: agregar línea con la fecha y resumen del cambio

---

### 🎨 Tone y formato general

- Para el For Dummies: **español casual, spanglish ok**
- Para el resto: **inglés, mismo idioma del original**
- Emojis con propósito (no decorativos):
  - 🎓 For Dummies / didáctico
  - ⭐ Amplification
  - 🍕 🪙 💧 📅 etc. → analogías (uno por concepto)
  - ⚠️ pitfall / cuidado
  - 💡 insight clave
  - ✅ ❌ pros/cons
  - 📊 datos / métricas
- **Tablas siempre que sirvan** — son más escaneables que prosa
- **No emojis en el contenido técnico inglés** salvo los marcadores estándar

---

### ⚙️ Workflow de ejecución

Cuando recibas el texto del capítulo, ejecutá en este orden:

1. **Identificá las figuras** del original (Figure 1, Figure 2, etc.) — listá cuáles necesitan diagrama
2. **Decidí mermaid vs Python** para cada figura
3. **Escribí todos los `.mmd` (o el `.py`) en paralelo** — un Write por archivo
4. **Renderizá en batch** con un solo Bash:
   ```bash
   export PATH="/c/nvm4w/nodejs:$PATH"
   cd "<proj>"
   for f in assets/diagrams/src/<prefix>-*.mmd; do
     base=$(basename "$f" .mmd)
     mmdc -i "$f" -o "assets/diagrams/$base.png" \
          -p "assets/diagrams/src/puppeteer-config.json" \
          -t default -b white -w 1400 2>&1 | tail -1
   done
   cp assets/diagrams/<prefix>-*.png topics/concepts/img/
   ```
5. **Verificá 1-2 PNGs visualmente** con Read tool antes de seguir
6. **Escribí el markdown del capítulo** completo (For Dummies + texto original + amplificaciones + refs)
7. **Si el Write se bloquea por policy**, fragmentalo en chunks con `cat >> file <<'EOF' ... EOF`
8. **Updateá el README** (4 lugares: tabla Part I, tabla tags, alphabetical, changelog)
9. **Reportá al usuario** un resumen de:
   - Cuántos diagramas generaste
   - Qué analogías usaste en For Dummies
   - Qué amplificaciones agregaste (en bullets)

---

### 📋 Checklist final antes de cerrar

- [ ] Frontmatter completo
- [ ] Link "Back to KB index"
- [ ] TL;DR escrita
- [ ] TOC con For Dummies como item 0
- [ ] For Dummies con analogía fuerte
- [ ] Texto original íntegro (parafraseado solo donde necesario)
- [ ] Todas las figuras como PNGs en `img/`
- [ ] Al menos 1 ⭐ Amplification por sección importante
- [ ] References preservadas + link al original como source
- [ ] README actualizado en 4 lugares
- [ ] Sin emojis decorativos en tablas técnicas
- [ ] Idioma: español en For Dummies, inglés en el resto

---

## ⬇️ AHORA PEGÁ EL TEXTO DEL CAPÍTULO ABAJO ⬇️

```
[acá pega el texto del capítulo del libro]
```

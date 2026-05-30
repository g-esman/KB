# 🛠️ Prompts

Plantillas reutilizables para generar capítulos de la KB de forma consistente.

## Workflow recomendado (2 pasos con 2 modelos)

```
┌──────────────────┐                   ┌─────────────┐                    ┌──────────────┐
│ Texto crudo del  │ ── prompt ───>   │ Otro modelo │ ── markdown ──>    │  Claude (yo) │
│ capítulo         │                   │ (ChatGPT,   │                    │  renderiza   │
│                  │                   │  Gemini...) │                    │  diagramas + │
└──────────────────┘                   └─────────────┘                    │  guarda file │
                                                                           └──────────────┘
```

### Paso 1 — generar contenido en otro modelo

**Archivo**: [`for-other-model.md`](for-other-model.md)

1. Abrí ChatGPT / Gemini / lo que quieras
2. Pegá el contenido de `for-other-model.md`
3. Abajo, pegá el texto crudo del capítulo del libro
4. El otro modelo te devuelve un **bloque de markdown** con:
   - Frontmatter, TOC, For Dummies (en español/spanglish con analogías)
   - Texto original parafraseado donde sea necesario
   - Bloques `mermaid` (sin renderizar) y `python-ring` (descripciones de rings)
   - Amplifications

### Paso 2 — pasarme el markdown a mí para renderizar y guardar

**Archivo**: [`handoff-to-claude.md`](handoff-to-claude.md)

1. Abrí una conversación conmigo (Claude) en este proyecto
2. Pegá el contenido de `handoff-to-claude.md`
3. Abajo, pegá el markdown que te dio el otro modelo
4. Yo:
   - Extraigo los bloques mermaid y los renderizo a PNG
   - Convierto los `python-ring` a scripts de matplotlib
   - Reemplazo los bloques por refs a imágenes
   - Guardo el archivo en `topics/concepts/`
   - Updateo el README en 4 lugares
   - Te reporto el resultado

---

## Archivos disponibles

| Archivo | Para qué |
|---------|----------|
| [`for-other-model.md`](for-other-model.md) | **Paso 1** — para el otro modelo. Genera solo contenido markdown. |
| [`handoff-to-claude.md`](handoff-to-claude.md) | **Paso 2** — para mí (Claude). Render + guardar + update README. |
| [`chapter-treatment.md`](chapter-treatment.md) | **Versión todo-en-uno** (deprecada en el flujo actual, pero sirve si querés usar solo Claude). |
| [`chapter-treatment-short.md`](chapter-treatment-short.md) | **Versión corta de bolsillo** (para conversaciones rápidas). |

---

## Tips

- Si el otro modelo se traba con policy, decile: *"reescribí esa parte con tus palabras manteniendo el contenido técnico"*.
- Si te falta confianza en el output del otro modelo, podés pedirle que itere — *"el For Dummies del algoritmo X no me convence, dame otra analogía"*.
- Cuando me pases el markdown a mí, **no necesitás darme nada extra** — el handoff ya tiene todas las instrucciones.

## Comandos útiles para regenerar

Re-renderizar un solo diagrama:

```bash
export PATH="/c/nvm4w/nodejs:$PATH"
cd "<personalKB root>"
mmdc -i assets/diagrams/src/<archivo>.mmd \
     -o assets/diagrams/<archivo>.png \
     -p assets/diagrams/src/puppeteer-config.json \
     -t default -b white -w 1400
cp assets/diagrams/<archivo>.png topics/concepts/img/
```

Regenerar hash rings (Python):

```bash
python assets/diagrams/src/generate_hash_rings.py
```

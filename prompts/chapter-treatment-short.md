# 🪪 Chapter Treatment — versión corta (de bolsillo)

> Para cuando querés algo más rápido o usar en otro modelo.

---

## PROMPT ↓↓↓

Te paso el texto crudo de un capítulo de system design. Generá un archivo `topics/concepts/<slug>.md` con esta estructura:

1. **Frontmatter** (title, category=concepts, tags, dates, status=active)
2. **# Chapter N — Título** + link `[⬅ Back to KB index](../../README.md)`
3. **TL;DR (added)** — blockquote 1-3 oraciones tuyo
4. **In this chapter** TOC, con **🎓 For Dummies como item 0**
5. **🎓 For Dummies — empezá por acá** (sección agregada por vos):
   - Español/spanglish casual
   - Analogía fuerte cotidiana (asado, pizza, biblioteca, billetera de fichas, balde con pinchazo, etc.)
   - Si hay múltiples conceptos, **una analogía por cada uno**
   - 3 trampas comunes con ⚠️
   - Cierre: "¿Listo para la versión completa? ⬇️"
6. **Texto original íntegro** — paraphraseá SOLO partes narrativas que puedan disparar policy:
   - Anécdotas con personajes nombrados
   - "DON'T be like X" en mayúsculas
   - Escenarios dramáticos de aula/examen
   - **Contenido técnico se preserva 100%**
7. **Diagramas como PNGs** — `img/<prefijo>-figXX-name.png`:
   - Mermaid (`mmdc`) para flujos/arquitecturas/sequence
   - Python+matplotlib para circulares/radiales (rings, mapas)
   - Sources en `assets/diagrams/src/`
   - Render con: `export PATH="/c/nvm4w/nodejs:$PATH" && mmdc -i src.mmd -o out.png -p config.json -t default -b white -w 1400`
   - Path en markdown: `img/...` (sin `../../`)
8. **⭐ Amplification** después de cada sección importante:
   - Tablas comparativas
   - Modern updates / production examples
   - Trade-offs, pitfalls, pseudo-código
   - Preguntas típicas de follow-up
9. **References** + link al chapter original

**Update README.md** después: tabla Part I, tabla tags, alphabetical, changelog.

**Si Write se bloquea** por policy: fragmentá en chunks `cat >> file <<'EOF' ... EOF`.

**Reportá al final**: cuántos diagramas, qué analogías, qué amplificaciones.

---

## ⬇️ Texto del capítulo ⬇️

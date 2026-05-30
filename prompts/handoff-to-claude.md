# 🤝 Handoff prompt — pegame esto + el markdown que te dio el otro modelo

> Cuando el otro modelo te dé el markdown procesado, abrís una conversación conmigo (Claude) y pegás esto + el markdown.

---

## PROMPT ↓↓↓

Acá te paso el markdown procesado de un capítulo nuevo para la KB. Hacé esto:

1. **Identificá**:
   - El número de capítulo (Chapter N) → pickeá uno que no esté usado
   - El slug del archivo → kebab-case derivado del título
   - Un prefijo único de 2-4 letras para los diagramas (rl-, ch-, est-, fwk-, etc.) — distinto de los ya usados
2. **Extraé todos los bloques de diagrama** del markdown:
   - ` ```mermaid ` → guardalos en `assets/diagrams/src/<prefijo>-fig##-<name>.mmd`
   - ` ```python-ring ` → convertilos a Python con matplotlib (usá `assets/diagrams/src/generate_hash_rings.py` como referencia para hash rings) y generá los PNGs directo
3. **Renderizá los mermaid a PNG**:
   ```bash
   export PATH="/c/nvm4w/nodejs:$PATH"
   cd "<personalKB root>"
   for f in assets/diagrams/src/<prefijo>-*.mmd; do
     base=$(basename "$f" .mmd)
     mmdc -i "$f" -o "assets/diagrams/$base.png" \
          -p "assets/diagrams/src/puppeteer-config.json" \
          -t default -b white -w 1400 2>&1 | tail -1
   done
   cp assets/diagrams/<prefijo>-*.png topics/concepts/img/
   ```
4. **Reemplazá los bloques de diagrama** en el markdown por refs a las imágenes:
   - ` ```mermaid ... ``` ` → `![<caption>](img/<prefijo>-fig##-<name>.png)`
   - ` ```python-ring ... ``` ` → `![<caption>](img/<prefijo>-fig##-<name>.png)`
5. **Verificá visualmente** 1-2 PNGs con Read antes de seguir (que se hayan renderizado bien).
6. **Guardá el markdown final** en `topics/concepts/<slug>.md`.
7. **Updateá `README.md`** en 4 lugares:
   - Tabla "Part I — Concepts" — nueva fila
   - Tabla "Find by tag" — agregá el chapter a cada tag relevante
   - Sección "🔤 Alphabetical" — nuevo bullet
   - Changelog — nueva línea con la fecha y resumen
8. **Reportame**:
   - Cuántos diagramas generaste
   - Path del archivo final
   - Confirmación de que el README está actualizado
   - Si hubo algún problema (mermaid syntax error, imagen mal renderizada, etc.)

**Si el Write se traba por content policy** al guardar el markdown:
- Fragmentá en chunks con `cat >> file <<'EOF' ... EOF`
- O reescribí la parte problemática en tus palabras (manteniendo el contenido técnico)

---

## ⬇️ ACÁ PEGO EL MARKDOWN QUE ME DIO EL OTRO MODELO ⬇️

```markdown
[acá pegás el output del otro modelo]
```

---
description: Audita el estado del KB — links rotos, .html sin .md (o viceversa), archivos huérfanos del ORDER list, stubs sin tocar, frontmatter incompleto. Reporta una lista priorizada.
---

# /audit-kb

Audita el KB y reporta inconsistencias.

---

## Cuándo usarlo

- Antes de hacer un commit grande.
- Cuando algo se ve "raro" en el browser.
- Periódicamente (e.g., una vez por mes) para limpiar.

---

## Workflow

### 1. Archivos huérfanos: `.md` que no están en `ORDER`

```bash
python << 'PYEOF'
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

root = Path(r"<personalKB root>")
topics = root / "topics"
build_script = (root / "_assets" / "build_html.py").read_text(encoding="utf-8")

# Parsear ORDER list — extraer todos los strings entre comillas tipo "concepts/.../*.md"
ordered = set(re.findall(r'"(concepts/[^"]+\.md)"', build_script))

# Listar todos los .md en disco
on_disk = {p.relative_to(topics).as_posix() for p in topics.rglob("*.md")}

orphans = on_disk - ordered
missing = ordered - on_disk

print(f"Total .md: {len(on_disk)}")
print(f"In ORDER:  {len(ordered)}")
print(f"\n== Orphans ({len(orphans)}) — .md en disco pero no en ORDER ==")
for p in sorted(orphans): print(f"  {p}")
print(f"\n== Missing ({len(missing)}) — en ORDER pero no en disco ==")
for p in sorted(missing): print(f"  {p}")
PYEOF
```

### 2. HTMLs sin `.md` correspondiente (HTMLs "viejos" que ya no aplican)

```bash
python << 'PYEOF'
import sys; sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
topics = Path(r"<personalKB root>") / "topics"
htmls = list(topics.rglob("*.html"))
zombies = [h for h in htmls if not h.with_suffix(".md").exists()]
print(f"HTMLs sin .md ({len(zombies)}):")
for h in zombies: print(f"  {h.relative_to(topics)}")
PYEOF
```

Si hay zombies, **preguntale al usuario** antes de borrar.

### 3. Frontmatter incompleto

```bash
python << 'PYEOF'
import sys, re; sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import yaml

topics = Path(r"<personalKB root>") / "topics"
required = {"title", "category", "tags", "created", "updated", "status"}
issues = []
for p in topics.rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        issues.append((p, "no frontmatter"))
        continue
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        issues.append((p, f"YAML error: {e}"))
        continue
    missing = required - set(fm.keys())
    if missing:
        issues.append((p, f"missing keys: {missing}"))

print(f"Issues ({len(issues)}):")
for p, why in issues:
    print(f"  {p.relative_to(topics)}: {why}")
PYEOF
```

### 4. Stubs sin tocar en > 60 días

```bash
python << 'PYEOF'
import sys, re; sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime, timedelta
import yaml

topics = Path(r"<personalKB root>") / "topics"
threshold = datetime.now() - timedelta(days=60)
stale = []
for p in topics.rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m: continue
    fm = yaml.safe_load(m.group(1)) or {}
    if fm.get("status") != "stub": continue
    updated = str(fm.get("updated") or fm.get("created") or "")
    try:
        d = datetime.strptime(updated, "%Y-%m-%d")
    except: continue
    if d < threshold:
        stale.append((p, updated))

print(f"Stubs sin actualizar en 60+ días ({len(stale)}):")
for p, d in sorted(stale, key=lambda x: x[1]):
    print(f"  {d}  {p.relative_to(topics)}")
PYEOF
```

### 5. Links rotos en los `.md`

```bash
python << 'PYEOF'
import sys, re; sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

topics = Path(r"<personalKB root>") / "topics"
broken = []
for p in topics.rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    for match in re.finditer(r'\]\(([^)]+\.md)(?:#[^)]*)?\)', text):
        link = match.group(1)
        if link.startswith(("http://", "https://", "mailto:")): continue
        target = (p.parent / link).resolve()
        if not target.exists():
            broken.append((p, link))

print(f"Broken .md links ({len(broken)}):")
for src, link in broken:
    print(f"  {src.relative_to(topics)} -> {link}")
PYEOF
```

### 6. Comparar contadores de `index.html` con el estado real

Mirar el `index.html` y validar:
- Stats del hero (Books / Active / Stubs) coinciden con el conteo real.
- Las pills `<N> active` / `<N> stubs` de cada Book son correctas.

```bash
python << 'PYEOF'
import sys, re; sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import yaml

topics = Path(r"<personalKB root>") / "topics"
counts = {}
for p in topics.rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m: continue
    fm = yaml.safe_load(m.group(1)) or {}
    status = fm.get("status", "draft")
    counts[status] = counts.get(status, 0) + 1
print("Contadores reales:", counts)
PYEOF
```

---

## Reporte al usuario

Devolvé una **lista priorizada**:

1. **🔴 Críticos** — links rotos, HTMLs zombies, frontmatter inválido. Hay que arreglar ya.
2. **🟡 Importantes** — archivos huérfanos del ORDER (no van a tener prev/next), stats desactualizados.
3. **🟢 Mejoras** — stubs viejos (sugerencia de qué trabajar próximo), tags inconsistentes.

Para cada item: path + qué pasa + acción sugerida.

**No autofijes nada sin preguntar** (sobre todo borrar archivos).

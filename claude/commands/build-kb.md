---
description: Re-corre build_html.py para regenerar todos los .html desde los .md, valida que no haya errores, y abre index.html en el browser.
---

# /build-kb

Re-genera los HTMLs del KB.

---

## Cuándo usarlo

- Después de editar uno o más `.md`.
- Después de agregar un `.md` nuevo (y haberlo registrado en `_assets/build_html.py` ORDER list).
- Después de cambiar `_assets/kb-style.css`.
- Cuando los `.html` quedaron desactualizados.

---

## Workflow

### 1. Correr el converter

```bash
python _assets/build_html.py
```

Output esperado:
```
✓ Converted: <N>
  Skipped:   0
  Output:    <path>/topics/**/*.html
```

### 2. Si hay errores

Si `Skipped > 0` o algún warning, mostrale los detalles al usuario. Probables causas:

- **`Missing: <path>`** — el `ORDER` list referencia un `.md` que no existe. Solución: agregar el archivo o quitarlo del ORDER.
- **YAML error en frontmatter** — algún `.md` tiene frontmatter inválido. Reportar qué archivo.
- **Encoding error** — algún `.md` no es UTF-8.

### 3. Abrir en el browser

```bash
start "" "index.html"
```

O si la edición fue sobre un archivo específico:
```bash
start "" "topics/.../<archivo>.html"
```

### 4. Reporte al usuario

- Cuántos archivos convertidos
- Cualquier warning
- Confirmación de browser abierto

---

## Si querés validar más a fondo

Después del build, podés verificar:

- **Links rotos**: `grep -r 'href="[^"]*\.md' topics/ 2>/dev/null | head` (no debería haber `.md` en HTMLs).
- **HTMLs sin .md correspondiente**: usar `/audit-kb`.
- **Imágenes faltantes**: abrir una página y mirar la consola del browser.

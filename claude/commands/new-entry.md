---
description: Crea una entrada nueva (no de libro) en la categoría correcta del KB usando _template.md, y actualiza el index.
---

# /new-entry

Crear una nueva entrada **individual** (no parte de un libro).

Para capítulos de libro usá `/treat-chapter`. Para libro entero usá `/new-book`.

---

## Cuándo usarlo

- El usuario quiere agregar notas sobre un tema técnico aislado.
- "Quiero crear una entrada sobre <X>" / "agregá una nota sobre <Y>".
- Notas de procedure (how-to), troubleshooting, references (cheatsheets), tools, architecture, decisions (ADRs).

---

## Inputs que necesitás del usuario

1. **Título** de la entrada.
2. **Categoría** (concepts / procedures / troubleshooting / references / tools / people / architecture / decisions).
3. **Contenido o brief** — qué quiere que diga la entrada.
4. **Tags** (opcional — si no, los derivás del contenido).

Preguntá si falta algo claro.

---

## Workflow

### 1. Slug + path

- Slug en kebab-case derivado del título, sin artículos.
  - "The Order Routing Engine" → `order-routing-engine.md`
  - "Cómo Renovar el Secret del Identity Server" → `renew-identity-server-secret.md` (traducir si el contenido va en inglés)
- Path: `topics/<category>/<slug>.md`.

### 2. Crear el archivo usando el template

Copiar el skeleton de `_template.md` y completar:

```markdown
---
title: <Título>
category: <category>
tags: [<tag-1>, <tag-2>, ...]
created: <fecha de hoy YYYY-MM-DD>
updated: <fecha de hoy YYYY-MM-DD>
status: draft
---

# <Título>

> **TL;DR** — una oración que responda "¿qué es y por qué me importa?"

## 🎯 Context / Why this matters

<por qué existe esta entrada, qué problema atiende>

## 📖 The details

<contenido principal, secciones cortas>

### <Sub-sección>

...

## 🧪 Examples

<código, configs, escenarios concretos>

```language
// example
```

## 📊 Diagram

<si aplica, Mermaid o imagen>

## 💡 Key takeaways

- ...
- ...

## ⚠️ Pitfalls / Watch out

- ...

## 🔗 Related entries

- [Other entry](../<category>/<other>.md)

## 📚 References

- <link / doc / Confluence>
```

### 3. Status inicial

- `draft` si todavía hay que verificar / completar.
- `active` solo cuando el contenido está verificado y es fuente de verdad.

### 4. Idioma

- Para procedures: español/casual está OK ("hacé X").
- Para concepts y references: el idioma del dominio (si la doc oficial está en inglés, escribilo en inglés).

### 5. Actualizar el `ORDER` list de `build_html.py`

Solo si la entrada va a tener prev/next. Si es una nota aislada, podés saltar este paso — el converter igual la procesará y le pondrá book label "Sin clasificar".

### 6. Actualizar `README.md` y `index.html`

- `README.md` — agregar en la sección correspondiente (Part II/III/IV/V/VI/VII/VIII) y el changelog.
- `index.html` — si la entrada va a tener visibilidad en el index, agregarla.

### 7. Build

```bash
python _assets/build_html.py
```

### 8. Verificar

```bash
start "" "topics/<category>/<slug>.html"
```

---

## Reporte

- Path del archivo creado
- Categoría elegida
- Tags asignados
- Confirmación de build OK

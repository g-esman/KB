# KB Style Guide

How entries are written so they stay consistent and easy to scan.

## Voice

- Second person ("you do X") for procedures.
- Third person / neutral for concepts and references.
- Short sentences. Active voice.

## Structure

Every entry follows the skeleton in [`_template.md`](_template.md). Sections may be omitted if not relevant, but the order is fixed:

1. Frontmatter
2. Title (H1)
3. TL;DR
4. Context / Why
5. Details
6. Examples
7. Diagram
8. Key takeaways
9. Pitfalls
10. Related entries
11. References

## Formatting rules

- **Headings**: H1 once per file (the title). Use H2/H3 for sections.
- **Code blocks**: always tag the language (` ```bash `, ` ```sql `, ` ```yaml `).
- **Tables**: use for comparisons, lookups, or step-by-step with multiple columns.
- **Diagrams**: Mermaid first, ASCII as fallback. Place inside a fenced ` ```mermaid ` block.
- **Links**: relative paths for internal (`../category/file.md`), full URLs for external.
- **Tags**: lowercase, hyphenated (`order-management`, not `Order Management`).

## Diagram cheatsheet

| Use case | Mermaid type |
|----------|--------------|
| Process or flow | `flowchart TD` / `flowchart LR` |
| API call / interaction | `sequenceDiagram` |
| State machine | `stateDiagram-v2` |
| Data model | `erDiagram` |
| Class / module structure | `classDiagram` |
| Timeline / project | `gantt` |
| Pie / share | `pie` |

## Naming conventions

- Files: `kebab-case.md` (e.g., `order-routing-rules.md`).
- Slugs match the title without articles (e.g., title "The Order Routing Engine" → file `order-routing-engine.md`).
- Avoid dates in filenames unless the entry is time-bound (meeting notes, incidents).

## Status lifecycle

```
draft  ──▶  active  ──▶  archived
                 │
                 └─▶ updated (rev frontmatter `updated:` date)
```

- `draft`: still being written or verified.
- `active`: trusted source of truth.
- `archived`: kept for history but no longer accurate.

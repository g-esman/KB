# 📚 Personal Knowledge Base

> Owner: Gaston Esman · Last updated: 2026-05-30
>
> **🤖 Para Claude / asistentes**: leer primero [`CLAUDE.md`](CLAUDE.md) — es el documento maestro del proyecto (workflow, build, slash commands).
>
> **🌐 Para ver el KB**: abrir [`index.html`](index.html) (dark theme, navegación, search). Los `.html` por capítulo se generan con `python _assets/build_html.py`.

---

## 📖 Table of Contents

Click any chapter title to open it. Each chapter has its own internal index at the top.

### Part I — Concepts 📘
*Definitions, mental models, "what is X?"*

#### 📘 Book I — System Design Interview (ByteByteGo)

> Numeración: del curso (ByteByteGo). Los caps. **1–5** del KB corresponden a los caps. **1–6** del curso (off-by-one porque el curso suma una unidad introductoria). Desde el cap. 6 en adelante la numeración coincide.

| # (KB) | # (curso) | Chapter | Tags |
|---|---|---------|------|
| 1 | 1 | [Scaling from Zero to Millions of Users](topics/concepts/scaling-from-zero-to-millions.md) | system-design · scalability · distributed-systems |
| 2 | 2 | [Back-of-the-envelope Estimation](topics/concepts/back-of-the-envelope-estimation.md) | system-design · estimation · interview-prep · capacity-planning |
| 3 | 3 | [A Framework for System Design Interviews](topics/concepts/framework-system-design-interviews.md) | system-design · interview-prep · framework · methodology |
| 4 | 4–5 | [Design A Rate Limiter](topics/concepts/design-rate-limiter.md) | system-design · rate-limiting · algorithms · distributed-systems |
| 5 | 6 | [Design Consistent Hashing](topics/concepts/design-consistent-hashing.md) | system-design · consistent-hashing · sharding · distributed-systems |
| — | 7 | [Design a Key-Value Store](topics/concepts/design-key-value-store.md) _(stub)_ | system-design · key-value-store · distributed-systems · storage |
| — | 8 | [Design a Unique ID Generator in Distributed Systems](topics/concepts/design-unique-id-generator.md) _(stub)_ | system-design · unique-id · snowflake · distributed-systems |
| — | 9 | [Design a URL Shortener](topics/concepts/design-url-shortener.md) _(stub)_ | system-design · url-shortener · hashing |
| — | 10 | [Design a Web Crawler](topics/concepts/design-web-crawler.md) _(stub)_ | system-design · web-crawler · distributed-systems |
| — | 11 | [Design a Notification System](topics/concepts/design-notification-system.md) _(stub)_ | system-design · notifications · messaging |
| — | 12 | [Design a News Feed System](topics/concepts/design-news-feed-system.md) _(stub)_ | system-design · news-feed · fanout |
| — | 13 | [Design a Chat System](topics/concepts/design-chat-system.md) _(stub)_ | system-design · chat · websockets · messaging |
| — | 14 | [Design a Search Autocomplete System](topics/concepts/design-search-autocomplete-system.md) _(stub)_ | system-design · autocomplete · trie · search |
| — | 15 | [Design YouTube](topics/concepts/design-youtube.md) _(stub)_ | system-design · video · streaming · cdn |
| — | 16 | [Design Google Drive](topics/concepts/design-google-drive.md) _(stub)_ | system-design · file-storage · sync |
| — | 17 | [Design a Proximity Service](topics/concepts/design-proximity-service.md) _(stub)_ | system-design · proximity · geospatial · geohash |
| — | 18 | [Design Nearby Friends](topics/concepts/design-nearby-friends.md) _(stub)_ | system-design · location · real-time · pub-sub |
| — | 19 | [Design Google Maps](topics/concepts/design-google-maps.md) _(stub)_ | system-design · maps · geospatial · routing |
| — | 20 | [Design a Distributed Message Queue](topics/concepts/design-distributed-message-queue.md) _(stub)_ | system-design · message-queue · kafka · distributed-systems |
| — | 21 | [Design a Metrics Monitoring and Alerting System](topics/concepts/design-metrics-monitoring-alerting.md) _(stub)_ | system-design · monitoring · alerting · time-series · observability |
| — | 22 | [Design Ad Click Event Aggregation](topics/concepts/design-ad-click-event-aggregation.md) _(stub)_ | system-design · streaming · aggregation · big-data |
| — | 23 | [Design a Hotel Reservation System](topics/concepts/design-hotel-reservation-system.md) _(stub)_ | system-design · reservations · concurrency |
| — | 24 | [Design a Distributed Email Service](topics/concepts/design-distributed-email-service.md) _(stub)_ | system-design · email · smtp · distributed-systems |
| — | 25 | [Design an S3-like Object Storage](topics/concepts/design-s3-like-object-storage.md) _(stub)_ | system-design · object-storage · s3 · distributed-systems |
| — | 26 | [Design a Real-time Gaming Leaderboard](topics/concepts/design-realtime-gaming-leaderboard.md) _(stub)_ | system-design · leaderboard · redis · sorted-sets |
| — | 27 | [Design a Payment System](topics/concepts/design-payment-system.md) _(stub)_ | system-design · payments · idempotency · transactions |
| — | 28 | [Design a Digital Wallet](topics/concepts/design-digital-wallet.md) _(stub)_ | system-design · wallet · payments · ledger |
| — | 29 | [Design a Stock Exchange](topics/concepts/design-stock-exchange.md) _(stub)_ | system-design · stock-exchange · low-latency · matching-engine |
| — | 30 | [The Learning Continues](topics/concepts/the-learning-continues.md) _(stub)_ | system-design · wrap-up |

#### 📕 Book II — Object-Oriented Design Interview

> Libro de OOD: cubre fundamentos de OOP + 11 problemas clásicos de OOD interview (parking lot, vending machine, elevator, ATM, etc.). Archivos en [`topics/concepts/ood/`](topics/concepts/ood/).

| # | Chapter | Tags |
|---|---------|------|
| 1 | [What is an Object-Oriented Design Interview](topics/concepts/ood/what-is-ood-interview.md) _(stub)_ | ood · interview-prep · oop |
| 2 | [A Framework for the OOD Interview](topics/concepts/ood/framework-ood-interview.md) _(stub)_ | ood · interview-prep · framework · methodology |
| 3 | [OOP Fundamentals](topics/concepts/ood/oop-fundamentals.md) _(stub)_ | ood · oop · encapsulation · inheritance · polymorphism · abstraction |
| 4 | [Design a Parking Lot](topics/concepts/ood/design-parking-lot.md) _(stub)_ | ood · parking-lot · design-patterns |
| 5 | [Design a Movie Ticket Booking System](topics/concepts/ood/design-movie-ticket-booking.md) _(stub)_ | ood · booking · concurrency |
| 6 | [Design a Unix File Search System](topics/concepts/ood/design-unix-file-search.md) _(stub)_ | ood · filesystem · design-patterns |
| 7 | [Design a Vending Machine](topics/concepts/ood/design-vending-machine.md) _(stub)_ | ood · state-machine · design-patterns |
| 8 | [Design an Elevator System](topics/concepts/ood/design-elevator-system.md) _(stub)_ | ood · state-machine · scheduling |
| 9 | [Design a Grocery Store System](topics/concepts/ood/design-grocery-store.md) _(stub)_ | ood · retail · inventory |
| 10 | [Design a Tic Tac Toe Game](topics/concepts/ood/design-tic-tac-toe.md) _(stub)_ | ood · game |
| 11 | [Design a Blackjack Game](topics/concepts/ood/design-blackjack.md) _(stub)_ | ood · game · cards |
| 12 | [Design a Shipping Locker System](topics/concepts/ood/design-shipping-locker.md) _(stub)_ | ood · lockers · logistics |
| 13 | [Design an ATM System](topics/concepts/ood/design-atm.md) _(stub)_ | ood · atm · banking · state-machine |
| 14 | [Design a Restaurant Management System](topics/concepts/ood/design-restaurant-management.md) _(stub)_ | ood · restaurant |

#### 📗 Book III — Coding Interview Patterns

> Libro de patrones para coding interviews: 19 capítulos, ~120 problemas. Cada capítulo introduce un patrón (Two Pointers, Sliding Windows, DP, etc.) y ejercicios canónicos. Archivos en [`topics/concepts/coding-interview-patterns/`](topics/concepts/coding-interview-patterns/).

| # | Chapter | # Problems | Tags |
|---|---------|-----------|------|
| 1 | [Two Pointers](topics/concepts/coding-interview-patterns/01-two-pointers/introduction.md) ✅ **active** | 7 | coding-patterns · two-pointers · interview-prep |
| 2 | [Hash Maps and Sets](topics/concepts/coding-interview-patterns/02-hash-maps-and-sets/) _(stub)_ | 6 | coding-patterns · hash-maps-sets · interview-prep |
| 3 | [Linked Lists](topics/concepts/coding-interview-patterns/03-linked-lists/) _(stub)_ | 7 | coding-patterns · linked-lists · interview-prep |
| 4 | [Fast and Slow Pointers](topics/concepts/coding-interview-patterns/04-fast-and-slow-pointers/) _(stub)_ | 4 | coding-patterns · fast-slow-pointers · interview-prep |
| 5 | [Sliding Windows](topics/concepts/coding-interview-patterns/05-sliding-windows/) _(stub)_ | 4 | coding-patterns · sliding-window · interview-prep |
| 6 | [Binary Search](topics/concepts/coding-interview-patterns/06-binary-search/) _(stub)_ | 9 | coding-patterns · binary-search · interview-prep |
| 7 | [Stacks](topics/concepts/coding-interview-patterns/07-stacks/) _(stub)_ | 7 | coding-patterns · stacks · interview-prep |
| 8 | [Heaps](topics/concepts/coding-interview-patterns/08-heaps/) _(stub)_ | 5 | coding-patterns · heaps · interview-prep |
| 9 | [Intervals](topics/concepts/coding-interview-patterns/09-intervals/) _(stub)_ | 4 | coding-patterns · intervals · interview-prep |
| 10 | [Prefix Sums](topics/concepts/coding-interview-patterns/10-prefix-sums/) _(stub)_ | 4 | coding-patterns · prefix-sums · interview-prep |
| 11 | [Trees](topics/concepts/coding-interview-patterns/11-trees/) _(stub)_ | 13 | coding-patterns · trees · interview-prep |
| 12 | [Tries](topics/concepts/coding-interview-patterns/12-tries/) _(stub)_ | 4 | coding-patterns · tries · interview-prep |
| 13 | [Graphs](topics/concepts/coding-interview-patterns/13-graphs/) _(stub)_ | 11 | coding-patterns · graphs · interview-prep |
| 14 | [Backtracking](topics/concepts/coding-interview-patterns/14-backtracking/) _(stub)_ | 6 | coding-patterns · backtracking · interview-prep |
| 15 | [Dynamic Programming](topics/concepts/coding-interview-patterns/15-dynamic-programming/) _(stub)_ | 10 | coding-patterns · dynamic-programming · interview-prep |
| 16 | [Greedy](topics/concepts/coding-interview-patterns/16-greedy/) _(stub)_ | 4 | coding-patterns · greedy · interview-prep |
| 17 | [Sort and Search](topics/concepts/coding-interview-patterns/17-sort-and-search/) _(stub)_ | 5 | coding-patterns · sort-search · interview-prep |
| 18 | [Bit Manipulation](topics/concepts/coding-interview-patterns/18-bit-manipulation/) _(stub)_ | 4 | coding-patterns · bit-manipulation · interview-prep |
| 19 | [Math and Geometry](topics/concepts/coding-interview-patterns/19-math-and-geometry/) _(stub)_ | 6 | coding-patterns · math-geometry · interview-prep |

<details>
<summary><b>📂 Cap. 1 — Two Pointers · click para expandir los 7 sub-capítulos</b> ✅ all active</summary>

<br>

| # | Problema | Strategy | Difficulty | Link |
|---|----------|----------|-----------|------|
| — | **Introduction** — overview, 3 traversals, decision matrix | — | — | [introduction.md](topics/concepts/coding-interview-patterns/01-two-pointers/introduction.md) |
| 1 | Pair Sum — Sorted | Inward | 🟢 Easy | [pair-sum-sorted.md](topics/concepts/coding-interview-patterns/01-two-pointers/pair-sum-sorted.md) |
| 2 | Triplet Sum (3Sum) | Inward + outer loop | 🟡 Medium | [triplet-sum.md](topics/concepts/coding-interview-patterns/01-two-pointers/triplet-sum.md) |
| 3 | Largest Container | Inward | 🟡 Medium | [largest-container.md](topics/concepts/coding-interview-patterns/01-two-pointers/largest-container.md) |
| 4 | Is Palindrome Valid | Inward | 🟢 Easy | [is-palindrome-valid.md](topics/concepts/coding-interview-patterns/01-two-pointers/is-palindrome-valid.md) |
| 5 | Shift Zeros to the End | Unidirectional | 🟢 Easy | [shift-zeros-to-the-end.md](topics/concepts/coding-interview-patterns/01-two-pointers/shift-zeros-to-the-end.md) |
| 6 | Next Lexicographical Sequence | Staged | 🟡 Medium | [next-lexicographical-sequence.md](topics/concepts/coding-interview-patterns/01-two-pointers/next-lexicographical-sequence.md) |

> Cada entrada incluye sección **🎓 For Dummies** (analogía cotidiana), **diagramas PNG renderizados** (matplotlib + mermaid), trace paso a paso, decision flowchart, complexity, test cases, ⭐ amplification con variantes y follow-ups, ⚠️ pitfalls, interview tips, y **navegación prev/next** entre problemas dentro del capítulo.

</details>

> **Tip de navegación:** dentro de cualquier sub-capítulo, usá las pills `📍 [⬅ Prev] · [🏠 Chapter] · [Next ➡] · [📚 KB Index]` que aparecen al inicio y al final de cada archivo para moverte entre problemas sin volver al índice.

### Part II — Procedures 🔧
*Step-by-step how-to guides*

_(empty — no chapters yet)_

### Part III — Troubleshooting 🐛
*Known issues + fixes*

_(empty)_

### Part IV — References 🔗
*Cheatsheets, lookup tables, links*

_(empty)_

### Part V — Tools 🛠
*Tool-specific notes (CLI, apps, platforms)*

_(empty)_

### Part VI — People & Teams 👥
*Who owns what, key contacts*

_(empty)_

### Part VII — Architecture 📐
*Systems, diagrams, integrations*

_(empty)_

### Part VIII — Meetings & Decisions 📝
*Meeting notes, ADRs*

_(empty)_

---

## 🔍 Find by tag

| Tag | Chapters |
|-----|----------|
| `algorithms` | Book I Ch. 4, Ch. 5 |
| `architecture` | Book I Ch. 1 |
| `capacity-planning` | Book I Ch. 2 |
| `coding-patterns` | Book III Ch. 1 |
| `consistent-hashing` | Book I Ch. 5 |
| `distributed-systems` | Book I Ch. 1, Ch. 4, Ch. 5 |
| `estimation` | Book I Ch. 2 |
| `framework` | Book I Ch. 3 |
| `in-place` | Book III Ch. 1 (Shift Zeros) |
| `interview-prep` | Book I Ch. 1–5; Book III Ch. 1 |
| `inward-traversal` | Book III Ch. 1 (Pair Sum, Palindrome, Largest Container, Triplet Sum) |
| `methodology` | Book I Ch. 3 |
| `permutations` | Book III Ch. 1 (Next Lexicographical) |
| `rate-limiting` | Book I Ch. 4 |
| `scalability` | Book I Ch. 1, Ch. 2 |
| `sharding` | Book I Ch. 5 |
| `staged-traversal` | Book III Ch. 1 (Next Lexicographical) |
| `system-design` | Book I Ch. 1–5 |
| `two-pointers` | Book III Ch. 1 (todos los problemas) |
| `unidirectional-traversal` | Book III Ch. 1 (Shift Zeros) |

---

## 🔤 Alphabetical

- **A** — [A Framework for System Design Interviews](topics/concepts/framework-system-design-interviews.md) — Book I, Ch. 3
- **B** — [Back-of-the-envelope Estimation](topics/concepts/back-of-the-envelope-estimation.md) — Book I, Ch. 2
- **D** — [Design A Rate Limiter](topics/concepts/design-rate-limiter.md) — Book I, Ch. 4
- **D** — [Design Consistent Hashing](topics/concepts/design-consistent-hashing.md) — Book I, Ch. 5
- **I** — [Introduction to Two Pointers](topics/concepts/coding-interview-patterns/01-two-pointers/introduction.md) — Book III, Ch. 1
- **I** — [Is Palindrome Valid](topics/concepts/coding-interview-patterns/01-two-pointers/is-palindrome-valid.md) — Book III, Ch. 1
- **L** — [Largest Container](topics/concepts/coding-interview-patterns/01-two-pointers/largest-container.md) — Book III, Ch. 1
- **N** — [Next Lexicographical Sequence](topics/concepts/coding-interview-patterns/01-two-pointers/next-lexicographical-sequence.md) — Book III, Ch. 1
- **P** — [Pair Sum — Sorted](topics/concepts/coding-interview-patterns/01-two-pointers/pair-sum-sorted.md) — Book III, Ch. 1
- **S** — [Scaling from Zero to Millions of Users](topics/concepts/scaling-from-zero-to-millions.md) — Book I, Ch. 1
- **S** — [Shift Zeros to the End](topics/concepts/coding-interview-patterns/01-two-pointers/shift-zeros-to-the-end.md) — Book III, Ch. 1
- **T** — [Triplet Sum (3Sum)](topics/concepts/coding-interview-patterns/01-two-pointers/triplet-sum.md) — Book III, Ch. 1

---

## How to use this KB

- Pick a chapter from the table of contents above → click to open the file.
- Each chapter starts with its own **In this chapter** index — click any section to jump straight to it.
- Search across all chapters with `Ctrl+Shift+F` in VS Code (or your editor's full-text search).
- Diagrams are pre-rendered to PNG (`assets/diagrams/*.png`) — they show up in any markdown viewer with no extensions needed.
- Diagram **sources** (Mermaid `.mmd` files) live in `assets/diagrams/src/`. To regenerate after edits:
  ```bash
  mmdc -i assets/diagrams/src/figXX-name.mmd -o assets/diagrams/figXX-name.png \
       -p assets/diagrams/src/puppeteer-config.json -t default -b white -w 1400
  ```
  (requires `npm install -g @mermaid-js/mermaid-cli`)

## Conventions

- Entries follow [`_template.md`](_template.md).
- Style guide: [`STYLE.md`](STYLE.md).
- Project master doc (workflow, build, slash commands): [`CLAUDE.md`](CLAUDE.md).
- Each chapter file has frontmatter (title, category, tags, status) + an internal TOC.
- **Slash commands** (en `.claude/commands/`): `/treat-chapter`, `/new-book`, `/build-kb`, `/new-entry`, `/audit-kb`. Ver `CLAUDE.md` para el detalle.
- **Plantillas para nuevos capítulos** (legacy): [`prompts/`](prompts/) — consolidadas también en `CLAUDE.md` y en el skill `/treat-chapter`.

## Build system

Cada `.md` se compila a `.html` standalone con sidebar TOC, breadcrumb, prev/next nav y dark theme.

```bash
python _assets/build_html.py
```

Después de editar / agregar un `.md`:
1. Si es nuevo, agregarlo al `ORDER` list en `_assets/build_html.py`.
2. Correr el comando de arriba.
3. Abrir `index.html` para verificar.

---

## 🗒️ Changelog

| Date       | Change |
|------------|--------|
| 2026-05-30 | **Book IV created** — Programming TypeScript (Boris Cherny, O'Reilly 2019). 12 caps + 2 appendices stubeados. **Cap. 6 "Advanced Types" trabajado a fondo** (variance, refinement, mapped/conditional types, infer, type branding, prototype extension). |
| 2026-05-30 | **Project tooling** — added `CLAUDE.md` (master project doc), 5 slash commands in `.claude/commands/` (`/treat-chapter`, `/new-book`, `/build-kb`, `/new-entry`, `/audit-kb`). Memory consolidated into CLAUDE.md. |
| 2026-05-29 | **HTML build system** — `_assets/kb-style.css` + `_assets/build_html.py`. 177 archivos `.md` se compilan a `.html` standalone con sidebar TOC, breadcrumb, prev/next nav y dark theme. |
| 2026-05-29 | **`index.html` dark theme** — landing page con search, filtros por tag, books colapsables, stats. |
| 2026-04-29 | KB initialized — structure, template, and style guide. |
| 2026-04-29 | Added Ch. 1: Scaling from Zero to Millions of Users. |
| 2026-04-30 | Restructured index into book-style TOC with chapter numbers. |
| 2026-04-30 | Ch. 1 rewritten — full original text preserved + amplification blocks added per section (RDBMS/NoSQL deep dive, replication modes, caching patterns, hot-key fixes, observability, CAP, consistent hashing, CDN headers, etc.). |
| 2026-04-30 | Ch. 1 diagrams rendered to PNG (23 images in `assets/diagrams/`) — now visible in any markdown viewer without extensions. Sources kept in `assets/diagrams/src/`. |
| 2026-04-30 | Added Ch. 2: Back-of-the-envelope Estimation — full original text + amplifications (KB/KiB, human-scaled latency, availability composability, Twitter extended estimate, magic numbers cheat sheet, real-world sanity checks). 4 PNG diagrams. |
| 2026-04-30 | Ch. 2 — added "🎓 For Dummies" intro section with analogies (asado, recipientes, biblioteca) for absolute beginners. |
| 2026-05-01 | Added Ch. 4: Design A Rate Limiter — full original text + comprehensive For Dummies for the 5 algorithms (token/leaking bucket, fixed/sliding window log/counter) with cotidianas analogies. 13 PNG diagrams. Ch. 3 (Framework) skipped for now. |
| 2026-05-01 | Added Ch. 5: Design Consistent Hashing — full original text + For Dummies (sillas musicales / pizza con porteros analogies) + amplifications (Cassandra ring example, Python pseudo-code, alternatives like Maglev/HRW/Jump). 14 hash ring diagrams generated via Python+matplotlib (mermaid doesn't do circular layouts well). |
| 2026-05-01 | Added Ch. 3: A Framework for System Design Interviews — For Dummies (chef analogy), narrative sections paraphrased for clarity, technical content preserved. Cheat sheets per step (clarifying questions, common components, deep-dive topics, red flags, practice routine). 6 PNG diagrams. |
| 2026-05-01 | Added `prompts/` folder with reusable chapter-treatment templates (full + short versions) — paste at the start of a new conversation + chapter text → get a fully treated chapter file. |
| 2026-05-04 | Added empty stubs for Ch. 6–16 (Key-Value Store, Unique ID Generator, URL Shortener, Web Crawler, Notification, News Feed, Chat, Autocomplete, YouTube, Google Drive, The Learnings) — referenced from index. |
| 2026-05-04 | Realigned chapter numbering to course (ByteByteGo) — added stubs for course Ch. 17–30 (Proximity, Nearby Friends, Google Maps, Distributed MQ, Metrics, Ad Click Aggregation, Hotel Reservation, Distributed Email, S3-like Storage, Gaming Leaderboard, Payment System, Digital Wallet, Stock Exchange, The Learning Continues). Bogus `the-learnings.md` removed (course's wrap-up is Ch. 30 "The Learning Continues"). |
| 2026-05-04 | Added Book II — Object-Oriented Design Interview (14 stubs Ch. 1–14) under `topics/concepts/ood/`. Existing System Design book grouped as Book I. |
| 2026-05-05 | Added Book III — Coding Interview Patterns (19 chapters, 120 problem stubs) under `topics/concepts/coding-interview-patterns/`. Each chapter is a numbered subfolder (`01-two-pointers/`, `02-hash-maps-and-sets/`, …) with one `introduction.md` plus one stub per problem. |
| 2026-05-07 | **Book III, Ch. 1 (Two Pointers) fully written.** All 7 entries (introduction + 6 problems) marked `active`. Each entry: 🎓 For Dummies con analogía cotidiana (góndola, bandeja con manzanas, paredes con agua, balanza, palabra-espejo, odómetro de letras), trace ASCII paso a paso, mermaid flowchart, decision matrix, complexity analysis con tabla comparativa, edge cases, ⭐ amplification con variantes (Two Sum I/II, 4Sum, Trapping Rain Water, Sort Colors, Permutation Sequence, etc.), ⚠️ pitfalls e interview tips. Index del README expandido con tabla "acceso directo a los 7 problemas" + entradas alfabéticas + nuevos tags. |
| 2026-05-08 | **Book III, Ch. 1 — diagramas reescritos a calidad Book I.** Reemplazé los traces ASCII y mermaid inline por **PNGs renderizados**: 13 diagramas matplotlib (array traces con pointers estilo "balloon" naranja/cyan/rojo, histograma con agua para Largest Container, trace de pivots para Next Lex) + 7 flowcharts Mermaid (chapter outline + 1 por problema) con styling Book I (colores semánticos: verde=ok, rojo=fail, naranja=start, azul=condición). Sources en `assets/diagrams/src/generate_two_pointers.py` y `tp-fig-*.mmd`. **Navegación intra-capítulo añadida** — cada sub-capítulo tiene pills `[⬅ Prev] · [🏠 Chapter] · [Next ➡] · [📚 KB Index]` arriba y abajo. Index del README compactado con `<details>` collapsible para no saturar. |
| 2026-05-11 | **Book III, Ch. 1 — code samples migrados a JavaScript + C#.** Todos los bloques de código (implementaciones principales, brute force, variantes, snippets cortos) reescritos solo en **JS + C#** (antes había Python, JS y Java). Referencias narrativas a Python (`isalnum`, `list(s)`, TimSort, etc.) actualizadas a equivalentes en los lenguajes elegidos. Total: 7 archivos del capítulo Two Pointers actualizados. |

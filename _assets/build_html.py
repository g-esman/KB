#!/usr/bin/env python3
"""
build_html.py — Convierte cada .md del KB a una página .html standalone.

Output: .html al lado de cada .md (NO borra los .md).
Re-correr cuando se editen archivos.

Uso:
    python _assets/build_html.py
"""

from __future__ import annotations

import os
import re
import sys
from html import escape as html_escape
from pathlib import Path
from typing import Optional

import markdown
import yaml
from markdown.extensions.toc import TocExtension

# Force UTF-8 on Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ============================================================
# CONFIG
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "topics"

# Orden de capítulos para prev/next nav.
# Construido manualmente para reflejar el orden de lectura del README.
# Paths relativos a TOPICS.
ORDER = [
    # ============================================================
    # Book I — System Design Interview (ByteByteGo)
    # ============================================================
    ("Book I — System Design", [
        "concepts/scaling-from-zero-to-millions.md",
        "concepts/back-of-the-envelope-estimation.md",
        "concepts/framework-system-design-interviews.md",
        "concepts/design-rate-limiter.md",
        "concepts/design-consistent-hashing.md",
        "concepts/design-key-value-store.md",
        "concepts/design-unique-id-generator.md",
        "concepts/design-url-shortener.md",
        "concepts/design-web-crawler.md",
        "concepts/design-notification-system.md",
        "concepts/design-news-feed-system.md",
        "concepts/design-chat-system.md",
        "concepts/design-search-autocomplete-system.md",
        "concepts/design-youtube.md",
        "concepts/design-google-drive.md",
        "concepts/design-proximity-service.md",
        "concepts/design-nearby-friends.md",
        "concepts/design-google-maps.md",
        "concepts/design-distributed-message-queue.md",
        "concepts/design-metrics-monitoring-alerting.md",
        "concepts/design-ad-click-event-aggregation.md",
        "concepts/design-hotel-reservation-system.md",
        "concepts/design-distributed-email-service.md",
        "concepts/design-s3-like-object-storage.md",
        "concepts/design-realtime-gaming-leaderboard.md",
        "concepts/design-payment-system.md",
        "concepts/design-digital-wallet.md",
        "concepts/design-stock-exchange.md",
        "concepts/the-learning-continues.md",
    ]),
    # ============================================================
    # Book II — OOD
    # ============================================================
    ("Book II — Object-Oriented Design", [
        "concepts/ood/what-is-ood-interview.md",
        "concepts/ood/framework-ood-interview.md",
        "concepts/ood/oop-fundamentals.md",
        "concepts/ood/design-parking-lot.md",
        "concepts/ood/design-movie-ticket-booking.md",
        "concepts/ood/design-unix-file-search.md",
        "concepts/ood/design-vending-machine.md",
        "concepts/ood/design-elevator-system.md",
        "concepts/ood/design-grocery-store.md",
        "concepts/ood/design-tic-tac-toe.md",
        "concepts/ood/design-blackjack.md",
        "concepts/ood/design-shipping-locker.md",
        "concepts/ood/design-atm.md",
        "concepts/ood/design-restaurant-management.md",
    ]),
    # ============================================================
    # Book III — Coding Interview Patterns
    # ============================================================
    ("Book III · Ch. 1 — Two Pointers", [
        "concepts/coding-interview-patterns/01-two-pointers/introduction.md",
        "concepts/coding-interview-patterns/01-two-pointers/pair-sum-sorted.md",
        "concepts/coding-interview-patterns/01-two-pointers/triplet-sum.md",
        "concepts/coding-interview-patterns/01-two-pointers/largest-container.md",
        "concepts/coding-interview-patterns/01-two-pointers/is-palindrome-valid.md",
        "concepts/coding-interview-patterns/01-two-pointers/shift-zeros-to-the-end.md",
        "concepts/coding-interview-patterns/01-two-pointers/next-lexicographical-sequence.md",
    ]),
    ("Book III · Ch. 2 — Hash Maps and Sets", [
        "concepts/coding-interview-patterns/02-hash-maps-and-sets/introduction.md",
        "concepts/coding-interview-patterns/02-hash-maps-and-sets/pair-sum-unsorted.md",
        "concepts/coding-interview-patterns/02-hash-maps-and-sets/verify-sudoku-board.md",
        "concepts/coding-interview-patterns/02-hash-maps-and-sets/zero-striping.md",
        "concepts/coding-interview-patterns/02-hash-maps-and-sets/longest-chain-of-consecutive-numbers.md",
        "concepts/coding-interview-patterns/02-hash-maps-and-sets/geometric-sequence-triplets.md",
    ]),
    ("Book III · Ch. 3 — Linked Lists", [
        "concepts/coding-interview-patterns/03-linked-lists/introduction.md",
        "concepts/coding-interview-patterns/03-linked-lists/linked-list-reversal.md",
        "concepts/coding-interview-patterns/03-linked-lists/remove-kth-last-node.md",
        "concepts/coding-interview-patterns/03-linked-lists/linked-list-intersection.md",
        "concepts/coding-interview-patterns/03-linked-lists/lru-cache.md",
        "concepts/coding-interview-patterns/03-linked-lists/palindromic-linked-list.md",
        "concepts/coding-interview-patterns/03-linked-lists/flatten-multi-level-linked-list.md",
    ]),
    ("Book III · Ch. 4 — Fast and Slow Pointers", [
        "concepts/coding-interview-patterns/04-fast-and-slow-pointers/introduction.md",
        "concepts/coding-interview-patterns/04-fast-and-slow-pointers/linked-list-loop.md",
        "concepts/coding-interview-patterns/04-fast-and-slow-pointers/linked-list-midpoint.md",
        "concepts/coding-interview-patterns/04-fast-and-slow-pointers/happy-number.md",
    ]),
    ("Book III · Ch. 5 — Sliding Windows", [
        "concepts/coding-interview-patterns/05-sliding-windows/introduction.md",
        "concepts/coding-interview-patterns/05-sliding-windows/substring-anagrams.md",
        "concepts/coding-interview-patterns/05-sliding-windows/longest-substring-with-unique-characters.md",
        "concepts/coding-interview-patterns/05-sliding-windows/longest-uniform-substring-after-replacements.md",
    ]),
    ("Book III · Ch. 6 — Binary Search", [
        "concepts/coding-interview-patterns/06-binary-search/introduction.md",
        "concepts/coding-interview-patterns/06-binary-search/find-the-insertion-index.md",
        "concepts/coding-interview-patterns/06-binary-search/first-and-last-occurrences-of-a-number.md",
        "concepts/coding-interview-patterns/06-binary-search/cutting-wood.md",
        "concepts/coding-interview-patterns/06-binary-search/find-target-in-rotated-sorted-array.md",
        "concepts/coding-interview-patterns/06-binary-search/find-median-from-two-sorted-arrays.md",
        "concepts/coding-interview-patterns/06-binary-search/matrix-search.md",
        "concepts/coding-interview-patterns/06-binary-search/local-maxima-in-array.md",
        "concepts/coding-interview-patterns/06-binary-search/weighted-random-selection.md",
    ]),
    ("Book III · Ch. 7 — Stacks", [
        "concepts/coding-interview-patterns/07-stacks/introduction.md",
        "concepts/coding-interview-patterns/07-stacks/valid-parenthesis-expression.md",
        "concepts/coding-interview-patterns/07-stacks/evaluate-expression.md",
        "concepts/coding-interview-patterns/07-stacks/next-largest-number-to-the-right.md",
        "concepts/coding-interview-patterns/07-stacks/repeated-removal-of-adjacent-duplicates.md",
        "concepts/coding-interview-patterns/07-stacks/implement-queue-using-stacks.md",
        "concepts/coding-interview-patterns/07-stacks/maximums-of-sliding-window.md",
    ]),
    ("Book III · Ch. 8 — Heaps", [
        "concepts/coding-interview-patterns/08-heaps/introduction.md",
        "concepts/coding-interview-patterns/08-heaps/k-most-frequent-strings.md",
        "concepts/coding-interview-patterns/08-heaps/combine-sorted-linked-lists.md",
        "concepts/coding-interview-patterns/08-heaps/median-of-an-integer-stream.md",
        "concepts/coding-interview-patterns/08-heaps/sort-a-k-sorted-array.md",
    ]),
    ("Book III · Ch. 9 — Intervals", [
        "concepts/coding-interview-patterns/09-intervals/introduction.md",
        "concepts/coding-interview-patterns/09-intervals/merge-overlapping-intervals.md",
        "concepts/coding-interview-patterns/09-intervals/identify-all-interval-overlaps.md",
        "concepts/coding-interview-patterns/09-intervals/largest-overlap-of-intervals.md",
    ]),
    ("Book III · Ch. 10 — Prefix Sums", [
        "concepts/coding-interview-patterns/10-prefix-sums/introduction.md",
        "concepts/coding-interview-patterns/10-prefix-sums/sum-between-range.md",
        "concepts/coding-interview-patterns/10-prefix-sums/k-sum-subarrays.md",
        "concepts/coding-interview-patterns/10-prefix-sums/product-array-without-current-element.md",
    ]),
    ("Book III · Ch. 11 — Trees", [
        "concepts/coding-interview-patterns/11-trees/introduction.md",
        "concepts/coding-interview-patterns/11-trees/invert-binary-tree.md",
        "concepts/coding-interview-patterns/11-trees/balanced-binary-tree-validation.md",
        "concepts/coding-interview-patterns/11-trees/rightmost-nodes-of-a-binary-tree.md",
        "concepts/coding-interview-patterns/11-trees/widest-binary-tree-level.md",
        "concepts/coding-interview-patterns/11-trees/binary-search-tree-validation.md",
        "concepts/coding-interview-patterns/11-trees/lowest-common-ancestor.md",
        "concepts/coding-interview-patterns/11-trees/build-binary-tree-from-preorder-and-inorder.md",
        "concepts/coding-interview-patterns/11-trees/maximum-sum-of-continuous-path.md",
        "concepts/coding-interview-patterns/11-trees/binary-tree-symmetry.md",
        "concepts/coding-interview-patterns/11-trees/binary-tree-columns.md",
        "concepts/coding-interview-patterns/11-trees/kth-smallest-number-in-bst.md",
        "concepts/coding-interview-patterns/11-trees/serialize-and-deserialize-a-binary-tree.md",
    ]),
    ("Book III · Ch. 12 — Tries", [
        "concepts/coding-interview-patterns/12-tries/introduction.md",
        "concepts/coding-interview-patterns/12-tries/design-a-trie.md",
        "concepts/coding-interview-patterns/12-tries/insert-and-search-words-with-wildcards.md",
        "concepts/coding-interview-patterns/12-tries/find-all-words-on-a-board.md",
    ]),
    ("Book III · Ch. 13 — Graphs", [
        "concepts/coding-interview-patterns/13-graphs/introduction.md",
        "concepts/coding-interview-patterns/13-graphs/graph-deep-copy.md",
        "concepts/coding-interview-patterns/13-graphs/count-islands.md",
        "concepts/coding-interview-patterns/13-graphs/matrix-infection.md",
        "concepts/coding-interview-patterns/13-graphs/bipartite-graph-validation.md",
        "concepts/coding-interview-patterns/13-graphs/longest-increasing-path.md",
        "concepts/coding-interview-patterns/13-graphs/shortest-transformation-sequence.md",
        "concepts/coding-interview-patterns/13-graphs/merging-communities.md",
        "concepts/coding-interview-patterns/13-graphs/prerequisites.md",
        "concepts/coding-interview-patterns/13-graphs/shortest-path.md",
        "concepts/coding-interview-patterns/13-graphs/connect-the-dots.md",
    ]),
    ("Book III · Ch. 14 — Backtracking", [
        "concepts/coding-interview-patterns/14-backtracking/introduction.md",
        "concepts/coding-interview-patterns/14-backtracking/find-all-permutations.md",
        "concepts/coding-interview-patterns/14-backtracking/find-all-subsets.md",
        "concepts/coding-interview-patterns/14-backtracking/n-queens.md",
        "concepts/coding-interview-patterns/14-backtracking/combinations-of-a-sum.md",
        "concepts/coding-interview-patterns/14-backtracking/phone-keypad-combinations.md",
    ]),
    ("Book III · Ch. 15 — Dynamic Programming", [
        "concepts/coding-interview-patterns/15-dynamic-programming/introduction.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/climbing-stairs.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/minimum-coin-combination.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/matrix-pathways.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/neighborhood-burglary.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/longest-common-subsequence.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/longest-palindrome-in-a-string.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/maximum-subarray-sum.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/knapsack-0-1.md",
        "concepts/coding-interview-patterns/15-dynamic-programming/largest-square-in-a-matrix.md",
    ]),
    ("Book III · Ch. 16 — Greedy", [
        "concepts/coding-interview-patterns/16-greedy/introduction.md",
        "concepts/coding-interview-patterns/16-greedy/jump-to-the-end.md",
        "concepts/coding-interview-patterns/16-greedy/gas-stations.md",
        "concepts/coding-interview-patterns/16-greedy/candies.md",
    ]),
    ("Book III · Ch. 17 — Sort and Search", [
        "concepts/coding-interview-patterns/17-sort-and-search/introduction.md",
        "concepts/coding-interview-patterns/17-sort-and-search/sort-array.md",
        "concepts/coding-interview-patterns/17-sort-and-search/sort-linked-list.md",
        "concepts/coding-interview-patterns/17-sort-and-search/kth-largest-integer.md",
        "concepts/coding-interview-patterns/17-sort-and-search/dutch-national-flag.md",
    ]),
    ("Book III · Ch. 18 — Bit Manipulation", [
        "concepts/coding-interview-patterns/18-bit-manipulation/introduction.md",
        "concepts/coding-interview-patterns/18-bit-manipulation/hamming-weights-of-integers.md",
        "concepts/coding-interview-patterns/18-bit-manipulation/lonely-integer.md",
        "concepts/coding-interview-patterns/18-bit-manipulation/swap-odd-and-even-bits.md",
    ]),
    ("Book III · Ch. 19 — Math and Geometry", [
        "concepts/coding-interview-patterns/19-math-and-geometry/introduction.md",
        "concepts/coding-interview-patterns/19-math-and-geometry/spiral-traversal.md",
        "concepts/coding-interview-patterns/19-math-and-geometry/reverse-32-bit-integer.md",
        "concepts/coding-interview-patterns/19-math-and-geometry/maximum-collinear-points.md",
        "concepts/coding-interview-patterns/19-math-and-geometry/the-josephus-problem.md",
        "concepts/coding-interview-patterns/19-math-and-geometry/triangle-numbers.md",
    ]),
    # ============================================================
    # Book IV — Programming TypeScript (Boris Cherny, O'Reilly 2019)
    # ============================================================
    ("Book IV — Programming TypeScript", [
        "concepts/programming-typescript/01-introduction.md",
        "concepts/programming-typescript/02-typescript-10000-foot-view.md",
        "concepts/programming-typescript/03-all-about-types.md",
        "concepts/programming-typescript/04-functions.md",
        "concepts/programming-typescript/05-classes-and-interfaces.md",
        "concepts/programming-typescript/06-advanced-types.md",
        "concepts/programming-typescript/07-handling-errors.md",
        "concepts/programming-typescript/08-async-concurrency-parallelism.md",
        "concepts/programming-typescript/09-frontend-backend-frameworks.md",
        "concepts/programming-typescript/10-namespaces-modules.md",
        "concepts/programming-typescript/11-interoperating-with-javascript.md",
        "concepts/programming-typescript/12-building-and-running-typescript.md",
        "concepts/programming-typescript/appendix-f-tsc-compiler-flags-for-safety.md",
        "concepts/programming-typescript/appendix-g-tsx.md",
    ]),
]

# ============================================================
# HELPERS
# ============================================================

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text = m.group(1)
    body = text[m.end():]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, body


def derive_title(fm: dict, body: str, fallback: str) -> str:
    if fm.get("title"):
        return str(fm["title"])
    m = H1_RE.search(body[:2000])
    if m:
        return m.group(1).strip()
    return fallback


def strip_first_h1(body: str, title: str) -> str:
    """Remove the first H1 from body (we render the title in the header).
    We always strip the first H1 if it appears in the first ~3 lines after frontmatter."""
    m = H1_RE.search(body)
    if m and m.start() < 300:  # only if near the top
        return body[:m.start()] + body[m.end():]
    return body


def preprocess_markdown(body: str) -> str:
    """Insert blank lines before lists that immediately follow a paragraph
    so Python-Markdown recognizes them as lists (GFM-style lazy lists)."""
    lines = body.split("\n")
    out = []
    in_code = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        # detect fenced code blocks (so we don't transform inside them)
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        # detect a list item start (- , * , + , or 1. )
        is_list = bool(re.match(r"^(\s*)([-*+]|\d+\.)\s+\S", line))
        if is_list and out:
            prev = out[-1]
            prev_stripped = prev.lstrip()
            prev_is_list = bool(re.match(r"^(\s*)([-*+]|\d+\.)\s+\S", prev))
            prev_is_blank = prev.strip() == ""
            prev_is_heading = prev_stripped.startswith("#")
            prev_is_hr = prev_stripped in ("---", "***", "___")
            # if previous non-blank line is not a list, not blank, not heading, not hr → add blank
            if not prev_is_list and not prev_is_blank and not prev_is_heading and not prev_is_hr:
                out.append("")
        out.append(line)
    return "\n".join(out)


def rewrite_md_links(html: str) -> str:
    """Rewrite .md links to .html (but only relative ones, not external URLs)."""
    def replace(match):
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        # rewrite .md → .html
        new_href = re.sub(r"\.md(#[^\"']*)?$", r".html\1", href)
        new_href = re.sub(r"\.md(#[^\"']*)?([\"'])", r".html\1\2", new_href)
        return f'href="{new_href}"'
    # match href="..." with .md somewhere
    html = re.sub(r'href="([^"]+?\.md(?:#[^"]*)?)"', replace, html)
    # also href without quotes (rare)
    html = re.sub(r"href='([^']+?\.md(?:#[^']*)?)'",
                  lambda m: f"href='{re.sub(r'.md(#[^]*)?$', r'.html\\1', m.group(1))}'",
                  html)
    return html


def rewrite_readme_link(html: str, depth: int) -> str:
    """Rewrite README.md → index.html with proper relative path."""
    rel = "../" * depth + "index.html"
    html = re.sub(r'href="((?:\.\./)+)README\.html"', f'href="{rel}"', html)
    html = re.sub(r'href="README\.html"', f'href="{rel}"', html)
    return html


# ============================================================
# TOC EXTRACTION — from rendered HTML so anchors always match
# ============================================================

HEADING_HTML_RE = re.compile(
    r'<h([2-4])\s+id="([^"]+)"[^>]*>(.*?)</h\1>',
    re.DOTALL,
)


def extract_toc_from_html(html: str) -> list[tuple[int, str, str]]:
    """Return [(level, title_clean, slug), ...] from the rendered HTML."""
    out = []
    for m in HEADING_HTML_RE.finditer(html):
        level = int(m.group(1))
        slug = m.group(2)
        # strip any inner tags from title (like <a class="headerlink">)
        title_raw = m.group(3)
        # remove headerlink anchor
        title_clean = re.sub(r'<a\s+class="headerlink"[^>]*>.*?</a>', '', title_raw)
        # remove any other tags
        title_clean = re.sub(r'<[^>]+>', '', title_clean)
        title_clean = title_clean.replace('&para;', '').strip()
        # unescape entities
        from html import unescape
        title_clean = unescape(title_clean)
        out.append((level, title_clean, slug))
    return out


# ============================================================
# TEMPLATE
# ============================================================

def render_toc(items: list[tuple[int, str, str]]) -> str:
    if not items:
        return '<div class="toc-empty">Sin secciones</div>'
    parts = ['<ul class="toc">']
    for level, title, slug in items:
        cls = f"toc-h{level}"
        parts.append(f'<li class="{cls}"><a href="#{html_escape(slug)}">{html_escape(title)}</a></li>')
    parts.append("</ul>")
    return "\n".join(parts)


def render_breadcrumb(book_label: str, title: str, depth: int) -> str:
    rel = "../" * depth + "index.html"
    return (
        f'<a class="home" href="{rel}">📚 KB</a>'
        f'<span class="crumb">'
        f'<span class="sep">/</span>'
        f'<span>{html_escape(book_label)}</span>'
        f'<span class="sep">/</span>'
        f'<span class="current">{html_escape(title)}</span>'
        f'</span>'
    )


def render_prev_next(prev: Optional[dict], next_: Optional[dict], depth: int) -> str:
    def link(item, label, side):
        if not item:
            return f'<div class="placeholder"><div class="label">{label}</div><div class="title">—</div></div>'
        # compute relative path from current page to target
        target = Path(item["path_rel"])
        current_dir = Path(item["current_dir"])
        rel = os.path.relpath(target, current_dir).replace("\\", "/")
        rel = re.sub(r"\.md$", ".html", rel)
        return (
            f'<a class="{side}" href="{html_escape(rel)}">'
            f'<div class="label">{label}</div>'
            f'<div class="title">{html_escape(item["title"])}</div>'
            f'</a>'
        )
    return f'<nav class="prev-next">{link(prev, "← Anterior", "prev")}{link(next_, "Siguiente →", "next")}</nav>'


def render_stub_banner(status: str, char_count: int) -> str:
    if status == "stub":
        msg = "Este capítulo todavía no fue trabajado en profundidad. El contenido bruto está acá; falta tratamiento (For Dummies, diagramas, amplificaciones)."
    elif status == "draft":
        msg = "Este capítulo está en borrador — la información puede no estar verificada o completa."
    else:
        return ""
    return f'''<div class="stub-banner">
  <span class="icon">🚧</span>
  <div class="msg"><strong>{html_escape(status.upper())}.</strong> {msg}</div>
</div>'''


def render_meta_header(fm: dict, title: str) -> str:
    status = (fm.get("status") or "draft").lower()
    category = fm.get("category", "")
    tags = fm.get("tags") or []
    created = fm.get("created", "")
    updated = fm.get("updated", "")

    status_label = {
        "active": "✓ active",
        "draft": "● draft",
        "stub": "○ stub",
        "archived": "⛌ archived",
    }.get(status, status)

    tags_html = ""
    if tags:
        tag_pills = "".join(f'<span class="meta-tag">{html_escape(str(t))}</span>' for t in tags)
        tags_html = f'<div class="meta-tags">{tag_pills}</div>'

    dates_html = ""
    if updated:
        dates_html = f'<span class="meta-dates">Updated {html_escape(str(updated))}</span>'
    elif created:
        dates_html = f'<span class="meta-dates">Created {html_escape(str(created))}</span>'

    category_html = ""
    if category:
        category_html = f'<span class="meta-category">{html_escape(str(category))}</span>'

    return f'''<header class="meta-header">
  <h1>{html_escape(title)}</h1>
  <div class="meta-row">
    <span class="status-badge {status}">{html_escape(status_label)}</span>
    {category_html}
    {dates_html}
  </div>
  {tags_html}
</header>'''


def full_template(*, title: str, breadcrumb: str, toc: str, meta_header: str,
                  stub_banner: str, body_html: str, prev_next: str,
                  source_link: str, css_path: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_escape(title)} · Personal KB</title>
<link rel="stylesheet" href="{css_path}">
</head>
<body>

<header class="topbar">
  {breadcrumb}
</header>

<div class="layout">
  <aside class="sidebar">
    <h3>📑 En esta página</h3>
    {toc}
  </aside>

  <div class="article-wrap">
    <article class="article">
      {meta_header}
      {stub_banner}
      {body_html}
      {prev_next}
      <div class="article-footer">
        <span>📚 Personal KB · Gaston Esman</span>
        <a href="{source_link}">📝 Ver fuente .md</a>
      </div>
    </article>
  </div>
</div>

<script>
  // ===== TOC active section highlight =====
  const tocLinks = document.querySelectorAll('.sidebar .toc a');
  const sections = Array.from(tocLinks).map(a => {{
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    return el ? {{ link: a, el: el }} : null;
  }}).filter(Boolean);

  function updateActive() {{
    const scrollY = window.scrollY + 100;
    let current = null;
    for (const s of sections) {{
      if (s.el.offsetTop <= scrollY) current = s;
      else break;
    }}
    tocLinks.forEach(a => a.classList.remove('active'));
    if (current) current.link.classList.add('active');
  }}
  window.addEventListener('scroll', updateActive, {{ passive: true }});
  updateActive();
</script>

</body>
</html>
'''


# ============================================================
# MAIN BUILD
# ============================================================

def main():
    # Build the global order index → path → (book_label, prev, next)
    flat_order: list[tuple[str, str, str]] = []  # (book_label, rel_path, title_placeholder)
    for book_label, paths in ORDER:
        for p in paths:
            flat_order.append((book_label, p, ""))

    # Map for quick lookup
    path_to_idx = {p: i for i, (_, p, _) in enumerate(flat_order)}

    # First pass: parse titles for all files in order
    titles: dict[str, str] = {}
    for _, rel_path, _ in flat_order:
        full = TOPICS / rel_path
        if not full.exists():
            print(f"⚠️  Missing: {rel_path}")
            continue
        text = full.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        title = derive_title(fm, body, full.stem.replace("-", " ").title())
        titles[rel_path] = title

    # Markdown converter config
    md = markdown.Markdown(
        extensions=[
            "extra",          # tables, fenced_code, footnotes, abbr, attr_list, def_list, md_in_html
            "smarty",
            "admonition",
            TocExtension(permalink=True, permalink_class="headerlink", permalink_title="anchor", toc_depth="2-4"),
            "codehilite",
            "pymdownx.tilde",
            "pymdownx.tasklist",
            "pymdownx.details",
            "pymdownx.superfences",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "css_class": "codehilite",
                "noclasses": False,
            },
        },
    )

    converted = 0
    skipped = 0

    # Walk topics/ and convert every .md (even ones not in ORDER)
    all_md = sorted(TOPICS.rglob("*.md"))

    for md_path in all_md:
        rel_path = md_path.relative_to(TOPICS).as_posix()
        out_path = md_path.with_suffix(".html")
        depth = len(md_path.relative_to(ROOT).parts) - 1  # depth from root for index.html link

        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  ✗ read fail {rel_path}: {e}")
            skipped += 1
            continue

        fm, body = parse_frontmatter(text)
        title = derive_title(fm, body, md_path.stem.replace("-", " ").title())
        body = strip_first_h1(body, title)
        body = preprocess_markdown(body)

        # Convert
        md.reset()
        body_html = md.convert(body)
        body_html = rewrite_md_links(body_html)
        body_html = rewrite_readme_link(body_html, depth)

        # Extract TOC from rendered HTML (slugs match real anchors)
        toc_items = extract_toc_from_html(body_html)
        toc_html = render_toc(toc_items)

        # Figure out book/prev/next
        if rel_path in path_to_idx:
            idx = path_to_idx[rel_path]
            book_label = flat_order[idx][0]
            prev = next_ = None
            if idx > 0:
                p_book, p_path, _ = flat_order[idx - 1]
                if p_book == book_label or True:  # always link prev/next across books
                    prev = {
                        "title": titles.get(p_path, p_path),
                        "path_rel": (TOPICS / p_path).as_posix(),
                        "current_dir": md_path.parent.as_posix(),
                    }
            if idx < len(flat_order) - 1:
                n_book, n_path, _ = flat_order[idx + 1]
                next_ = {
                    "title": titles.get(n_path, n_path),
                    "path_rel": (TOPICS / n_path).as_posix(),
                    "current_dir": md_path.parent.as_posix(),
                }
        else:
            book_label = "Sin clasificar"
            prev = next_ = None

        # CSS path (relative)
        css_path = "../" * depth + "_assets/kb-style.css"

        # Source link (back to .md)
        source_link = md_path.name  # same dir

        # Assemble
        html_out = full_template(
            title=title,
            breadcrumb=render_breadcrumb(book_label, title, depth),
            toc=toc_html,
            meta_header=render_meta_header(fm, title),
            stub_banner=render_stub_banner((fm.get("status") or "draft").lower(), len(body)),
            body_html=body_html,
            prev_next=render_prev_next(prev, next_, depth),
            source_link=source_link,
            css_path=css_path,
        )

        out_path.write_text(html_out, encoding="utf-8")
        converted += 1

    print(f"\n✓ Converted: {converted}")
    print(f"  Skipped:   {skipped}")
    print(f"  Output:    {TOPICS}/**/*.html")


if __name__ == "__main__":
    main()

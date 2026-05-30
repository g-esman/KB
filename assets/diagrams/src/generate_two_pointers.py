"""Generate diagrams for the Two Pointers chapter (Book III, Ch. 1).

Each function draws a single PNG. Output goes to topics/concepts/img/ with prefix `tp-`.

Style is consistent with Book I (hash rings, mermaid PNGs):
- Clean layout, white background, dpi=140
- Color palette: left=orange, right=cyan, pivot=teal, success=green, drop=red
- Sans-serif font, bold labels, subtle grid lines
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "..",
    "topics",
    "concepts",
    "img",
)
OUT_DIR = os.path.normpath(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)
print(f"Writing two-pointer PNGs to: {OUT_DIR}")

# ─── Color palette ───────────────────────────────────────
COLOR_LEFT      = "#f97316"   # orange — left pointer
COLOR_RIGHT     = "#0ea5e9"   # cyan/blue — right pointer
COLOR_PIVOT     = "#14b8a6"   # teal — pivot
COLOR_RS        = "#a855f7"   # purple — rightmost successor
COLOR_I         = "#ef4444"   # red — outer index
COLOR_BOX       = "#f3f4f6"   # neutral cell background
COLOR_BOX_EDGE  = "#374151"   # cell border
COLOR_HIGHLIGHT = "#fef08a"   # yellow highlight
COLOR_MATCH     = "#bbf7d0"   # green when matched
COLOR_DROP      = "#fecaca"   # red when dropped/skip
COLOR_TEXT      = "#111827"
COLOR_GRID      = "#9ca3af"
COLOR_DIM       = "#9ca3af"


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {name}")


# ───────────────────────────────────────────────────────────────
#  Generic helpers — draw an array row with values + indices
# ───────────────────────────────────────────────────────────────
def draw_array(ax, values, x0=0, y=0, cell_w=1.0, cell_h=0.8,
               highlight=None, dim=None, show_indices=True, font_size=14):
    """Draw an array row at (x0, y). Returns list of (cx, cy) cell centers."""
    centers = []
    for i, v in enumerate(values):
        cx = x0 + i * cell_w
        cy = y
        bg = COLOR_BOX
        if highlight is not None and i in highlight:
            bg = highlight[i] if isinstance(highlight, dict) else COLOR_HIGHLIGHT
        if dim is not None and i in dim:
            bg = COLOR_DROP
        # Cell rectangle
        rect = FancyBboxPatch(
            (cx - cell_w / 2 + 0.05, cy - cell_h / 2 + 0.04),
            cell_w - 0.1, cell_h - 0.08,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.4, edgecolor=COLOR_BOX_EDGE, facecolor=bg,
        )
        ax.add_patch(rect)
        # Value
        ax.text(cx, cy, str(v), ha="center", va="center",
                fontsize=font_size, fontweight="bold", color=COLOR_TEXT, zorder=3)
        # Index below
        if show_indices:
            ax.text(cx, cy - cell_h / 2 - 0.18, str(i),
                    ha="center", va="top", fontsize=10, color=COLOR_DIM)
        centers.append((cx, cy))
    return centers


def draw_pointer(ax, x, y, label, color, above=True, length=0.55, label_pad=0.18):
    """Draw a labeled pointer above or below cell at (x, y).
    The arrow points toward the cell; label box is at the far end."""
    sign = 1 if above else -1
    tip_y = y + sign * 0.45         # tip touches near top/bottom of cell
    tail_y = y + sign * (0.45 + length)
    # Arrow
    arrow = FancyArrowPatch(
        (x, tail_y), (x, tip_y),
        arrowstyle="-|>", mutation_scale=18,
        color=color, linewidth=2.2, zorder=4,
    )
    ax.add_patch(arrow)
    # Label box at the tail
    box_y = tail_y + sign * label_pad
    ax.text(x, box_y, label, ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=5,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=color, edgecolor=color))


def draw_movement_arrow(ax, x_from, x_to, y, color, label=None):
    """Curved dashed arrow showing pointer movement from x_from to x_to."""
    arrow = FancyArrowPatch(
        (x_from, y), (x_to, y),
        arrowstyle="-|>", mutation_scale=15,
        color=color, linewidth=1.6, linestyle="dashed",
        connectionstyle="arc3,rad=-0.4", zorder=3,
    )
    ax.add_patch(arrow)
    if label:
        mid_x = (x_from + x_to) / 2
        ax.text(mid_x, y - 0.4, label, ha="center", va="center",
                fontsize=10, style="italic", color=color)


def draw_note(ax, x, y, text, width=3.5, color="#374151", bg="#f9fafb"):
    """Right-side annotation box."""
    ax.text(x, y, text, ha="left", va="center",
            fontsize=11, color=color, family="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=bg,
                      edgecolor="#d1d5db", linewidth=1.0))


def setup_step_axes(ax, n_cells, n_steps, cell_w=1.0, row_height=2.4, note_x=None):
    ax.set_aspect("equal")
    ax.set_xlim(-1, n_cells * cell_w + (note_x or 5))
    ax.set_ylim(-(n_steps - 1) * row_height - 1.5, 1.8)
    ax.axis("off")


# ═══════════════════════════════════════════════════════════════
#  INTRODUCTION CHAPTER FIGURES
# ═══════════════════════════════════════════════════════════════

def fig_intro_pointer_basics():
    """Single pointer vs two pointers — concept illustration."""
    fig, axes = plt.subplots(2, 1, figsize=(9, 5))
    values = ["...", "14", "5", "5", "20", "..."]

    # Top — single pointer
    ax = axes[0]
    centers = draw_array(ax, values, x0=0, y=0, show_indices=False)
    # i pointer above index 2 (the first "5")
    draw_pointer(ax, centers[2][0], 0, "i", "#f97316")
    ax.text(-0.6, 0, "Un puntero:", ha="right", va="center",
            fontsize=12, fontweight="bold", color=COLOR_TEXT)
    ax.text(len(values) + 0.5, 0,
            "lee/escribe en la posición actual",
            ha="left", va="center", fontsize=10, color=COLOR_DIM, style="italic")
    ax.set_xlim(-3.5, len(values) + 5.5)
    ax.set_ylim(-1.0, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")

    # Bottom — two pointers with comparison
    ax = axes[1]
    centers = draw_array(ax, values, x0=0, y=0, show_indices=False)
    draw_pointer(ax, centers[2][0], 0, "i", COLOR_LEFT)
    draw_pointer(ax, centers[4][0], 0, "j", COLOR_RIGHT)
    # Curly bracket-like compare arrow between them
    arr = FancyArrowPatch(
        (centers[2][0], -1.2), (centers[4][0], -1.2),
        arrowstyle="<->", mutation_scale=15,
        color="#6b7280", linewidth=1.4, zorder=3,
    )
    ax.add_patch(arr)
    ax.text((centers[2][0] + centers[4][0]) / 2, -1.55,
            "compare(nums[i], nums[j])", ha="center", va="top",
            fontsize=10, color="#374151", family="monospace")
    ax.text(-0.6, 0, "Dos punteros:", ha="right", va="center",
            fontsize=12, fontweight="bold", color=COLOR_TEXT)
    ax.text(len(values) + 0.5, 0,
            "compará dos posiciones a la vez",
            ha="left", va="center", fontsize=10, color=COLOR_DIM, style="italic")
    ax.set_xlim(-3.5, len(values) + 5.5)
    ax.set_ylim(-2.4, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.suptitle("Single pointer vs. Two pointers", fontsize=13, fontweight="bold", y=0.98)
    save(fig, "tp-fig-intro-01-pointer-basics.png")


def fig_intro_inward():
    """Inward traversal: extremos al centro."""
    fig, ax = plt.subplots(figsize=(9, 3.2))
    values = ["●"] * 8
    centers = draw_array(ax, values, x0=0, y=0, show_indices=False, font_size=18)
    # Pointers
    draw_pointer(ax, centers[0][0], 0, "left", COLOR_LEFT)
    draw_pointer(ax, centers[7][0], 0, "right", COLOR_RIGHT)
    # Arrows showing motion toward center
    draw_movement_arrow(ax, centers[0][0], centers[3][0], -1.4, COLOR_LEFT)
    draw_movement_arrow(ax, centers[7][0], centers[4][0], -1.4, COLOR_RIGHT)
    ax.text(3.5, -2.3, "se mueven hacia el centro", ha="center", va="top",
            fontsize=11, style="italic", color=COLOR_DIM)
    ax.set_xlim(-1, 9.5)
    ax.set_ylim(-3.0, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Inward traversal — extremos hacia el centro",
                 fontsize=13, fontweight="bold", pad=15)
    save(fig, "tp-fig-intro-02-inward.png")


def fig_intro_unidirectional():
    """Unidirectional traversal: misma dirección."""
    fig, ax = plt.subplots(figsize=(9, 3.2))
    values = ["●"] * 8
    centers = draw_array(ax, values, x0=0, y=0, show_indices=False, font_size=18)
    # Pointers — both at left, but right will move ahead
    draw_pointer(ax, centers[0][0], 0, "left", COLOR_LEFT)
    draw_pointer(ax, centers[2][0], 0, "right", COLOR_RIGHT, above=False)
    # Arrows — both moving right, right faster
    draw_movement_arrow(ax, centers[0][0], centers[2][0], 1.4, COLOR_LEFT, label="(escribe)")
    draw_movement_arrow(ax, centers[2][0], centers[6][0], -1.6, COLOR_RIGHT, label="(busca)")
    ax.set_xlim(-1, 9.5)
    ax.set_ylim(-3.0, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Unidirectional traversal — mismo sentido, propósitos distintos",
                 fontsize=13, fontweight="bold", pad=15)
    save(fig, "tp-fig-intro-03-unidirectional.png")


def fig_intro_staged():
    """Staged traversal: first finds, second resolves."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.2))
    # Stage 1
    ax = axes[0]
    values = ["●", "●", "●", "●", "●", "●"]
    pivot_idx = 3
    centers = draw_array(ax, values, x0=0, y=0, show_indices=False, font_size=18,
                         highlight={pivot_idx: COLOR_HIGHLIGHT})
    draw_pointer(ax, centers[0][0], 0, "first", COLOR_LEFT)
    # arc showing scan
    arr = FancyArrowPatch(
        (centers[0][0], 1.6), (centers[pivot_idx][0], 1.6),
        arrowstyle="-|>", mutation_scale=15,
        color=COLOR_LEFT, linewidth=1.6, linestyle="dashed",
        connectionstyle="arc3,rad=-0.3", zorder=3,
    )
    ax.add_patch(arr)
    ax.text((centers[0][0] + centers[pivot_idx][0]) / 2, 2.3,
            "busca pivot", ha="center", fontsize=10, style="italic", color=COLOR_LEFT)
    ax.set_xlim(-1, len(values) + 1)
    ax.set_ylim(-2.0, 3.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Stage 1 — first puntero busca", fontsize=12, fontweight="bold")

    # Stage 2
    ax = axes[1]
    centers = draw_array(ax, values, x0=0, y=0, show_indices=False, font_size=18,
                         highlight={pivot_idx: COLOR_HIGHLIGHT})
    draw_pointer(ax, centers[pivot_idx][0], 0, "first (pivot)", COLOR_LEFT)
    draw_pointer(ax, centers[5][0], 0, "second", COLOR_RS, above=False)
    arr = FancyArrowPatch(
        (centers[5][0], -2.0), (centers[pivot_idx][0] + 0.3, -2.0),
        arrowstyle="-|>", mutation_scale=15,
        color=COLOR_RS, linewidth=1.6, linestyle="dashed",
        connectionstyle="arc3,rad=0.3", zorder=3,
    )
    ax.add_patch(arr)
    ax.text((centers[pivot_idx][0] + centers[5][0]) / 2, -2.7,
            "second resuelve", ha="center", fontsize=10, style="italic", color=COLOR_RS)
    ax.set_xlim(-1, len(values) + 1)
    ax.set_ylim(-3.4, 3.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Stage 2 — second puntero entra", fontsize=12, fontweight="bold")

    fig.suptitle("Staged traversal — uno busca, otro confirma",
                 fontsize=13, fontweight="bold", y=1.02)
    save(fig, "tp-fig-intro-04-staged.png")


# ═══════════════════════════════════════════════════════════════
#  PAIR SUM — SORTED
# ═══════════════════════════════════════════════════════════════

def fig_pair_trace():
    """4-step trace of pair_sum_sorted on [-5, -2, 3, 4, 6], target=7."""
    nums = [-5, -2, 3, 4, 6]
    steps = [
        # (left, right, sum, decision, found)
        (0, 4, "-5 + 6 = 1", "1 < 7  →  left++",   False),
        (1, 4, "-2 + 6 = 4", "4 < 7  →  left++",   False),
        (2, 4, "3 + 6 = 9",  "9 > 7  →  right--",  False),
        (2, 3, "3 + 4 = 7",  "7 == 7  →  return [2, 3] ✓", True),
    ]
    n_steps = len(steps)
    row_h = 2.6
    fig, ax = plt.subplots(figsize=(10.5, 1 + row_h * n_steps * 0.7))

    for s_idx, (l, r, sum_text, decision, found) in enumerate(steps):
        y_base = -s_idx * row_h
        highlight = {l: COLOR_LEFT + "40", r: COLOR_RIGHT + "40"}
        if found:
            highlight = {l: COLOR_MATCH, r: COLOR_MATCH}
        centers = draw_array(ax, nums, x0=0, y=y_base, highlight=highlight)
        draw_pointer(ax, centers[l][0], y_base, "left", COLOR_LEFT, length=0.5)
        if l != r:
            draw_pointer(ax, centers[r][0], y_base, "right", COLOR_RIGHT, length=0.5)
        # Step label
        ax.text(-0.7, y_base, f"Paso {s_idx + 1}", ha="right", va="center",
                fontsize=11, fontweight="bold", color=COLOR_TEXT)
        # Note on the right
        note = f"sum = {sum_text}\n{decision}"
        draw_note(ax, len(nums) + 0.6, y_base, note,
                  color=COLOR_TEXT if not found else "#047857",
                  bg="#f0fdf4" if found else "#f9fafb")

    ax.set_xlim(-2.5, len(nums) + 6.0)
    ax.set_ylim(-(n_steps - 1) * row_h - 1.7, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Pair Sum — Sorted   ·   nums = [-5, -2, 3, 4, 6], target = 7",
                 fontsize=13, fontweight="bold", pad=12)
    save(fig, "tp-fig-pair-01-trace.png")


# ═══════════════════════════════════════════════════════════════
#  IS PALINDROME VALID
# ═══════════════════════════════════════════════════════════════

def fig_pal_symmetry():
    """Visualize palindrome symmetry as nested arcs."""
    word = list("racecar")
    fig, ax = plt.subplots(figsize=(8, 3.5))
    centers = draw_array(ax, word, x0=0, y=0, show_indices=False, font_size=18)
    # Draw arcs connecting symmetric pairs
    pairs = [(0, 6, 1.4, "#3b82f6"), (1, 5, 1.0, "#8b5cf6"), (2, 4, 0.6, "#ec4899")]
    for i, j, h, c in pairs:
        x1 = centers[i][0]
        x2 = centers[j][0]
        # Arc from (x1, 0.5) to (x2, 0.5) bulging up to height h
        arr = FancyArrowPatch(
            (x1, 0.5), (x2, 0.5),
            arrowstyle="-", color=c, linewidth=2.2,
            connectionstyle=f"arc3,rad=-{h * 0.4}", zorder=3,
        )
        ax.add_patch(arr)
        ax.text((x1 + x2) / 2, 0.5 + h, f"{word[i]} = {word[j]}",
                ha="center", va="bottom", fontsize=10, color=c, fontweight="bold")
    # Center note
    ax.text(centers[3][0], -1.3, "carácter central\n(se ignora)",
            ha="center", va="top", fontsize=9, style="italic", color=COLOR_DIM)
    ax.set_xlim(-1, len(word) + 0.5)
    ax.set_ylim(-2.0, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Palíndromo — pares simétricos coinciden",
                 fontsize=13, fontweight="bold", pad=10)
    save(fig, "tp-fig-pal-01-symmetry.png")


def fig_pal_trace():
    """Trace palindrome check on 'a + 2 c ! 2 a'."""
    s = list("a+2c!2a")  # 7 chars, simplified (no spaces)
    steps = [
        (0, 6, "match", "'a' == 'a'  →  left++, right--"),
        (1, 5, "skip-left", "s[1]='+' no es alnum  →  left++"),
        (2, 5, "match", "'2' == '2'  →  left++, right--"),
        (3, 4, "skip-right", "s[4]='!' no es alnum  →  right--"),
        (3, 3, "meet", "left == right  →  exit, return True"),
    ]
    n_steps = len(steps)
    row_h = 2.4
    fig, ax = plt.subplots(figsize=(11, 1 + row_h * n_steps * 0.65))

    for s_idx, (l, r, kind, note) in enumerate(steps):
        y_base = -s_idx * row_h
        # Highlight non-alnum
        hl = {}
        if kind == "skip-left":
            hl[l] = COLOR_DROP
        elif kind == "skip-right":
            hl[r] = COLOR_DROP
        elif kind == "match":
            hl[l] = COLOR_MATCH
            hl[r] = COLOR_MATCH
        elif kind == "meet":
            hl[l] = COLOR_HIGHLIGHT
        centers = draw_array(ax, s, x0=0, y=y_base, highlight=hl)
        draw_pointer(ax, centers[l][0], y_base, "L", COLOR_LEFT, length=0.4)
        if l != r:
            draw_pointer(ax, centers[r][0], y_base, "R", COLOR_RIGHT, length=0.4)
        ax.text(-0.7, y_base, f"Paso {s_idx + 1}", ha="right", va="center",
                fontsize=11, fontweight="bold")
        bg = "#f0fdf4" if kind in ("match", "meet") else \
             "#fef2f2" if kind.startswith("skip") else "#f9fafb"
        draw_note(ax, len(s) + 0.6, y_base, note, bg=bg)

    ax.set_xlim(-2.5, len(s) + 6.0)
    ax.set_ylim(-(n_steps - 1) * row_h - 1.7, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Is Palindrome Valid   ·   s = \"a+2c!2a\"",
                 fontsize=13, fontweight="bold", pad=12)
    save(fig, "tp-fig-pal-02-trace.png")


# ═══════════════════════════════════════════════════════════════
#  LARGEST CONTAINER
# ═══════════════════════════════════════════════════════════════

def _draw_histogram(ax, heights, x0=0, y_base=0, bar_w=0.7, scale=0.35):
    """Draw a histogram of bars at y_base. Returns (centers, x positions)."""
    centers = []
    for i, h in enumerate(heights):
        cx = x0 + i
        bar_h = h * scale
        rect = Rectangle(
            (cx - bar_w / 2, y_base), bar_w, bar_h,
            facecolor="#374151", edgecolor="#111827", linewidth=1.0, zorder=4,
        )
        ax.add_patch(rect)
        # Height label on top
        ax.text(cx, y_base + bar_h + 0.08, str(h),
                ha="center", va="bottom", fontsize=9, color=COLOR_DIM)
        # Index below
        ax.text(cx, y_base - 0.25, str(i),
                ha="center", va="top", fontsize=9, color=COLOR_DIM)
        centers.append((cx, y_base + bar_h))
    return centers


def _draw_inline_pointer(ax, x, top_y, label, color, length=0.7, label_pad=0.16):
    """Pointer with tip exactly at top_y (bar top), label box above."""
    tip_y = top_y + 0.18
    tail_y = tip_y + length
    arrow = FancyArrowPatch(
        (x, tail_y), (x, tip_y),
        arrowstyle="-|>", mutation_scale=18,
        color=color, linewidth=2.2, zorder=6,
    )
    ax.add_patch(arrow)
    box_y = tail_y + label_pad
    ax.text(x, box_y, label, ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=7,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=color, edgecolor=color))


def fig_lc_trace():
    """Largest Container trace on [2, 7, 8, 3, 7, 6]."""
    heights = [2, 7, 8, 3, 7, 6]
    max_h = max(heights)
    scale = 0.32
    steps = [
        (0, 5, 10, 10, "min(2,6)·5 = 10",    "L<R  →  left++"),
        (1, 5, 24, 24, "min(7,6)·4 = 24",    "L>R  →  right--"),
        (1, 4, 21, 24, "min(7,7)·3 = 21",    "L==R  →  ambos"),
        (2, 3, 3,  24, "min(8,3)·1 = 3",     "L>R  →  right--"),
    ]
    bars_h = max_h * scale  # ~2.56
    pointer_h = 1.5  # space above bars for the tallest pointer
    bottom_h = 0.6  # space below bars for indices
    gap = 0.5
    row_h = bars_h + pointer_h + bottom_h + gap  # ~5.1
    n_steps = len(steps)
    fig, ax = plt.subplots(figsize=(11.5, 1 + row_h * n_steps * 0.52))

    for s_idx, (l, r, water, max_w, calc, decision) in enumerate(steps):
        y_base = -s_idx * row_h
        # histogram
        centers = _draw_histogram(ax, heights, x0=0, y_base=y_base, scale=scale)
        # water rectangle (light blue) sitting ON top of bars
        water_h = min(heights[l], heights[r]) * scale
        water_rect = Rectangle(
            (l - 0.35, y_base), (r - l) + 0.7, water_h,
            facecolor="#bae6fd", edgecolor="#0284c7", linewidth=1.0, alpha=0.7, zorder=3,
        )
        ax.add_patch(water_rect)
        # Pointers — tip exactly at the top of THIS bar
        l_top = y_base + heights[l] * scale
        _draw_inline_pointer(ax, l, l_top, "L", COLOR_LEFT, length=0.7)
        if l != r:
            r_top = y_base + heights[r] * scale
            _draw_inline_pointer(ax, r, r_top, "R", COLOR_RIGHT, length=0.7)
        # Step label (left-side, vertically centered on the bars)
        ax.text(-1.3, y_base + bars_h / 2, f"Paso {s_idx + 1}",
                ha="right", va="center", fontsize=11, fontweight="bold")
        # Note on right
        bg = "#f0fdf4" if water == max_w else "#f9fafb"
        note = f"agua = {calc}\nmax_water = {max_w}\n{decision}"
        draw_note(ax, len(heights) + 0.5, y_base + bars_h / 2, note, bg=bg)

    top = bars_h + pointer_h + 0.5
    bottom = -(n_steps - 1) * row_h - bottom_h - 0.3
    ax.set_xlim(-2.5, len(heights) + 6.5)
    ax.set_ylim(bottom, top)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Largest Container   ·   heights = [2, 7, 8, 3, 7, 6]",
                 fontsize=13, fontweight="bold", pad=12)
    save(fig, "tp-fig-lc-01-trace.png")


# ═══════════════════════════════════════════════════════════════
#  TRIPLET SUM
# ═══════════════════════════════════════════════════════════════

def fig_ts_trace():
    """Triplet sum trace on sorted [-3, -1, 0, 1, 2]. Show outer i with inner left/right."""
    nums = [-3, -1, 0, 1, 2]
    # Each step: (i, left, right, action_text, found_text_or_None)
    steps = [
        (0, 1, 4, "i=0, a=-3, target=3   ·   sum(-1,2)=1 < 3  →  left++",  None),
        (0, 2, 4, "                            sum(0,2)=2 < 3  →  left++", None),
        (0, 3, 4, "                            sum(1,2)=3 ✓",              "[-3, 1, 2]"),
        (1, 2, 4, "i=1, a=-1, target=1   ·   sum(0,2)=2 > 1  →  right--",  None),
        (1, 2, 3, "                            sum(0,1)=1 ✓",              "[-1, 0, 1]"),
        (2, 3, 4, "i=2, a=0, target=0    ·   sum(1,2)=3 > 0  →  right--",  None),
        (3, None, None, "i=3, a=1 > 0  →  break (optimización)",            None),
    ]
    n_steps = len(steps)
    row_h = 3.4   # bigger gap so below-pointers don't bleed into next row
    fig, ax = plt.subplots(figsize=(11.5, 1 + row_h * n_steps * 0.55))
    for s_idx, (i, l, r, note, found) in enumerate(steps):
        y_base = -s_idx * row_h
        hl = {i: COLOR_HIGHLIGHT}
        if found:
            hl[i] = COLOR_MATCH
            if l is not None:
                hl[l] = COLOR_MATCH
            if r is not None:
                hl[r] = COLOR_MATCH
        centers = draw_array(ax, nums, x0=0, y=y_base, highlight=hl, font_size=13)
        # i ABOVE the array (longer arrow to differentiate from L/R)
        draw_pointer(ax, centers[i][0], y_base, "i", COLOR_I, length=0.5)
        # L and R BELOW the array (clear vertical separation)
        if l is not None:
            draw_pointer(ax, centers[l][0], y_base, "L", COLOR_LEFT, above=False, length=0.5)
        if r is not None and r != l:
            draw_pointer(ax, centers[r][0], y_base, "R", COLOR_RIGHT, above=False, length=0.5)
        ax.text(-0.7, y_base, f"P{s_idx + 1}", ha="right", va="center",
                fontsize=10, fontweight="bold")
        bg = "#f0fdf4" if found else "#f9fafb"
        full_note = note
        if found:
            full_note = f"{note}\n→ triplete: {found}"
        draw_note(ax, len(nums) + 0.6, y_base, full_note, bg=bg)
    ax.set_xlim(-2.5, len(nums) + 7.5)
    ax.set_ylim(-(n_steps - 1) * row_h - 2.0, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Triplet Sum   ·   nums = [-3, -1, 0, 1, 2] (sorted)   ·   2 tripletes encontrados",
                 fontsize=12, fontweight="bold", pad=12)
    save(fig, "tp-fig-ts-01-trace.png")


def fig_ts_dedup():
    """Illustrate dedup case: skipping duplicate 'a' values."""
    nums = [-4, -4, -2, 0, 0, 1, 2, 3]
    fig, ax = plt.subplots(figsize=(11, 5))
    # Top row — first instance of -4
    centers = draw_array(ax, nums, x0=0, y=0, highlight={0: COLOR_HIGHLIGHT}, font_size=12)
    draw_pointer(ax, centers[0][0], 0, "i=0, a=-4", COLOR_I, length=0.45)
    ax.text(len(nums) + 0.6, 0,
            "→ triplete: [-4, 1, 3]",
            ha="left", va="center", fontsize=11, color="#047857",
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f0fdf4", edgecolor="#10b981"))

    # Bottom row — second instance of -4 (skipped)
    centers = draw_array(ax, nums, x0=0, y=-2.4, dim=[1], font_size=12)
    draw_pointer(ax, centers[1][0], -2.4, "i=1, a=-4", COLOR_I, length=0.45)
    ax.text(len(nums) + 0.6, -2.4,
            "nums[1] == nums[0]  →  skip\n(generaría el mismo triplete)",
            ha="left", va="center", fontsize=11, color="#b91c1c",
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#fef2f2", edgecolor="#dc2626"))

    ax.set_xlim(-1.5, len(nums) + 7.0)
    ax.set_ylim(-3.6, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Triplet Sum — manejo de duplicados en 'a'",
                 fontsize=13, fontweight="bold", pad=10)
    save(fig, "tp-fig-ts-02-dedup.png")


# ═══════════════════════════════════════════════════════════════
#  SHIFT ZEROS TO THE END
# ═══════════════════════════════════════════════════════════════

def fig_sz_trace():
    """Trace shift_zeros on [0, 1, 0, 3, 2]."""
    states = [
        # (array, left, right, note, swapped?)
        ([0, 1, 0, 3, 2], 0, 0, "right=0, nums[0]=0  →  skip, right++", False),
        ([0, 1, 0, 3, 2], 0, 1, "right=1, nums[1]=1 ≠ 0  →  swap(0,1), left++", True),
        ([1, 0, 0, 3, 2], 1, 2, "right=2, nums[2]=0  →  skip, right++", False),
        ([1, 0, 0, 3, 2], 1, 3, "right=3, nums[3]=3 ≠ 0  →  swap(1,3), left++", True),
        ([1, 3, 0, 0, 2], 2, 4, "right=4, nums[4]=2 ≠ 0  →  swap(2,4), left++", True),
        ([1, 3, 2, 0, 0], 3, 5, "right=5  →  exit (final)", False),
    ]
    n_steps = len(states)
    row_h = 2.6   # enough room for L+R both above
    fig, ax = plt.subplots(figsize=(11, 1 + row_h * n_steps * 0.6))
    for s_idx, (arr, l, r, note, swapped) in enumerate(states):
        y_base = -s_idx * row_h
        hl = {}
        if swapped and r < len(arr) and l < len(arr):
            hl[l] = COLOR_MATCH
            hl[r] = COLOR_MATCH
        centers = draw_array(ax, arr, x0=0, y=y_base, highlight=hl, font_size=13)
        # When L and R are at the SAME column, stack them: L slightly higher
        same_col = (l == r) and l < len(arr) and r < len(arr)
        if l < len(arr):
            l_len = 0.95 if same_col else 0.45
            draw_pointer(ax, centers[l][0], y_base, "L", COLOR_LEFT, length=l_len)
        if r < len(arr) and not same_col:
            draw_pointer(ax, centers[r][0], y_base, "R", COLOR_RIGHT, length=0.45)
        elif r < len(arr) and same_col:
            # Both at same column — R on top of L
            draw_pointer(ax, centers[r][0], y_base, "R", COLOR_RIGHT, length=0.45)
        if r >= len(arr):
            # right past end — show off to the right
            x_end = len(arr) + 0.0
            ax.text(x_end, y_base + 1.0, "R\n(off-end)", ha="center", va="center",
                    fontsize=9, color=COLOR_RIGHT, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                              edgecolor=COLOR_RIGHT, linewidth=1.0))
        ax.text(-0.7, y_base, f"P{s_idx + 1}", ha="right", va="center",
                fontsize=11, fontweight="bold")
        bg = "#f0fdf4" if swapped else "#f9fafb"
        draw_note(ax, len(arr) + 0.6, y_base, note, bg=bg)
    ax.set_xlim(-2.5, 5 + 7.0)
    ax.set_ylim(-(n_steps - 1) * row_h - 1.5, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Shift Zeros to the End   ·   nums = [0, 1, 0, 3, 2]",
                 fontsize=13, fontweight="bold", pad=12)
    save(fig, "tp-fig-sz-01-trace.png")


# ═══════════════════════════════════════════════════════════════
#  NEXT LEXICOGRAPHICAL SEQUENCE
# ═══════════════════════════════════════════════════════════════

def fig_nl_perms():
    """Show permutations of 'abc' in lex order."""
    fig, ax = plt.subplots(figsize=(7, 5))
    perms = ["abc", "acb", "bac", "bca", "cab", "cba"]
    for i, p in enumerate(perms):
        ax.text(0, -i * 0.6, f"{i + 1}.  ", ha="right", va="center",
                fontsize=12, color=COLOR_DIM)
        # Draw cells for each char
        for j, ch in enumerate(p):
            cx = 0.6 + j * 0.7
            cy = -i * 0.6
            rect = FancyBboxPatch(
                (cx - 0.32, cy - 0.27),
                0.64, 0.54,
                boxstyle="round,pad=0.02,rounding_size=0.06",
                linewidth=1.2, edgecolor=COLOR_BOX_EDGE, facecolor=COLOR_BOX,
            )
            ax.add_patch(rect)
            ax.text(cx, cy, ch, ha="center", va="center",
                    fontsize=12, fontweight="bold", color=COLOR_TEXT)
    # Highlight transition: "abc" → "acb"
    arr = FancyArrowPatch(
        (3.5, 0), (3.5, -0.6),
        arrowstyle="-|>", mutation_scale=15,
        color=COLOR_LEFT, linewidth=2, zorder=5,
    )
    ax.add_patch(arr)
    ax.text(3.9, -0.3, "next", ha="left", va="center",
            fontsize=10, fontweight="bold", color=COLOR_LEFT)
    # Wrap-around arrow
    arr = FancyArrowPatch(
        (-0.8, -5 * 0.6), (-0.8, 0),
        arrowstyle="-|>", mutation_scale=12,
        color=COLOR_DIM, linewidth=1.5, linestyle="dashed",
        connectionstyle="arc3,rad=0.5", zorder=3,
    )
    ax.add_patch(arr)
    ax.text(-1.3, -1.5, "wrap", ha="center", va="center",
            fontsize=9, color=COLOR_DIM, style="italic", rotation=90)

    ax.set_xlim(-2, 5)
    ax.set_ylim(-3.5, 0.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Permutaciones de 'abc' en orden lexicográfico",
                 fontsize=13, fontweight="bold", pad=10)
    save(fig, "tp-fig-nl-01-perms.png")


def fig_nl_trace():
    """Trace next-lex on 'abcedda'."""
    s = list("abcedda")
    states = [
        # (array, pivot, rs, note, kind)
        (list("abcedda"), 5, None, "Paso 1: pivot search\n  letters[5]='d' >= [6]='a'  →  pivot--",  "search"),
        (list("abcedda"), 4, None, "  letters[4]='d' >= [5]='d'  →  pivot--", "search"),
        (list("abcedda"), 3, None, "  letters[3]='e' >= [4]='d'  →  pivot--", "search"),
        (list("abcedda"), 2, None, "  letters[2]='c' < [3]='e'  →  STOP. pivot = 2.", "found-pivot"),
        (list("abcedda"), 2, 6, "Paso 2: rightmost successor\n  letters[6]='a' <= 'c'  →  rs--", "search"),
        (list("abcedda"), 2, 5, "  letters[5]='d' > 'c'  →  STOP. rs = 5.", "found-rs"),
        (list("abdedca"), 2, 5, "Paso 3: swap pivot ↔ rs", "swap"),
        (list("abdacde"), 2, 5, "Paso 4: reverse cola desde pivot+1\n  → resultado: 'abdacde'", "reversed"),
    ]
    n_steps = len(states)
    row_h = 2.0
    fig, ax = plt.subplots(figsize=(12, 1 + row_h * n_steps * 0.65))
    for s_idx, (arr, p, rs, note, kind) in enumerate(states):
        y_base = -s_idx * row_h
        hl = {}
        if kind == "found-pivot":
            hl[p] = COLOR_PIVOT
        elif kind == "found-rs":
            hl[p] = COLOR_PIVOT
            hl[rs] = COLOR_RS
        elif kind == "swap":
            hl[p] = COLOR_MATCH
            hl[rs] = COLOR_MATCH
        elif kind == "reversed":
            for k in range(p + 1, len(arr)):
                hl[k] = COLOR_HIGHLIGHT
        centers = draw_array(ax, arr, x0=0, y=y_base, highlight=hl, font_size=13)
        if p is not None:
            draw_pointer(ax, centers[p][0], y_base, "pivot", COLOR_PIVOT, length=0.4)
        if rs is not None:
            draw_pointer(ax, centers[rs][0], y_base, "rs", COLOR_RS, above=False, length=0.4)
        ax.text(-0.7, y_base, f"P{s_idx + 1}", ha="right", va="center",
                fontsize=10, fontweight="bold")
        bg = {
            "search": "#f9fafb",
            "found-pivot": "#ecfdf5",
            "found-rs": "#ecfdf5",
            "swap": "#fef3c7",
            "reversed": "#dbeafe",
        }.get(kind, "#f9fafb")
        draw_note(ax, len(arr) + 0.6, y_base, note, bg=bg)
    ax.set_xlim(-2.5, len(s) + 8.0)
    ax.set_ylim(-(n_steps - 1) * row_h - 1.8, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Next Lexicographical Sequence   ·   s = 'abcedda'  →  'abdacde'",
                 fontsize=12, fontweight="bold", pad=12)
    save(fig, "tp-fig-nl-02-trace.png")


# ═══════════════════════════════════════════════════════════════
#  RUN ALL
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\nIntro:")
    fig_intro_pointer_basics()
    fig_intro_inward()
    fig_intro_unidirectional()
    fig_intro_staged()

    print("\nPair Sum:")
    fig_pair_trace()

    print("\nPalindrome:")
    fig_pal_symmetry()
    fig_pal_trace()

    print("\nLargest Container:")
    fig_lc_trace()

    print("\nTriplet Sum:")
    fig_ts_trace()
    fig_ts_dedup()

    print("\nShift Zeros:")
    fig_sz_trace()

    print("\nNext Lexicographical:")
    fig_nl_perms()
    fig_nl_trace()

    print("\nDone.")

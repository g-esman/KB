"""Generate hash ring diagrams for the Consistent Hashing chapter.

Each function draws a single PNG. Saved to topics/concepts/img/.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyArrowPatch, Arc
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
print(f"Writing PNGs to: {OUT_DIR}")

# Server colors (similar palette to mermaid default)
SERVER_COLORS = {
    "s0": "#a78bfa",  # purple
    "s1": "#7dd3fc",  # cyan
    "s2": "#f9a8d4",  # pink
    "s3": "#fdba74",  # orange
    "s4": "#86efac",  # green
    "s5": "#fcd34d",  # yellow
}


def ang2xy(angle_deg, r=1.0):
    """0 deg = top of circle, increasing clockwise."""
    rad = np.deg2rad(90 - angle_deg)
    return r * np.cos(rad), r * np.sin(rad)


def setup_ax(ax, title=None, span=1.9):
    ax.set_aspect("equal")
    ax.set_xlim(-span, span)
    ax.set_ylim(-span, span)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=15, fontweight="bold", pad=10)


def draw_ring(ax, r=1.0):
    ax.add_patch(Circle((0, 0), r, fill=False, color="#6b7280", linewidth=2))


def draw_server(ax, angle, name, color=None, r=1.0, label_pad=0.28, size=550):
    if color is None:
        color = SERVER_COLORS.get(name.split("_")[0], "#a78bfa")
    x, y = ang2xy(angle, r)
    ax.scatter(x, y, s=size, c=color, edgecolors="black", linewidths=1.5, zorder=5)
    lx, ly = ang2xy(angle, r + label_pad)
    ax.text(lx, ly, name, ha="center", va="center", fontsize=11, fontweight="bold", zorder=6)


def draw_key(ax, angle, name, r=1.0, label_pad=0.20, color="black", size=70):
    x, y = ang2xy(angle, r)
    ax.scatter(x, y, s=size, c=color, zorder=5)
    lx, ly = ang2xy(angle, r + label_pad)
    ax.text(lx, ly, name, ha="center", va="center", fontsize=10, fontweight="bold", color=color, zorder=6)


def draw_clockwise_arrow(ax, from_angle, to_angle, r=1.0, color="#dc2626", linewidth=2):
    """Arc arrow going clockwise on the ring."""
    # Going clockwise on the ring means angle increases in our system (0 top, clockwise)
    # We draw a curved arrow from key position to server position
    fx, fy = ang2xy(from_angle, r)
    tx, ty = ang2xy(to_angle, r)
    # rad negative bends inward
    arrow = FancyArrowPatch(
        (fx, fy),
        (tx, ty),
        connectionstyle="arc3,rad=0.3",
        arrowstyle="-|>",
        mutation_scale=20,
        color=color,
        linewidth=linewidth,
        zorder=4,
    )
    ax.add_patch(arrow)


def draw_arc_highlight(ax, start_angle, end_angle, r=1.0, color="#fde68a", width=0.15):
    """Highlight a section of the ring (between start_angle clockwise to end_angle)."""
    # matplotlib Arc uses theta in degrees with 0 = right, counter-clockwise positive
    # Convert from our convention (0 = top, clockwise)
    # our angle X in deg --> matplotlib theta = 90 - X
    theta_start_mpl = 90 - end_angle
    theta_end_mpl = 90 - start_angle
    # Draw a thicker arc
    ax.add_patch(
        Wedge(
            (0, 0),
            r + width / 2,
            theta_start_mpl,
            theta_end_mpl,
            width=width,
            facecolor=color,
            edgecolor="none",
            zorder=2,
        )
    )


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {name}")


# ───────────────────────────────────────────────────────
# Figure 4 — basic hash ring with x0 marker
# ───────────────────────────────────────────────────────
def fig04_hash_ring():
    fig, ax = plt.subplots(figsize=(5, 5))
    setup_ax(ax)
    draw_ring(ax)
    # x0 / xn marker at top
    ax.scatter(*ang2xy(0), s=120, c="#374151", zorder=5)
    ax.text(0, 1.28, "x0 / xn\n(0 = 2¹⁶⁰−1)", ha="center", va="bottom", fontsize=10, fontweight="bold")
    # Direction arrow (clockwise)
    arc = Arc((0, 0), 1.6, 1.6, theta1=70, theta2=110, color="#6b7280", linewidth=1.5)
    ax.add_patch(arc)
    ax.annotate("", xy=ang2xy(20, 0.8), xytext=ang2xy(40, 0.8), arrowprops=dict(arrowstyle="->", color="#6b7280"))
    ax.text(0.6, 0.55, "clockwise", fontsize=9, color="#6b7280", style="italic")
    save(fig, "ch-fig04-hash-ring.png")


# ───────────────────────────────────────────────────────
# Figure 5 — 4 servers placed on the ring
# ───────────────────────────────────────────────────────
def fig05_servers_on_ring():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    servers = [("s0", 30), ("s1", 130), ("s2", 220), ("s3", 320)]
    for name, ang in servers:
        draw_server(ax, ang, name)
    # Annotation
    ax.text(0, -1.55, "4 servers placed on the hash ring\nvia f(server_ip) → angle", ha="center", fontsize=10, color="#374151")
    save(fig, "ch-fig05-servers-on-ring.png")


# ───────────────────────────────────────────────────────
# Figure 6 — servers + keys on ring (no lookup arrows yet)
# ───────────────────────────────────────────────────────
def fig06_keys_on_ring():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    servers = [("s0", 30), ("s1", 130), ("s2", 220), ("s3", 320)]
    keys = [("k0", 0), ("k1", 90), ("k2", 180), ("k3", 280)]
    for name, ang in servers:
        draw_server(ax, ang, name)
    for name, ang in keys:
        draw_key(ax, ang, name)
    ax.text(0, -1.55, "Keys hashed onto the ring\nf(key) → angle", ha="center", fontsize=10, color="#374151")
    save(fig, "ch-fig06-keys-on-ring.png")


# ───────────────────────────────────────────────────────
# Figure 7 — server lookup (clockwise from each key)
# ───────────────────────────────────────────────────────
def fig07_server_lookup():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    servers = [("s0", 30), ("s1", 130), ("s2", 220), ("s3", 320)]
    keys = [("k0", 0), ("k1", 90), ("k2", 180), ("k3", 280)]
    for name, ang in servers:
        draw_server(ax, ang, name)
    for name, ang in keys:
        draw_key(ax, ang, name)
    # Clockwise lookup arrows
    pairs = [(0, 30), (90, 130), (180, 220), (280, 320)]
    for fa, ta in pairs:
        draw_clockwise_arrow(ax, fa, ta, color="#dc2626")
    ax.text(0, -1.6, "Each key → first server clockwise", ha="center", fontsize=11, fontweight="bold", color="#dc2626")
    save(fig, "ch-fig07-server-lookup.png")


# ───────────────────────────────────────────────────────
# Figure 8 — add a server (s4) — only k0 reassigned
# ───────────────────────────────────────────────────────
def fig08_add_server():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    servers = [("s0", 30), ("s1", 130), ("s2", 220), ("s3", 320), ("s4", 350)]
    keys = [("k0", 0), ("k1", 90), ("k2", 180), ("k3", 280)]
    for name, ang in servers:
        draw_server(ax, ang, name)
    for name, ang in keys:
        draw_key(ax, ang, name)
    # Highlight: s4 added at 350 → captures k0 (which would have gone to s0)
    draw_clockwise_arrow(ax, 0, 350, color="#059669", linewidth=2.5)  # k0 → s4 (new)
    # other keys unchanged
    draw_clockwise_arrow(ax, 90, 130, color="#9ca3af")
    draw_clockwise_arrow(ax, 180, 220, color="#9ca3af")
    draw_clockwise_arrow(ax, 280, 320, color="#9ca3af")
    ax.text(0, -1.6, "s4 added → only k0 moves (to s4)\nothers unchanged", ha="center", fontsize=11, fontweight="bold", color="#059669")
    save(fig, "ch-fig08-add-server.png")


# ───────────────────────────────────────────────────────
# Figure 9 — remove a server (s1) — only k1 reassigned
# ───────────────────────────────────────────────────────
def fig09_remove_server():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    servers = [("s0", 30), ("s2", 220), ("s3", 320)]
    removed_servers = [("s1", 130)]
    keys = [("k0", 0), ("k1", 90), ("k2", 180), ("k3", 280)]
    for name, ang in servers:
        draw_server(ax, ang, name)
    # Removed (greyed out, X)
    for name, ang in removed_servers:
        x, y = ang2xy(ang)
        ax.scatter(x, y, s=550, c="#e5e7eb", edgecolors="#9ca3af", linewidths=1.5, zorder=5)
        ax.text(x, y, "✕", ha="center", va="center", fontsize=14, color="#dc2626", fontweight="bold", zorder=6)
        lx, ly = ang2xy(ang, 1.28)
        ax.text(lx, ly, f"{name}\n(removed)", ha="center", va="center", fontsize=10, color="#9ca3af", zorder=6)
    for name, ang in keys:
        draw_key(ax, ang, name)
    # Lookups
    draw_clockwise_arrow(ax, 0, 30, color="#9ca3af")  # k0 → s0
    draw_clockwise_arrow(ax, 90, 220, color="#dc2626", linewidth=2.5)  # k1 → s2 (changed)
    draw_clockwise_arrow(ax, 180, 220, color="#9ca3af")
    draw_clockwise_arrow(ax, 280, 320, color="#9ca3af")
    ax.text(0, -1.6, "s1 removed → only k1 moves (to s2)\nothers unchanged", ha="center", fontsize=11, fontweight="bold", color="#dc2626")
    save(fig, "ch-fig09-remove-server.png")


# ───────────────────────────────────────────────────────
# Figure 10 — uneven partitions problem
# ───────────────────────────────────────────────────────
def fig10_uneven_partitions():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    # If s1 is removed, s2 covers a huge partition
    servers = [("s0", 30), ("s2", 220), ("s3", 320)]
    for name, ang in servers:
        draw_server(ax, ang, name)
    # Highlight s2's huge partition (from 30 clockwise to 220)
    draw_arc_highlight(ax, 30, 220, color="#fecaca", width=0.18)
    ax.text(*ang2xy(125, 1.45), "s2's partition\n(huge!)", ha="center", va="center", fontsize=10, fontweight="bold", color="#dc2626")
    # Other partitions
    draw_arc_highlight(ax, 220, 320, color="#fde68a", width=0.18)
    draw_arc_highlight(ax, 320, 30 + 360, color="#fde68a", width=0.18)
    ax.text(0, -1.6, "After s1 removal, partitions become uneven\ns2 owns 2× the keyspace of s0 / s3", ha="center", fontsize=10, color="#374151")
    save(fig, "ch-fig10-uneven-partitions.png")


# ───────────────────────────────────────────────────────
# Figure 11 — non-uniform key distribution
# ───────────────────────────────────────────────────────
def fig11_non_uniform_distribution():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    # Servers clustered on top half — s2 owns most
    servers = [("s0", 350), ("s1", 10), ("s2", 30), ("s3", 50)]
    for name, ang in servers:
        draw_server(ax, ang, name)
    # Many keys clustered around the bottom — all assigned to s0 (clockwise)
    key_angles = [70, 100, 130, 160, 190, 220, 250, 280, 310, 340]
    for i, ang in enumerate(key_angles):
        draw_key(ax, ang, f"k{i}")
    ax.text(0, -1.6, "Servers clustered → s0 owns most keys\ns1, s3 nearly empty", ha="center", fontsize=10, color="#dc2626", fontweight="bold")
    save(fig, "ch-fig11-non-uniform-distribution.png")


# ───────────────────────────────────────────────────────
# Figure 12 — virtual nodes (3 vnodes per server, 2 servers)
# ───────────────────────────────────────────────────────
def fig12_virtual_nodes():
    fig, ax = plt.subplots(figsize=(7, 7))
    setup_ax(ax, span=1.85)
    draw_ring(ax)
    # 2 servers with 3 vnodes each, interleaved
    nodes = [
        ("s0_0", 20, "#a78bfa"),
        ("s1_0", 70, "#7dd3fc"),
        ("s0_1", 130, "#a78bfa"),
        ("s1_1", 190, "#7dd3fc"),
        ("s0_2", 250, "#a78bfa"),
        ("s1_2", 310, "#7dd3fc"),
    ]
    # Highlight partitions per server
    for i, (name, ang, color) in enumerate(nodes):
        next_ang = nodes[(i + 1) % len(nodes)][1]
        if next_ang < ang:
            next_ang += 360
        # Color the partition that THIS node owns (from previous node clockwise to this)
        prev_ang = nodes[(i - 1) % len(nodes)][1]
        if ang <= prev_ang:
            start = prev_ang
            end = ang + 360
        else:
            start = prev_ang
            end = ang
        # Use lighter version of color
        light = color + "80"  # ~50% alpha hex (12 ch hex with alpha)
        draw_arc_highlight(ax, start, end, color=light, width=0.13)
    for name, ang, color in nodes:
        draw_server(ax, ang, name, color=color, label_pad=0.32, size=400)
    ax.text(0, -1.75, "Each server has multiple vnodes on the ring\n→ load is balanced; no single huge partition", ha="center", fontsize=10, color="#374151")
    save(fig, "ch-fig12-virtual-nodes.png")


# ───────────────────────────────────────────────────────
# Figure 13 — vnode lookup: k0 → s1_1
# ───────────────────────────────────────────────────────
def fig13_vnode_lookup():
    fig, ax = plt.subplots(figsize=(7, 7))
    setup_ax(ax, span=1.85)
    draw_ring(ax)
    nodes = [
        ("s0_0", 20, "#a78bfa"),
        ("s1_0", 70, "#7dd3fc"),
        ("s0_1", 130, "#a78bfa"),
        ("s1_1", 190, "#7dd3fc"),
        ("s0_2", 250, "#a78bfa"),
        ("s1_2", 310, "#7dd3fc"),
    ]
    for name, ang, color in nodes:
        draw_server(ax, ang, name, color=color, label_pad=0.32, size=400)
    # Place k0 at 160, lookup → s1_1 at 190
    draw_key(ax, 160, "k0")
    draw_clockwise_arrow(ax, 160, 190, color="#dc2626", linewidth=2.5)
    ax.text(0, -1.75, "k0 → first vnode clockwise = s1_1\n(which means → server 1)", ha="center", fontsize=10, color="#dc2626", fontweight="bold")
    save(fig, "ch-fig13-vnode-lookup.png")


# ───────────────────────────────────────────────────────
# Figure 14 — find affected keys when adding s4
# ───────────────────────────────────────────────────────
def fig14_find_affected_add():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    servers = [("s0", 30), ("s1", 130), ("s2", 220), ("s3", 320), ("s4", 350)]
    keys = [("k0", 0), ("k1", 90), ("k2", 180), ("k3", 280)]
    # Highlight affected range: from s3 (320) clockwise to s4 (350) — anticlockwise from s4 to s3
    draw_arc_highlight(ax, 320, 350, color="#fde68a", width=0.18)
    for name, ang in servers:
        draw_server(ax, ang, name)
    for name, ang in keys:
        draw_key(ax, ang, name)
    ax.text(*ang2xy(335, 1.55), "AFFECTED\nrange", ha="center", va="center", fontsize=10, fontweight="bold", color="#b45309")
    ax.text(0, -1.65, "Adding s4 → affected = (s3 → s4]\nKeys in this range move from s0 to s4", ha="center", fontsize=10, color="#374151")
    save(fig, "ch-fig14-find-affected-add.png")


# ───────────────────────────────────────────────────────
# Figure 15 — find affected keys when removing s1
# ───────────────────────────────────────────────────────
def fig15_find_affected_remove():
    fig, ax = plt.subplots(figsize=(6, 6))
    setup_ax(ax, span=1.7)
    draw_ring(ax)
    servers = [("s0", 30), ("s2", 220), ("s3", 320)]
    removed_servers = [("s1", 130)]
    keys = [("k0", 0), ("k1", 90), ("k2", 180), ("k3", 280)]
    # Affected range: from s0 clockwise to s1 (now removed)
    draw_arc_highlight(ax, 30, 130, color="#fde68a", width=0.18)
    for name, ang in servers:
        draw_server(ax, ang, name)
    for name, ang in removed_servers:
        x, y = ang2xy(ang)
        ax.scatter(x, y, s=550, c="#e5e7eb", edgecolors="#9ca3af", linewidths=1.5, zorder=5)
        ax.text(x, y, "✕", ha="center", va="center", fontsize=14, color="#dc2626", fontweight="bold", zorder=6)
        lx, ly = ang2xy(ang, 1.28)
        ax.text(lx, ly, f"{name}\n(removed)", ha="center", va="center", fontsize=10, color="#9ca3af", zorder=6)
    for name, ang in keys:
        draw_key(ax, ang, name)
    ax.text(*ang2xy(80, 1.5), "AFFECTED\nrange", ha="center", va="center", fontsize=10, fontweight="bold", color="#b45309")
    ax.text(0, -1.65, "Removing s1 → affected = (s0 → s1]\nKeys in this range move to s2 (next clockwise)", ha="center", fontsize=10, color="#374151")
    save(fig, "ch-fig15-find-affected-remove.png")


# ───────────────────────────────────────────────────────
# Figures 1 & 2 — rehashing problem (bar charts)
# ───────────────────────────────────────────────────────
def fig01_rehashing_before():
    fig, ax = plt.subplots(figsize=(8, 4))
    keys = [f"key{i}" for i in range(8)]
    hashes = [18358617, 26143584, 18131146, 35863496, 34085809, 27581703, 38164978, 22530351]
    server_idx = [h % 4 for h in hashes]
    colors = ["#a78bfa", "#7dd3fc", "#f9a8d4", "#fdba74"]
    bar_colors = [colors[i] for i in server_idx]
    bars = ax.bar(keys, [1] * 8, color=bar_colors, edgecolor="black")
    for bar, idx in zip(bars, server_idx):
        ax.text(bar.get_x() + bar.get_width() / 2, 0.5, f"server {idx}", ha="center", va="center", fontweight="bold", fontsize=10)
    ax.set_title("hash(key) % 4 — 4 servers", fontsize=13, fontweight="bold")
    ax.set_ylim(0, 1.2)
    ax.set_yticks([])
    legend = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colors]
    ax.legend(legend, [f"server {i}" for i in range(4)], loc="upper right", ncol=4, fontsize=9, frameon=False)
    save(fig, "ch-fig01-rehashing-before.png")


def fig02_rehashing_after():
    fig, ax = plt.subplots(figsize=(8, 4))
    keys = [f"key{i}" for i in range(8)]
    hashes = [18358617, 26143584, 18131146, 35863496, 34085809, 27581703, 38164978, 22530351]
    server_idx_3 = [h % 3 for h in hashes]
    server_idx_4 = [h % 4 for h in hashes]
    colors = ["#a78bfa", "#7dd3fc", "#f9a8d4", "#fdba74"]
    bar_colors = [colors[i] for i in server_idx_3]
    bars = ax.bar(keys, [1] * 8, color=bar_colors, edgecolor="black")
    for bar, idx, was in zip(bars, server_idx_3, server_idx_4):
        ax.text(bar.get_x() + bar.get_width() / 2, 0.5, f"server {idx}", ha="center", va="center", fontweight="bold", fontsize=10)
        # Mark moved keys
        if idx != was:
            ax.text(bar.get_x() + bar.get_width() / 2, 1.05, "moved!", ha="center", va="center", color="#dc2626", fontsize=9, fontweight="bold")
    ax.set_title("hash(key) % 3 — server 1 removed → 7 of 8 keys moved!", fontsize=13, fontweight="bold", color="#dc2626")
    ax.set_ylim(0, 1.2)
    ax.set_yticks([])
    legend = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colors[:3]]
    ax.legend(legend, [f"server {i}" for i in range(3)], loc="upper right", ncol=3, fontsize=9, frameon=False)
    save(fig, "ch-fig02-rehashing-after.png")


if __name__ == "__main__":
    print("Generating consistent hashing diagrams...")
    fig01_rehashing_before()
    fig02_rehashing_after()
    fig04_hash_ring()
    fig05_servers_on_ring()
    fig06_keys_on_ring()
    fig07_server_lookup()
    fig08_add_server()
    fig09_remove_server()
    fig10_uneven_partitions()
    fig11_non_uniform_distribution()
    fig12_virtual_nodes()
    fig13_vnode_lookup()
    fig14_find_affected_add()
    fig15_find_affected_remove()
    print("Done!")

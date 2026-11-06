"""Regenerate og-image.png — the social-share preview card.

Reads data/ivr_sp_index.csv and renders a vintage parchment card showing the
IIVR-SP name, the cumulative nominal appreciation, and a sparkline.
Run from the repo root:  python _build/make_og_image.py
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data", "ivr_sp_index.csv")
OUT = os.path.join(ROOT, "og-image.png")

# palette (matches index.html)
PAPER = "#eef1f5"
CARD = "#ffffff"
INK = "#23282f"
ACCENT = "#012169"
MUTED = "#6c7580"
RULE = "#ccd4dc"

# ---- read series -------------------------------------------------------------
dates, cs = [], []
with open(CSV, newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        dates.append(row["date"])
        cs.append(float(row["cs_sp"]))

nom = cs[-1] / cs[0] - 1.0
span = dates[0][:4] + "\u2013" + dates[-1][:4]

# ---- figure ------------------------------------------------------------------
W, H = 1200, 630
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

# card
card = FancyBboxPatch((44, 44), W - 88, H - 88,
                      boxstyle="round,pad=0,rounding_size=14",
                      linewidth=1.4, edgecolor=RULE, facecolor=CARD)
ax.add_patch(card)
ax.add_patch(plt.Rectangle((44, 44), W - 88, 10, color=ACCENT, zorder=3))

serif = {"family": "serif"}
mono = {"family": "monospace"}

ax.text(92, 548, "HOUSE PRICES \u00b7 S\u00c3O PAULO", color=ACCENT,
        fontsize=15, fontweight="bold", **mono)
ax.text(90, 448, "IIVR-SP", color=INK, fontsize=74, fontweight="bold", **serif)
ax.text(92, 392, "S\u00e3o Paulo Repeat-Sales Housing Index", color=MUTED,
        fontsize=23, fontstyle="italic", **serif)

# headline number
ax.text(92, 250, ("+%.0f%%" % (nom * 100)), color=ACCENT,
        fontsize=92, fontweight="bold", **serif)
ax.text(96, 150, "cumulative nominal appreciation, " + span,
        color=MUTED, fontsize=22, fontstyle="italic", **serif)

# sparkline (right side)
sx0, sx1, sy0, sy1 = 760, 1130, 195, 470
lo, hi = min(cs), max(cs)
n = len(cs)
xs = [sx0 + (sx1 - sx0) * i / (n - 1) for i in range(n)]
ys = [sy0 + (sy1 - sy0) * (v - lo) / (hi - lo) for v in cs]
ax.plot(xs, ys, color=ACCENT, linewidth=3.4, solid_capstyle="round")
ax.plot([xs[-1]], [ys[-1]], "o", color=ACCENT, markersize=9)

ax.text(96, 92, "otaviolmbraga.github.io/sp-housing-index", color=MUTED,
        fontsize=16, **mono)
ax.text(1108, 92, "by Ot\u00e1vio Braga", color=MUTED, fontsize=16,
        ha="right", **mono)

fig.savefig(OUT, facecolor=PAPER)
print("wrote", OUT, "| nominal", "+%.1f%%" % (nom * 100))

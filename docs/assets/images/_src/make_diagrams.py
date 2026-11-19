"""
make_diagrams.py: builds the illustrated "sticky note" diagrams used in docs/concepts/.

Why a script instead of drawing by hand?
  - Every diagram shares one style (colors, notes, icons, arrows), so they look like a set.
  - To fix a typo or change a number, edit the text below and re-run. No design tool needed.
  - Output is SVG: small files, sharp at any zoom, rendered by GitHub like any image.

Run from the repo root (no extra packages needed):
    python3 docs/assets/images/_src/make_diagrams.py

Output: docs/assets/images/01-rag/*.svg and docs/assets/images/02-agentic-ai/*.svg
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
INK = "#1F2937"        # main text and outlines
SOFT = "#4B5563"       # secondary text
PAPER = "#FBF7EF"      # background
ACCENT = "#EA580C"     # orange underline / highlights
GOOD = "#15803D"       # check marks
BAD = "#DC2626"        # crosses

YELLOW, GREEN, BLUE = "#FEF3A0", "#C6F0D2", "#C9E0FB"
PINK, PURPLE, ORANGE = "#FAD2E6", "#E0D9FB", "#FED9B4"


def t(x, y, text, size=16, weight=400, anchor="start", color=INK, font=FONT, italic=False):
    """One or more lines of text. Pass a list for several lines."""
    lines = text if isinstance(text, list) else [text]
    style = ' font-style="italic"' if italic else ""
    if font == MONO:
        style += ' xml:space="preserve"'  # keep code indentation (SVG collapses spaces otherwise)
    out = [f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
           f'fill="{color}" text-anchor="{anchor}"{style}>']
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else round(size * 1.3, 1)
        out.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    out.append("</text>")
    return "".join(out)


def note(x, y, w, h, color, rot=0, tape=True):
    """A sticky note with a soft shadow and a strip of tape on top."""
    cx, cy = x + w / 2, y + h / 2
    g = [f'<g transform="rotate({rot} {cx} {cy})">',
         f'<rect x="{x + 3}" y="{y + 5}" width="{w}" height="{h}" rx="6" fill="#000" opacity="0.08"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{color}" stroke="#00000014"/>']
    if tape:
        g.append(f'<rect x="{cx - 28}" y="{y - 9}" width="56" height="18" rx="2" fill="#E9DFC4" opacity="0.85"/>')
    g.append("</g>")
    return "".join(g)


def badge(x, y, n, r=15, fill="#FFFFFF"):
    """A numbered circle: ① ② ③ ..."""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
            + t(x, y + r * 0.38, str(n), size=r * 1.05, weight=700, anchor="middle"))


def arrow(x1, y1, x2, y2, bend=0, color=INK, dashed=False, width=2.4):
    """Arrow from (x1,y1) to (x2,y2). bend > 0 curves it."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * bend, my + dx * bend
    dash = ' stroke-dasharray="6 6"' if dashed else ""
    return (f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round"{dash} marker-end="url(#head)"/>')


def check(x, y, s=1.0, color=GOOD):
    return (f'<circle cx="{x}" cy="{y}" r="{13 * s}" fill="{color}"/>'
            f'<path d="M{x - 6 * s},{y} l{4.5 * s},{5 * s} l{8 * s},{-10 * s}" fill="none" '
            f'stroke="#fff" stroke-width="{3 * s}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(x, y, s=1.0, color=BAD):
    return (f'<circle cx="{x}" cy="{y}" r="{13 * s}" fill="{color}"/>'
            f'<path d="M{x - 5 * s},{y - 5 * s} l{10 * s},{10 * s} M{x + 5 * s},{y - 5 * s} l{-10 * s},{10 * s}" '
            f'stroke="#fff" stroke-width="{3 * s}" stroke-linecap="round"/>')


def warn(x, y, s=1.0):
    return (f'<circle cx="{x}" cy="{y}" r="{13 * s}" fill="#D97706"/>'
            + t(x, y + 6 * s, "!", size=18 * s, weight=800, anchor="middle", color="#fff"))


def pill(x, y, text, fill="#FFFFFF", size=14, color=INK, font=FONT, pad=10, stroke=INK):
    """A rounded label. Width is estimated from the text length."""
    w = len(text) * size * (0.62 if font == MONO else 0.56) + pad * 2
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 12}" rx="{(size + 12) / 2}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
            + t(x + w / 2, y + size + 3, text, size=size, anchor="middle", color=color, font=font)), w


def underline(x, y, w):
    """Hand-drawn style orange underline."""
    return (f'<path d="M{x},{y} C{x + w * 0.3},{y - 4} {x + w * 0.7},{y + 4} {x + w},{y - 1}" '
            f'fill="none" stroke="{ACCENT}" stroke-width="4" stroke-linecap="round"/>')


def title(w, text, sub=None):
    out = t(w / 2, 52, text, size=30, weight=800, anchor="middle")
    tw = len(text) * 30 * 0.56
    out += underline(w / 2 - tw / 2, 64, tw)
    if sub:
        out += t(w / 2, 94, sub, size=16, anchor="middle", color=SOFT)
    return out


def svg(w, h, body, name, folder, alt):
    defs = ('<defs><marker id="head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/>'
            '</marker></defs>')
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
           f'role="img" aria-label="{escape(alt)}"><title>{escape(alt)}</title>{defs}'
           f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="20" fill="{PAPER}" stroke="#E7DFD0" stroke-width="2"/>'
           f'{body}</svg>\n')
    path = OUT / folder / f"{name}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")
    print("wrote", path.relative_to(OUT.parents[1]))


# ---------------------------------------------------------------------------
# Icons (simple line drawings; (x, y) = center, s = scale)
# ---------------------------------------------------------------------------
def _stroke(extra=""):
    return f'fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" {extra}'


def i_doc(x, y, s=1.0, fill="#FFFFFF"):
    w, h = 30 * s, 38 * s
    l, tp = x - w / 2, y - h / 2
    return (f'<path d="M{l},{tp} h{w * 0.65} l{w * 0.35},{w * 0.35} v{h - w * 0.35} h{-w} z" fill="{fill}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="M{l + 6 * s},{tp + 16 * s} h{w - 12 * s} M{l + 6 * s},{tp + 23 * s} h{w - 12 * s} M{l + 6 * s},{tp + 30 * s} h{w - 18 * s}" {_stroke()}/>')


def i_scissors(x, y, s=1.0):
    return (f'<circle cx="{x - 9 * s}" cy="{y + 10 * s}" r="{6 * s}" {_stroke()}/>'
            f'<circle cx="{x + 9 * s}" cy="{y + 10 * s}" r="{6 * s}" {_stroke()}/>'
            f'<path d="M{x - 5 * s},{y + 5 * s} L{x + 10 * s},{y - 16 * s} M{x + 5 * s},{y + 5 * s} L{x - 10 * s},{y - 16 * s}" {_stroke()}/>')


def i_numbers(x, y, s=1.0):
    return t(x, y + 5 * s, "[0.12, -0.4, …]", size=13 * s, anchor="middle", font=MONO, weight=600)


def i_db(x, y, s=1.0, fill="#FFFFFF"):
    w, h = 34 * s, 36 * s
    l, tp = x - w / 2, y - h / 2
    ry = 6 * s
    return (f'<path d="M{l},{tp + ry} v{h - 2 * ry} a{w / 2},{ry} 0 0 0 {w},0 v{-(h - 2 * ry)}" fill="{fill}" stroke="{INK}" stroke-width="2.2"/>'
            f'<ellipse cx="{x}" cy="{tp + ry}" rx="{w / 2}" ry="{ry}" fill="{fill}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{l},{y + 1 * s} a{w / 2},{ry} 0 0 0 {w},0" {_stroke()}/>')


def i_search(x, y, s=1.0):
    return (f'<circle cx="{x - 4 * s}" cy="{y - 4 * s}" r="{11 * s}" fill="#FFFFFF" stroke="{INK}" stroke-width="2.4"/>'
            f'<path d="M{x + 4 * s},{y + 4 * s} l{11 * s},{11 * s}" {_stroke("stroke-width=\"4\"")}/>')


def i_chat(x, y, s=1.0, fill="#FFFFFF"):
    return (f'<path d="M{x - 18 * s},{y - 14 * s} h{36 * s} a4,4 0 0 1 4,4 v{18 * s} a4,4 0 0 1 -4,4 h{-24 * s} l{-8 * s},{8 * s} v{-8 * s} h{-4 * s} a4,4 0 0 1 -4,-4 v{-18 * s} a4,4 0 0 1 4,-4 z" fill="{fill}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            + t(x, y + 3 * s, "?", size=16 * s, weight=800, anchor="middle"))


def i_spark(x, y, s=1.0, fill="#FDE047"):
    p = []
    for cx, cy, r in ((x, y, 14 * s), (x + 15 * s, y - 12 * s, 6 * s)):
        p.append(f'<path d="M{cx},{cy - r} Q{cx},{cy} {cx + r},{cy} Q{cx},{cy} {cx},{cy + r} Q{cx},{cy} {cx - r},{cy} Q{cx},{cy} {cx},{cy - r} z" fill="{fill}" stroke="{INK}" stroke-width="2"/>')
    return "".join(p)


def i_plus_doc(x, y, s=1.0):
    return i_doc(x - 8 * s, y, s * 0.85) + (f'<circle cx="{x + 12 * s}" cy="{y + 10 * s}" r="{9 * s}" fill="{ACCENT}"/>'
                                           f'<path d="M{x + 12 * s},{y + 5 * s} v{10 * s} M{x + 7 * s},{y + 10 * s} h{10 * s}" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>')


def i_bulb(x, y, s=1.0):
    return (f'<path d="M{x - 7 * s},{y + 8 * s} C{x - 18 * s},{y - 2 * s} {x - 12 * s},{y - 20 * s} {x},{y - 20 * s} C{x + 12 * s},{y - 20 * s} {x + 18 * s},{y - 2 * s} {x + 7 * s},{y + 8 * s} z" fill="#FDE047" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="M{x - 6 * s},{y + 13 * s} h{12 * s} M{x - 4 * s},{y + 18 * s} h{8 * s}" {_stroke()}/>')


def i_wrench(x, y, s=1.0):
    """A gear: the 'tools' icon."""
    import math
    teeth = "".join(
        f'<rect x="{x - 4 * s}" y="{y - 19 * s}" width="{8 * s}" height="{9 * s}" rx="1.5" fill="#FFFFFF" '
        f'stroke="{INK}" stroke-width="2" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 45))
    del math
    return (teeth + f'<circle cx="{x}" cy="{y}" r="{12 * s}" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2"/>'
            f'<circle cx="{x}" cy="{y}" r="{4.5 * s}" fill="none" stroke="{INK}" stroke-width="2.2"/>')


def i_eye(x, y, s=1.0):
    return (f'<path d="M{x - 20 * s},{y} Q{x},{y - 18 * s} {x + 20 * s},{y} Q{x},{y + 18 * s} {x - 20 * s},{y} z" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2"/>'
            f'<circle cx="{x}" cy="{y}" r="{6 * s}" fill="{INK}"/>')


def i_brain(x, y, s=1.0, fill="#FBCFE8"):
    return (f'<path d="M{x},{y - 16 * s} C{x - 10 * s},{y - 22 * s} {x - 24 * s},{y - 12 * s} {x - 18 * s},{y - 2 * s} C{x - 26 * s},{y + 6 * s} {x - 14 * s},{y + 20 * s} {x},{y + 14 * s} '
            f'C{x + 14 * s},{y + 20 * s} {x + 26 * s},{y + 6 * s} {x + 18 * s},{y - 2 * s} C{x + 24 * s},{y - 12 * s} {x + 10 * s},{y - 22 * s} {x},{y - 16 * s} z" fill="{fill}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x},{y - 16 * s} V{y + 14 * s} M{x - 10 * s},{y - 4 * s} q5,4 10,0 M{x + 10 * s},{y + 4 * s} q-5,-4 -10,0" {_stroke()}/>')


def i_scroll(x, y, s=1.0):
    return (f'<rect x="{x - 15 * s}" y="{y - 18 * s}" width="{30 * s}" height="{36 * s}" rx="3" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x - 9 * s},{y - 9 * s} h{18 * s} M{x - 9 * s},{y - 2 * s} h{18 * s} M{x - 9 * s},{y + 5 * s} h{12 * s}" {_stroke()}/>'
            f'<path d="M{x + 5 * s},{y + 13 * s} l{3 * s},{3 * s} l{6 * s},{-7 * s}" {_stroke(f"stroke=\"{GOOD}\"")}/>')


def i_box(x, y, s=1.0):
    return (f'<rect x="{x - 18 * s}" y="{y - 12 * s}" width="{36 * s}" height="{26 * s}" rx="3" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x - 18 * s},{y - 4 * s} h{36 * s} M{x - 4 * s},{y - 12 * s} v{8 * s} M{x + 4 * s},{y - 12 * s} v{8 * s}" {_stroke()}/>')


def i_map(x, y, s=1.0):
    return (f'<path d="M{x - 18 * s},{y - 12 * s} l{12 * s},{-4 * s} l{12 * s},{4 * s} l{12 * s},{-4 * s} v{28 * s} l{-12 * s},{4 * s} l{-12 * s},{-4 * s} l{-12 * s},{4 * s} z" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="M{x - 6 * s},{y - 16 * s} v{28 * s} M{x + 6 * s},{y - 12 * s} v{28 * s}" {_stroke()}/>')


def i_shield(x, y, s=1.0):
    return (f'<path d="M{x},{y - 18 * s} l{15 * s},{6 * s} v{9 * s} c0,{10 * s} {-7 * s},{16 * s} {-15 * s},{19 * s} c{-8 * s},{-3 * s} {-15 * s},{-9 * s} {-15 * s},{-19 * s} v{-9 * s} z" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="M{x - 6 * s},{y} l{4 * s},{5 * s} l{8 * s},{-9 * s}" {_stroke(f"stroke=\"{GOOD}\"")}/>')


def i_book(x, y, s=1.0):
    return (f'<path d="M{x},{y - 12 * s} C{x - 8 * s},{y - 18 * s} {x - 18 * s},{y - 16 * s} {x - 20 * s},{y - 14 * s} v{26 * s} c{4 * s},{-3 * s} {13 * s},{-3 * s} {20 * s},{3 * s} '
            f'c{7 * s},{-6 * s} {16 * s},{-6 * s} {20 * s},{-3 * s} v{-26 * s} C{x + 18 * s},{y - 16 * s} {x + 8 * s},{y - 18 * s} {x},{y - 12 * s} z M{x},{y - 12 * s} v{27 * s}" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>')


def i_code(x, y, s=1.0):
    return (f'<rect x="{x - 20 * s}" y="{y - 15 * s}" width="{40 * s}" height="{30 * s}" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2"/>'
            + t(x, y + 5 * s, "</>", size=14 * s, weight=800, anchor="middle", font=MONO))


def i_table(x, y, s=1.0):
    return (f'<rect x="{x - 18 * s}" y="{y - 14 * s}" width="{36 * s}" height="{28 * s}" rx="3" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x - 18 * s},{y - 5 * s} h{36 * s} M{x - 18 * s},{y + 4 * s} h{36 * s} M{x - 6 * s},{y - 14 * s} v{28 * s} M{x + 6 * s},{y - 14 * s} v{28 * s}" {_stroke("stroke-width=\"1.6\"")}/>')


def i_plug(x, y, s=1.0):
    return (f'<path d="M{x - 6 * s},{y - 18 * s} v{8 * s} M{x + 6 * s},{y - 18 * s} v{8 * s}" {_stroke("stroke-width=\"3\"")}/>'
            f'<path d="M{x - 13 * s},{y - 10 * s} h{26 * s} v{8 * s} a{13 * s},{12 * s} 0 0 1 {-26 * s},0 z" fill="#FFFFFF" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x},{y + 10 * s} v{8 * s}" {_stroke("stroke-width=\"3\"")}/>')


def i_stack(x, y, s=1.0):
    p = ""
    for i in range(3):
        p += i_doc(x - 8 * s + i * 8 * s, y - 6 * s + i * 6 * s, s * 0.8)
    return p


# ---------------------------------------------------------------------------
# Diagrams: RAG
# ---------------------------------------------------------------------------
def rag_overview():
    W, H = 1100, 660
    b = title(W, "RAG in 2 steps", "Prepare your data once. Then answer every question with the right pieces.")

    def row(y, label, label_color, steps, colors):
        out = t(60, y - 14, label, size=17, weight=800, color=label_color)
        xs = [60, 320, 580, 840]
        for i, ((head, line, icon), col, x) in enumerate(zip(steps, colors, xs)):
            out += note(x, y, 200, 170, col, rot=(-1.2, 0.8, -0.6, 1.0)[i])
            out += badge(x + 26, y + 28, i + 1)
            out += icon(x + 100, y + 72)
            out += t(x + 100, y + 125, head, size=18, weight=700, anchor="middle")
            out += t(x + 100, y + 148, line, size=13.5, anchor="middle", color=SOFT)
            if i < 3:
                out += arrow(x + 208, y + 85, x + 252, y + 85)
        return out

    b += row(150, "STEP 1 · PREPARE  (once, before any question)", ACCENT, [
        ("Documents", "files, PDFs, code", i_stack),
        ("Chunk", "cut into small pieces", i_scissors),
        ("Embed", "each piece → numbers", i_numbers),
        ("Store", "in a vector database", i_db),
    ], [YELLOW, GREEN, BLUE, PURPLE])
    b += row(420, "STEP 2 · ANSWER  (every question)", ACCENT, [
        ("Question", "turned into numbers too", i_chat),
        ("Find k closest", "most similar pieces", i_search),
        ("Add to prompt", "question + those pieces", i_plus_doc),
        ("LLM answers", "using the pieces", i_spark),
    ], [PINK, YELLOW, GREEN, BLUE])
    # link the database to the search step
    b += arrow(940, 330, 420, 418, bend=0.12, dashed=True, color=SOFT)
    b += t(700, 372, "search the stored pieces", size=14, anchor="middle", color=SOFT, italic=True)
    b += t(W / 2, 636, "R = Retrieve the right pieces  ·  A = Augment the prompt with them  ·  G = Generate the answer",
           size=16, weight=600, anchor="middle")
    svg(W, H, b, "rag-overview", "01-rag", "RAG in two steps: prepare the data once (documents, chunk, embed, store), then answer each question (question, find k closest, add to prompt, LLM answers).")


def with_without_rag():
    W, H = 1100, 560
    b = title(W, "Without RAG vs. With RAG", 'Question: "How many tasks can a free user create?"')

    # left: closed book
    b += note(50, 130, 470, 390, PINK, rot=-0.8)
    b += cross(90, 168)
    b += t(115, 175, "Without RAG  ·  closed-book exam", size=19, weight=800)
    b += i_chat(130, 255) + arrow(165, 255, 225, 255) + i_brain(270, 255) + t(270, 300, "LLM", size=14, weight=700, anchor="middle")
    b += arrow(305, 255, 365, 255)
    b += note(370, 210, 130, 95, "#FFFFFF", rot=1.5, tape=False)
    b += t(435, 240, ['"Usually', 'around 5–10,', 'depends on…"'], size=14, anchor="middle", italic=True)
    b += t(80, 365, ["• Only knows its training data", "• Never saw YOUR code", "• So it guesses, confidently"], size=16)
    b += t(80, 470, "Result: a hallucination", size=17, weight=800, color=BAD)

    # right: open book
    b += note(580, 130, 470, 390, GREEN, rot=0.8)
    b += check(620, 168)
    b += t(645, 175, "With RAG  ·  open-book exam", size=19, weight=800)
    b += i_chat(630, 255) + arrow(663, 255, 690, 255)
    b += i_search(715, 255) + t(715, 300, "search", size=14, weight=700, anchor="middle")
    b += arrow(742, 255, 770, 255)
    b += i_doc(795, 255, fill=YELLOW) + t(795, 300, "billing.py", size=13, weight=700, anchor="middle", font=MONO)
    b += arrow(818, 255, 846, 255)
    b += i_brain(880, 255) + t(880, 300, "LLM", size=14, weight=700, anchor="middle")
    b += arrow(912, 255, 935, 255)
    b += note(940, 210, 98, 95, "#FFFFFF", rot=-1.5, tape=False)
    b += t(989, 240, ['"10 tasks', '(TASK_LIMITS,', 'billing.py)"'], size=12.5, anchor="middle", italic=True)
    b += t(610, 365, ["• Looks up the code first", "• Answers from what it found", "• Can show where it came from"], size=16)
    b += t(610, 470, "Result: grounded and cited", size=17, weight=800, color=GOOD)
    svg(W, H, b, "with-without-rag", "01-rag", "Without RAG the LLM guesses the free plan limit; with RAG it searches billing.py first and answers 10 tasks with a citation.")


def chunking():
    W, H = 1100, 640
    b = title(W, "Chunking: cut documents into pieces", "So search can return just the part that answers the question.")

    # big file
    b += note(60, 140, 230, 300, "#FFFFFF", rot=-1)
    b += t(175, 172, "billing.py", size=17, weight=800, anchor="middle", font=MONO)
    for i, (lbl, col) in enumerate([("imports", "#E5E7EB"), ("class PlanTier", "#E5E7EB"), ("TASK_LIMITS", YELLOW),
                                    ("get_plan()", "#E5E7EB"), ("check_task_limit()", ORANGE), ("usage_summary()", "#E5E7EB")]):
        b += f'<rect x="85" y="{190 + i * 40}" width="180" height="30" rx="4" fill="{col}"/>'
        b += t(175, 210 + i * 40, lbl, size=13, anchor="middle", font=MONO)
    b += t(175, 470, ["1 file = many topics", "(59 lines)"], size=14, anchor="middle", color=SOFT)

    # scissors
    b += i_scissors(345, 285, 1.3) + arrow(310, 330, 385, 330)
    b += t(345, 365, "chunk_size", size=14, weight=700, anchor="middle", font=MONO)

    # chunks
    chunks = [("imports", "#F3F4F6"), ("class PlanTier", "#F3F4F6"), ("def get_plan(…)", "#F3F4F6"),
              ("TASK_LIMITS = {FREE: 10…", YELLOW), ("def check_task_limit(…)", ORANGE), ("if current_count >= limit", ORANGE)]
    for i, (lbl, col) in enumerate(chunks):
        x, y = 420 + (i % 2) * 230, 150 + (i // 2) * 95
        b += note(x, y, 210, 70, col, rot=(-1.5, 1.2, 0.8, -1, 1.4, -0.7)[i], tape=False)
        b += t(x + 105, y + 42, lbl, size=13, anchor="middle", font=MONO)
    b += t(650, 455, "6 small pieces, each about ONE thing", size=15, weight=700, anchor="middle")

    # question
    b += note(900, 180, 170, 170, PINK, rot=1.5)
    b += i_chat(985, 230)
    b += t(985, 285, ['"What is the', 'free plan limit?"'], size=14, anchor="middle", italic=True)
    b += arrow(898, 290, 868, 282)
    b += t(985, 395, ["this piece is", "the best match ✓"], size=14, weight=700, anchor="middle", color=GOOD)

    # why strip
    whys = [("Precise", "1 piece = 1 topic, so it matches well"), ("Fits the model", "embedders read ~256 tokens max"),
            ("Cheaper", "send pieces, not whole files"), ("Citable", '"found in check_task_limit"')]
    for i, (h, d) in enumerate(whys):
        x = 60 + i * 255
        b += note(x, 510, 235, 100, (GREEN, BLUE, YELLOW, PURPLE)[i], rot=(-0.8, 0.6, -0.5, 0.9)[i], tape=False)
        b += badge(x + 24, 538, i + 1, r=13)
        b += t(x + 45, 544, h, size=16, weight=800)
        b += t(x + 18, 585, d, size=13, color=SOFT)
    svg(W, H, b, "chunking", "01-rag", "Chunking cuts billing.py into small pieces, each about one topic; a question about the free plan limit returns only the TASK_LIMITS piece. Four reasons: precise, fits the model, cheaper, citable.")


def overlap():
    W, H = 1100, 450
    b = title(W, "Why overlap?", "Neighbouring chunks share a little text, so an idea on the border isn't cut in half.")
    # no overlap
    b += t(60, 160, "No overlap", size=18, weight=800)
    b += cross(200, 154, 0.8)
    b += f'<rect x="60" y="180" width="480" height="60" rx="6" fill="{BLUE}"/><rect x="540" y="180" width="500" height="60" rx="6" fill="{GREEN}"/>'
    b += f'<path d="M540,170 v80" stroke="{BAD}" stroke-width="3" stroke-dasharray="5 4"/>'
    b += t(300, 216, "chunk A: …limit = TASK_LIMITS.get(plan)", size=14, anchor="middle", font=MONO)
    b += t(790, 216, "chunk B: current_count = … if >= limit", size=14, anchor="middle", font=MONO)
    b += t(550, 270, '"limit" is set in A but used in B: neither chunk has the whole check', size=14, anchor="middle", color=BAD, weight=600)
    # with overlap
    b += t(60, 345, "With overlap", size=18, weight=800)
    b += check(215, 339, 0.8)
    b += f'<rect x="250" y="335" width="440" height="34" rx="6" fill="{BLUE}" opacity="0.9"/><rect x="560" y="375" width="480" height="34" rx="6" fill="{GREEN}" opacity="0.9"/>'
    b += f'<rect x="560" y="335" width="130" height="74" rx="6" fill="none" stroke="{ACCENT}" stroke-width="3"/>'
    b += t(405, 357, "chunk A", size=14, anchor="middle", font=MONO) + t(870, 397, "chunk B", size=14, anchor="middle", font=MONO)
    b += t(625, 326, "shared text: the whole check is in one chunk", size=13, weight=700, anchor="middle", color=ACCENT)
    svg(W, H, b, "overlap", "01-rag", "Without overlap a check is split between two chunks; with overlap the border text appears in both chunks.")


def embeddings():
    W, H = 1100, 620
    b = title(W, "Embeddings: text → numbers → a map of meaning", "Similar meaning ends up close together.")

    # left: text -> model -> numbers
    rows = [('"puppy"', "[0.81, 0.10, …]", PINK), ('"car"', "[-0.20, 0.92, …]", BLUE), ('"free plan limit"', "[0.05, -0.33, …]", YELLOW)]
    for i, (txt, vec, col) in enumerate(rows):
        y = 160 + i * 110
        b += note(50, y, 170, 60, col, rot=(-1, 1, -0.6)[i], tape=False)
        b += t(135, y + 37, txt, size=15, weight=700, anchor="middle")
        b += arrow(225, y + 30, 290, y + 30)
        b += note(400, y, 190, 60, "#FFFFFF", rot=(0.8, -0.8, 0.6)[i], tape=False)
        b += t(495, y + 37, vec, size=13, anchor="middle", font=MONO)
    b += note(290, 170, 100, 270, PURPLE, rot=0)
    b += t(340, 280, ["embedding", "model"], size=14, weight=800, anchor="middle")
    b += t(340, 360, ["MiniLM", "384", "numbers"], size=12.5, anchor="middle", color=SOFT)
    for i in range(3):
        y = 160 + i * 110 + 30
        b += arrow(390, y, 398, y)
    b += t(320, 520, ["The SAME model must embed both", "the chunks and the question."], size=15, weight=700, anchor="middle", color=ACCENT)

    # right: the map
    mx, my, mw, mh = 640, 130, 420, 440
    b += f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="14" fill="#FFFFFF" stroke="#D6CFC0" stroke-width="2"/>'
    for gx in range(1, 6):
        b += f'<path d="M{mx + gx * mw / 6},{my + 10} v{mh - 20}" stroke="#F1ECE2"/>'
    for gy in range(1, 6):
        b += f'<path d="M{mx + 10},{my + gy * mh / 6} h{mw - 20}" stroke="#F1ECE2"/>'
    b += t(mx + mw / 2, my + 28, "the meaning map", size=15, weight=700, anchor="middle", color=SOFT)

    def dot(x, y, lbl, col):
        return f'<circle cx="{x}" cy="{y}" r="8" fill="{col}" stroke="{INK}" stroke-width="1.6"/>' + t(x + 14, y + 5, lbl, size=13.5)

    b += f'<ellipse cx="{mx + 105}" cy="{my + 110}" rx="90" ry="55" fill="{PINK}" opacity="0.55"/>'
    b += dot(mx + 60, my + 90, "dog", PINK) + dot(mx + 85, my + 125, "puppy", PINK) + dot(mx + 55, my + 145, "pet", PINK)
    b += f'<ellipse cx="{mx + 320}" cy="{my + 115}" rx="80" ry="50" fill="{BLUE}" opacity="0.55"/>'
    b += dot(mx + 280, my + 100, "car", BLUE) + dot(mx + 300, my + 140, "vehicle", BLUE)
    b += f'<ellipse cx="{mx + 230}" cy="{my + 320}" rx="150" ry="80" fill="{YELLOW}" opacity="0.7"/>'
    b += dot(mx + 120, my + 290, "TASK_LIMITS chunk", YELLOW) + dot(mx + 150, my + 345, "check_task_limit chunk", YELLOW)
    b += dot(mx + 260, my + 300, "billing plan", YELLOW)
    # question star
    qx, qy = mx + 200, my + 250
    b += i_spark(qx, qy, 0.9, fill=ACCENT)
    b += t(qx + 22, qy - 14, "your question", size=13.5, weight=800, color=ACCENT)
    b += f'<circle cx="{qx - 30}" cy="{qy + 65}" r="95" fill="none" stroke="{ACCENT}" stroke-width="2.5" stroke-dasharray="7 6"/>'
    b += t(mx + mw / 2, my + mh - 16, "search = take the k dots closest to the question", size=14, weight=700, anchor="middle")
    svg(W, H, b, "embeddings", "01-rag", "An embedding model turns each text into a list of numbers; on the resulting meaning map, similar texts sit close together and the question lands near the billing chunks.")


def chunk_k_grid():
    W, H = 1100, 760
    b = title(W, "Chunk size × k: the 4 combinations", "k = how many pieces come back   ·   chunk size = how big each piece is")

    b += t(445, 140, "SMALL k  (e.g. 2)", size=17, weight=800, anchor="middle")
    b += t(835, 140, "BIG k  (e.g. 10)", size=17, weight=800, anchor="middle")
    b += t(120, 260, ["SMALL", "chunks", "(256)"], size=17, weight=800, anchor="middle")
    b += t(120, 500, ["BIG", "chunks", "(1024)"], size=17, weight=800, anchor="middle")

    def blocks(x, y, n, w, h, col, gap=6, per_row=10):
        out = ""
        for i in range(n):
            r, c = divmod(i, per_row)
            out += f'<rect x="{x + c * (w + gap)}" y="{y + r * (h + gap)}" width="{w}" height="{h}" rx="3" fill="{col}" stroke="{INK}" stroke-width="1.4"/>'
        return out

    def missing(x, y, n):
        return "".join(f'<rect x="{x + i * 32}" y="{y}" width="26" height="26" rx="3" fill="none" '
                       f'stroke="#9CA3AF" stroke-width="1.6" stroke-dasharray="4 3"/>' for i in range(n))

    cells = [
        (250, 160, PINK, cross, "Too little", ["Answer comes back in fragments.", "Parts are missing → incomplete,", "or the LLM guesses the rest."],
         blocks(290, 225, 2, 26, 26, "#FFFFFF") + missing(354, 225, 2) + t(420, 244, "missing pieces", size=12.5, color=SOFT, italic=True),
         "≈ 2 × 80 tokens"),
        (640, 160, GREEN, check, "Many precise pieces", ["Small focused pieces that together", "cover the answer.", "A few unrelated pieces too."],
         blocks(680, 225, 10, 26, 26, "#FFFFFF"), "≈ 10 × 80 tokens"),
        (250, 400, GREEN, check, "Whole units", ["Full functions, nothing cut in half.", "But a 3rd file is never seen,", "and matching gets blurrier."],
         blocks(290, 465, 2, 140, 26, "#FFFFFF", per_row=2), "≈ 2 × 280 tokens"),
        (640, 400, PINK, cross, "Too much", ["The answer is in there, buried", "in noise. Slow, costly, and the", "LLM may quote the wrong code."],
         blocks(680, 461, 10, 52, 13, "#FFFFFF", gap=4, per_row=5), "≈ 10 × 280 tokens"),
    ]
    for i, (x, y, col, mark, head, lines, vis, cost) in enumerate(cells):
        b += note(x, y, 370, 215, col, rot=(-0.8, 0.7, 0.6, -0.7)[i])
        b += mark(x + 30, y + 34)
        b += t(x + 54, y + 41, head, size=19, weight=800)
        b += vis
        b += t(x + 345, y + 200, cost, size=12.5, anchor="end", color=SOFT, italic=True)
        b += t(x + 22, y + 125, lines, size=14.5)

    b += note(150, 650, 800, 80, YELLOW, rot=-0.4)
    b += t(550, 683, "Rule of thumb:  small chunks → need a bigger k   ·   big chunks → can use a smaller k", size=17, weight=800, anchor="middle")
    b += t(550, 711, "Then measure: pick the SMALLEST settings that still find the answer.", size=15, anchor="middle", color=SOFT)
    svg(W, H, b, "chunk-size-and-k", "01-rag", "Four combinations: small chunks and small k gives fragments; small chunks and big k gives many precise pieces; big chunks and small k gives whole units; big chunks and big k is too much. Rule: small chunks need a bigger k.")


def k_vs_tokens():
    W, H = 1100, 560
    b = title(W, "k, chunk size and tokens are NOT the same", "Three different things, measured in three different units.")
    cards = [
        (BLUE, "k", "HOW MANY chunks come back", "unit: chunks", "k = 3", "you choose it in code"),
        (YELLOW, "chunk_size", "HOW BIG each chunk is", "unit: characters (in our code)", "256 characters", "you choose it in code"),
        (PINK, "tokens", "pieces of text the LLM reads", "unit: tokens (~4 chars each)", "[free] [ user] [ limit]", "the tokenizer decides"),
    ]
    for i, (col, name, what, unit, ex, who) in enumerate(cards):
        x = 60 + i * 340
        b += note(x, 130, 300, 250, col, rot=(-1, 0.6, -0.5)[i])
        b += badge(x + 30, 162, i + 1)
        b += t(x + 150, 210, name, size=26, weight=800, anchor="middle", font=MONO)
        b += t(x + 150, 245, what, size=15, weight=700, anchor="middle")
        b += t(x + 150, 272, unit, size=13.5, anchor="middle", color=SOFT)
        b += f'<rect x="{x + 30}" y="{290}" width="240" height="40" rx="8" fill="#FFFFFF" stroke="#00000020"/>'
        b += t(x + 150, 316, ex, size=15, weight=700, anchor="middle", font=MONO)
        b += t(x + 150, 358, who, size=13.5, anchor="middle", color=SOFT, italic=True)

    b += note(110, 420, 880, 110, "#FFFFFF", rot=0.3)
    b += t(550, 458, "tokens sent to the LLM  ≈  k  ×  tokens per chunk", size=21, weight=800, anchor="middle", font=MONO)
    b += t(550, 492, "example:  k = 5 chunks  ×  ~80 tokens each (256 chars of code)  =  ~400 tokens", size=15, anchor="middle")
    b += t(550, 516, "Library analogy: k = how many BOOKS you take · tokens = how many WORDS are inside them", size=14, anchor="middle", color=SOFT, italic=True)
    svg(W, H, b, "k-chunk-size-tokens", "01-rag", "k is how many chunks come back, chunk size is how big each chunk is in characters, tokens are the text pieces the LLM reads. Tokens sent is roughly k times tokens per chunk.")


def where_answer_lives():
    W, H = 1100, 640
    b = title(W, "Where does the answer live?", "Pick the tool by where the knowledge is, not by habit.")
    cards = [
        (i_brain, "General knowledge", '"What is a REST API?"', "Plain LLM", BLUE, False),
        (i_doc, "One small document", '"Summarize this PDF"', "Paste it in", GREEN, False),
        (i_code, "Code on disk", '"Fix the login bug"', "grep + read files", PURPLE, False),
        (i_table, "Database / numbers", '"Sales by region in Q3?"', "SQL / a tool", ORANGE, False),
        (i_plug, "A live system", '"Is order #123 shipped?"', "API call", PINK, False),
        (i_stack, "Huge pile of text", '"Our refund policy for…"', "RAG", YELLOW, True),
    ]
    for i, (icon, where, ex, tool, col, star) in enumerate(cards):
        r, c = divmod(i, 3)
        x, y = 60 + c * 340, 130 + r * 245
        b += note(x, y, 300, 215, col, rot=((-0.8, 0.6, -0.4), (0.7, -0.6, 0.5))[r][c])
        b += badge(x + 28, y + 30, i + 1, r=14)
        b += icon(x + 150, y + 55)
        b += t(x + 150, y + 112, where, size=18, weight=800, anchor="middle")
        b += t(x + 150, y + 138, ex, size=13.5, anchor="middle", color=SOFT, italic=True)
        bw = len(tool) * 16 * 0.6 + 50
        b += f'<rect x="{x + 150 - bw / 2}" y="{y + 156}" width="{bw}" height="36" rx="18" fill="{ACCENT if star else "#FFFFFF"}" stroke="{INK}" stroke-width="1.6"/>'
        b += t(x + 150, y + 180, "→ " + tool, size=16, weight=800, anchor="middle", color="#FFFFFF" if star else INK)
        if star:
            b += i_spark(x + 275, y + 30, 0.8, fill=ACCENT)
    svg(W, H, b, "where-does-the-answer-live", "01-rag", "Six places an answer can live and the tool for each: general knowledge, plain LLM; one small document, paste it in; code on disk, grep; database, SQL; live system, API; huge pile of text, RAG.")


def two_failures():
    W, H = 1100, 470
    b = title(W, "A RAG system can fail in 2 places", "So every test checks both: was the right chunk found? Is the answer right?")
    xs = [70, 330, 590, 850]
    steps = [("Question", i_chat, PINK), ("Retriever", i_search, YELLOW), ("Chunks", i_stack, GREEN), ("LLM → Answer", i_spark, BLUE)]
    for i, (lbl, icon, col) in enumerate(steps):
        b += note(xs[i], 130, 180, 120, col, rot=(-1, 0.8, -0.6, 0.9)[i], tape=False)
        b += icon(xs[i] + 90, 175)
        b += t(xs[i] + 90, 230, lbl, size=16, weight=800, anchor="middle")
        if i < 3:
            b += arrow(xs[i] + 186, 190, xs[i + 1] - 6, 190)
    for x, n, head, lines, fix in [
        (220, 1, "Right chunk NOT found", ["Checked by: file hit, chunk hit"], "Fix: chunk size, k, embedding model"),
        (700, 2, "Chunk found, answer wrong", ["Ignored it, misread it, or invented"], 'Fix: prompt, "say not found" rule'),
    ]:
        b += f'<path d="M{x + 180},{262} v30" stroke="{BAD}" stroke-width="3" stroke-dasharray="5 4"/>'
        b += note(x, 300, 360, 140, "#FFFFFF", rot=0.5 if n == 1 else -0.5)
        b += cross(x + 30, 330, 0.9)
        b += t(x + 52, 336, f"Failure {n}: {head}", size=15.5, weight=800)
        b += t(x + 22, 372, lines, size=14, color=SOFT)
        b += t(x + 22, 410, fix, size=14, weight=700, color=GOOD)
    svg(W, H, b, "two-failures", "01-rag", "A RAG pipeline goes question, retriever, chunks, LLM. Failure 1: the retriever misses the right chunk. Failure 2: the chunk is found but the LLM ignores it or invents.")


# ---------------------------------------------------------------------------
# Diagrams: Agentic AI
# ---------------------------------------------------------------------------
def agent_loop():
    W, H = 1100, 600
    b = title(W, "The agent loop: Think → Act → Observe", "The LLM repeats this until the goal is reached.")

    b += note(50, 250, 170, 120, PINK, rot=-1.5)
    b += t(135, 290, "GOAL", size=17, weight=800, anchor="middle")
    b += t(135, 318, ['"Do scheduled', 'tasks notify?"'], size=13.5, anchor="middle", italic=True)

    pos = [(470, 115, YELLOW, i_bulb, "THINK", ["What do I know?", "What next?"]),
           (650, 345, GREEN, i_wrench, "ACT", ["Call a tool", "search_codebase(…)"]),
           (290, 345, BLUE, i_eye, "OBSERVE", ["Read the result", "scheduler.py: no notify"])]
    for i, (x, y, col, icon, head, lines) in enumerate(pos):
        b += note(x, y, 200, 170, col, rot=(0.8, -1, 1)[i])
        b += badge(x + 26, y + 28, i + 1)
        b += icon(x + 100, y + 60)
        b += t(x + 100, y + 112, head, size=19, weight=800, anchor="middle")
        b += t(x + 100, y + 136, lines, size=13, anchor="middle", color=SOFT, font=MONO if i else FONT)
    b += arrow(675, 210, 760, 335, bend=-0.18)
    b += arrow(640, 445, 500, 445, bend=-0.18)
    b += arrow(380, 335, 465, 210, bend=-0.18)
    b += arrow(225, 305, 462, 195, bend=0.15)
    b += t(560, 330, "repeat", size=16, weight=800, anchor="middle", color=ACCENT)

    b += note(880, 140, 180, 140, GREEN, rot=1.2)
    b += check(970, 180)
    b += t(970, 225, "Done?", size=18, weight=800, anchor="middle")
    b += t(970, 250, "→ final answer", size=14, anchor="middle")
    b += arrow(675, 160, 872, 190, bend=-0.08, dashed=True)
    b += t(780, 150, "when done", size=13.5, anchor="middle", color=SOFT, italic=True)
    b += t(W / 2, 572, "The LLM only ASKS for a tool call. Your code runs the tool and gives the result back.", size=15, weight=700, anchor="middle")
    svg(W, H, b, "agent-loop", "02-agentic-ai", "The agent loop: from a goal, the agent thinks, acts by calling a tool, observes the result, and repeats until done, then gives the final answer.")


def building_blocks():
    W, H = 1100, 660
    b = title(W, "The 6 building blocks of an agent", "Same LLM inside. The blocks around it make it an agent.")
    b += note(445, 255, 210, 170, PINK, rot=0)
    b += i_brain(550, 315, 1.3)
    b += t(550, 385, "AGENT", size=22, weight=800, anchor="middle")
    blocks = [
        (60, 130, YELLOW, i_brain, "1  Model", ["the LLM that thinks", "gpt-4o-mini"]),
        (60, 300, GREEN, i_scroll, "2  Instructions", ["system prompt: role,", "rules, format"]),
        (60, 470, BLUE, i_wrench, "3  Tools", ["functions it may call:", "search, APIs, files"]),
        (790, 130, PURPLE, i_box, "4  Memory", ["short: this chat", "long: saved facts"]),
        (790, 300, ORANGE, i_map, "5  Planning", ["break the goal", "into steps"]),
        (790, 470, "#D7F0F5", i_shield, "6  Guardrails", ["max steps, approvals,", "allowed tools"]),
    ]
    for i, (x, y, col, icon, head, lines) in enumerate(blocks):
        b += note(x, y, 250, 140, col, rot=(-0.8, 0.6, -0.5, 0.7, -0.6, 0.8)[i])
        b += (icon(x + 45, y + 70, 0.9) if icon is not i_brain else icon(x + 45, y + 70, 0.8, fill="#FFFFFF"))
        b += t(x + 85, y + 50, head, size=18, weight=800)
        b += t(x + 85, y + 80, lines, size=14, color=SOFT)
        if x < 400:
            b += arrow(x + 256, y + 70, 438, 340 + (y - 300) * 0.25, color=SOFT)
        else:
            b += arrow(x - 6, y + 70, 662, 340 + (y - 300) * 0.25, color=SOFT)
    svg(W, H, b, "agent-building-blocks", "02-agentic-ai", "Six building blocks around the agent: model, instructions, tools, memory, planning, guardrails.")


def classic_vs_agentic_rag():
    W, H = 1100, 520
    b = title(W, "Classic RAG vs. Agentic RAG", "Who decides what to search?")
    b += note(50, 130, 480, 350, BLUE, rot=-0.7)
    b += t(80, 172, "Classic RAG  ·  a fixed pipeline", size=19, weight=800)
    b += i_chat(110, 245) + arrow(140, 245, 190, 245)
    b += i_search(225, 245) + arrow(255, 245, 305, 245)
    b += i_spark(340, 245) + t(340, 285, "answer", size=13, anchor="middle", weight=700)
    b += t(225, 285, "1 search", size=13, anchor="middle", weight=700)
    b += t(80, 362, ["• Always searches exactly once", "• Uses your exact question as the search", "• Cheap and predictable"], size=15.5)
    b += t(80, 455, "In our code: --retrieval-only", size=14, weight=700, font=MONO, color=SOFT)

    b += note(570, 130, 480, 350, GREEN, rot=0.7)
    b += t(600, 172, "Agentic RAG  ·  the LLM drives", size=19, weight=800)
    b += i_chat(630, 245) + arrow(660, 245, 700, 245)
    b += i_brain(735, 245, 0.9) + t(735, 285, "agent", size=13, anchor="middle", weight=700)
    b += arrow(765, 232, 820, 205) + arrow(765, 258, 820, 285)
    b += pill(828, 192, "1st search", size=13)[0] + pill(828, 272, "2nd search", size=13)[0]
    b += arrow(932, 205, 975, 236) + arrow(932, 285, 975, 256)
    b += i_spark(998, 245) + t(998, 285, "answer", size=13, anchor="middle", weight=700)
    b += t(880, 325, "its own search words", size=12.5, anchor="middle", color=SOFT, italic=True)
    b += t(600, 362, ["• Decides IF and how often to search", "• Rewrites the question into better searches", "• Can also call APIs, SQL, grep"], size=15.5)
    b += t(600, 455, "In our code: create_agent + search_codebase", size=14, weight=700, font=MONO, color=SOFT)
    svg(W, H, b, "classic-vs-agentic-rag", "02-agentic-ai", "Classic RAG searches once with the exact question; agentic RAG lets the LLM decide whether to search, rewrite the query and search several times.")


# ---------------------------------------------------------------------------
# Diagrams: AST chunking (RAG page 7)
# ---------------------------------------------------------------------------
def ast_tree():
    W, H = 1100, 600
    b = title(W, "AST: code becomes a tree", "Python's ast module reads the structure, not just the characters.")

    # left: the code
    b += note(50, 140, 430, 300, "#FFFFFF", rot=-0.8)
    b += t(80, 178, "billing.py (simplified)", size=15, weight=800, color=SOFT)
    code = [("class BillingService:", PURPLE), ("    def check_task_limit(self, user):", BLUE),
            ("        if current_count >= limit:", GREEN), ('            raise BillingError("…")', ORANGE)]
    for i, (line, col) in enumerate(code):
        y = 205 + i * 52
        b += f'<rect x="72" y="{y}" width="388" height="36" rx="6" fill="{col}"/>'
        b += t(84, y + 24, line, size=14, font=MONO, weight=600)
    b += t(265, 425, "4 lines of text", size=14, anchor="middle", color=SOFT, italic=True)

    b += arrow(495, 290, 575, 290)
    b += t(535, 275, "ast.parse()", size=14, weight=800, anchor="middle", font=MONO)

    # right: the tree
    nodes = [(810, 150, "Module", "the whole file", "#F3F4F6"),
             (810, 245, "ClassDef", "BillingService", PURPLE),
             (810, 340, "FunctionDef", "check_task_limit", BLUE),
             (700, 440, "If", "current_count >= limit", GREEN),
             (920, 440, "arguments", "self, user", "#F3F4F6")]
    for x, y, kind, name, col in nodes:
        b += note(x - 95, y, 190, 62, col, rot=0, tape=False)
        b += t(x, y + 26, kind, size=16, weight=800, anchor="middle", font=MONO)
        b += t(x, y + 48, name, size=12.5, anchor="middle", color=SOFT, font=MONO)
    b += note(605, 530, 190, 52, ORANGE, rot=0, tape=False)
    b += t(700, 554, "Raise", size=16, weight=800, anchor="middle", font=MONO)
    b += t(700, 573, "BillingError", size=12.5, anchor="middle", color=SOFT, font=MONO)
    for x1, y1, x2, y2 in [(810, 212, 810, 243), (810, 307, 810, 338), (790, 402, 720, 438), (830, 402, 900, 438), (700, 502, 700, 528)]:
        b += f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{INK}" stroke-width="2.2"/>'
    b += t(1050, 278, ["each box", "= a node"], size=13.5, anchor="end", color=SOFT, italic=True)
    b += t(265, 480, ["Same colour = same piece of code.", "The tree knows where each", "class and function starts and ends."],
           size=14.5, weight=700, anchor="middle")
    svg(W, H, b, "ast-tree", "01-rag", "ast.parse turns four lines of billing.py into a tree: Module, ClassDef BillingService, FunctionDef check_task_limit, If, Raise.")


def ast_vs_characters():
    W, H = 1100, 600
    b = title(W, "Chunking code: by characters vs. by AST", "Same function, check_task_limit (531 characters).")

    b += note(50, 130, 480, 420, PINK, rot=-0.6)
    b += cross(90, 168)
    b += t(115, 175, "By characters  (module 01, size 256)", size=18, weight=800)
    pieces = [("def check_task_limit(self, user):", "  plan = self.get_plan(user)", "  limit = TASK_LIMITS.get(…)"),
              ("current_count = len(…)", "  if current_count >= limit:", "    raise BillingError("),
              ('"Upgrade your plan_tier…"', "", "")]
    for i, lines in enumerate(pieces):
        y = 205 + i * 92
        b += note(85, y, 300, 78, "#FFFFFF", rot=(-1.2, 1, -0.8)[i], tape=False)
        b += t(100, y + 24, [l for l in lines if l], size=12.5, font=MONO)
        b += t(400, y + 44, f"piece {i + 1}", size=13, weight=700, color=SOFT)
    b += f'<path d="M80,{290} h330 M80,{382} h330" stroke="{BAD}" stroke-width="2.5" stroke-dasharray="7 5"/>'
    b += t(80, 510, ["Cut wherever the size runs out.", "Piece 2 has the check but not the name."], size=14.5, weight=700, color=BAD)

    b += note(570, 130, 480, 420, GREEN, rot=0.6)
    b += check(610, 168)
    b += t(635, 175, "By AST  (module 02)", size=18, weight=800)
    b += note(605, 205, 410, 150, "#FFFFFF", rot=0.6, tape=False)
    b += t(622, 232, ["class BillingService:", "  def check_task_limit(self, user):", "    plan = self.get_plan(user)",
                      "    if current_count >= limit:", "      raise BillingError(…)", "  def usage_summary(self, user): …"],
           size=12.5, font=MONO)
    b += t(1005, 232, "1 chunk", size=13, weight=700, anchor="end", color=GOOD)
    b += pill(605, 372, "type: class", size=13)[0] + pill(730, 372, "name: BillingService", size=13)[0]
    b += t(600, 440, ["Cut where the code says a unit ends:", "a whole class or a whole function.", "Each chunk also gets its type and name."],
           size=14.5, weight=700, color=GOOD)
    svg(W, H, b, "ast-vs-character-chunking", "01-rag", "By characters, check_task_limit is cut into three pieces; by AST, the whole BillingService class is one chunk with its type and name.")


def ast_uses():
    W, H = 1100, 400
    b = title(W, "Where else are ASTs used?", "Any tool that needs to UNDERSTAND code, not just read text.")
    cards = [(i_spark, "Compilers and interpreters", "turn code into something", "the computer runs", BLUE),
             (i_shield, "Linters and checkers", "spot bugs and style", "problems (e.g. Ruff)", GREEN),
             (i_wrench, "IDEs", "autocomplete, rename,", "go to definition", PURPLE),
             (i_search, "Code RAG (us!)", "cut code into whole", "classes and functions", YELLOW)]
    for i, (icon, head, l1, l2, col) in enumerate(cards):
        x = 50 + i * 255
        b += note(x, 130, 235, 230, col, rot=(-0.8, 0.6, -0.5, 0.8)[i])
        b += badge(x + 26, 158, i + 1, r=14)
        b += icon(x + 117, 205)
        b += t(x + 117, 265, head, size=16, weight=800, anchor="middle")
        b += t(x + 117, 295, [l1, l2], size=13.5, anchor="middle", color=SOFT)
    svg(W, H, b, "ast-uses", "01-rag", "ASTs are used by compilers and interpreters, linters, IDEs, and code RAG.")


if __name__ == "__main__":
    ast_tree()
    ast_vs_characters()
    ast_uses()
    rag_overview()
    with_without_rag()
    chunking()
    overlap()
    embeddings()
    chunk_k_grid()
    k_vs_tokens()
    where_answer_lives()
    two_failures()
    agent_loop()
    building_blocks()
    classic_vs_agentic_rag()

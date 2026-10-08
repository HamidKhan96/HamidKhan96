#!/usr/bin/env python3
"""
Generate the profile's SVG art, light and dark, FROM ONE TEMPLATE.

Both themes come out of the same geometry string with only the palette
substituted. That is deliberate: the house rule this workspace keeps breaking is
a derived colour that only looks right in one theme, and the usual cause is two
hand-maintained copies drifting apart. One template cannot drift.

No web fonts. A README image is served through GitHub's camo proxy, which does
not fetch Google Fonts, so anything referencing Instrument Serif would silently
fall back on the viewer's machine and change the layout. Generic stacks only.
"""
import os

# Writes beside itself. Run it from anywhere: `python3 assets/generate.py`.
OUT = os.path.dirname(os.path.abspath(__file__))

# The Exynex warm-paper palette, read from 1. Exynex Web Design's own CSS tokens.
THEMES = {
    'light': dict(bg='#F4EEE2', panel='#FFFFFF', ink='#16120C', muted='#5E574B',
                  subtle='#897F71', accent='#DE4F1D', line='#DED5C4'),
    'dark':  dict(bg='#0E0C09', panel='#17130E', ink='#F2EDE3', muted='#B3AB9D',
                  subtle='#8C8377', accent='#ED6230', line='#2A2318'),
}

SERIF = "Georgia,'Times New Roman',Times,serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

# ── hero ────────────────────────────────────────────────────────────────────
HERO = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="Hamid Khan, GTM engineer">
  <rect width="1200" height="300" fill="{bg}"/>
  <rect x="0" y="0" width="6" height="300" fill="{accent}"/>

  <!-- A pipeline, which is what most of this work actually is: a source, a
       filter, a decision, an action. Low opacity so it reads as texture. -->
  <g opacity="0.5" fill="none" stroke="{accent}" stroke-width="1.5">
    <line x1="885" y1="150" x2="955" y2="105"/>
    <line x1="885" y1="150" x2="955" y2="195"/>
    <line x1="955" y1="105" x2="1030" y2="150"/>
    <line x1="955" y1="195" x2="1030" y2="150"/>
    <line x1="1030" y1="150" x2="1105" y2="150"/>
  </g>
  <g fill="{bg}" stroke="{accent}" stroke-width="2">
    <circle cx="885" cy="150" r="9"/>
    <circle cx="955" cy="105" r="7"/>
    <circle cx="955" cy="195" r="7"/>
    <circle cx="1030" cy="150" r="9"/>
  </g>
  <circle cx="1105" cy="150" r="11" fill="{accent}"/>

  <text x="72" y="118" font-family="{serif}" font-size="62" fill="{ink}">Hamid Khan</text>
  <rect x="74" y="140" width="54" height="3" fill="{accent}"/>
  <text x="72" y="183" font-family="{sans}" font-size="20" fill="{muted}">GTM engineer. I build the tooling my own sales and recruiting runs on.</text>

  <g font-family="{sans}" font-size="13" letter-spacing="0.08em">
    <rect x="72" y="214" width="150" height="30" rx="15" fill="none" stroke="{accent}" stroke-width="1.5"/>
    <circle cx="90" cy="229" r="4" fill="{accent}"/>
    <text x="102" y="234" fill="{accent}">APPLYING · LIVE</text>

    <rect x="232" y="214" width="96" height="30" rx="15" fill="none" stroke="{line}"/>
    <text x="252" y="234" fill="{subtle}">QUILL</text>

    <rect x="338" y="214" width="108" height="30" rx="15" fill="none" stroke="{line}"/>
    <text x="358" y="234" fill="{subtle}">EXYNEX</text>

    <rect x="456" y="214" width="170" height="30" rx="15" fill="none" stroke="{line}"/>
    <text x="476" y="234" fill="{subtle}">ICP PIPELINES</text>
  </g>
</svg>
'''

# ── metrics ─────────────────────────────────────────────────────────────────
# Every figure here is counted, not estimated. The comment says where from so a
# future reader can re-run it rather than trust it.
#   12,544  vitest run, cloud/, 2026-10-08
#    2,042  git rev-list --count across the five repos
#      148  cloud/src/db/migrations/*.sql
#   11,819  jobs where deleted_at IS NULL, production, 2026-10-08
STATS = [
    ('12,544', 'tests passing', 'one suite, 74 seconds'),
    ('2,042',  'commits',       'since April 2026'),
    ('148',    'migrations',    'forward only, no rollbacks'),
    ('11,819', 'job postings',  'indexed and de-duplicated'),
]

def metrics(p):
    w, h = 1200, 190
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Four counted figures from the work">',
        f'<rect width="{w}" height="{h}" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>',
    ]
    colw = w / len(STATS)
    for i, (num, label, sub) in enumerate(STATS):
        cx = colw * i + colw / 2
        if i:
            x = colw * i
            parts.append(f'<line x1="{x:.0f}" y1="42" x2="{x:.0f}" y2="{h-42}" stroke="{p["line"]}"/>')
        parts.append(
            f'<text x="{cx:.0f}" y="88" text-anchor="middle" font-family="{SERIF}" '
            f'font-size="46" fill="{p["accent"]}">{num}</text>'
        )
        parts.append(
            f'<text x="{cx:.0f}" y="120" text-anchor="middle" font-family="{SANS}" '
            f'font-size="15" fill="{p["ink"]}">{label}</text>'
        )
        parts.append(
            f'<text x="{cx:.0f}" y="143" text-anchor="middle" font-family="{SANS}" '
            f'font-size="12.5" fill="{p["subtle"]}">{sub}</text>'
        )
    parts.append('</svg>')
    return '\n  '.join(parts) + '\n'


# ── system diagram ──────────────────────────────────────────────────────────
# Applying, as it actually runs. Drawn rather than screenshotted because a
# screenshot of a dashboard shows a moment and this shows the shape.
NODES = [
    # (x, y, w, label, sublabel, emphasis). Five columns, left to right, which is
    # the order a job actually moves through the system.
    (40,  54, 150, 'Chrome MV3',     'reads the posting',    False),
    (40, 150, 150, 'Job boards',     '12 scrapers',          False),
    (250, 102, 170, 'Next.js 15',    'app + server actions', True),
    (480,  54, 150, 'Postgres 17',   '148 migrations',       False),
    (480, 150, 150, 'Inngest',       'queued work',          False),
    (690, 102, 160, 'Worker',        'ticks, scrapes, mail', False),
    (910,  54, 150, 'Claude',        'tailoring, scoring',   False),
    (910, 150, 150, 'Gmail / Graph', 'OAuth, per message',   False),
]
# Node centres: a 72px box at y gives centre y+36. Edges meet boxes on the
# centre line, offset slightly where two share a side.
EDGES = [
    (190,  90, 250, 128),   # extension  -> app
    (190, 186, 250, 148),   # scrapers   -> app
    (420, 128, 480,  90),   # app        -> database
    (420, 148, 480, 186),   # app        -> queue
    (630, 186, 690, 148),   # queue      -> worker
    (630,  90, 690, 128),   # database   -> worker
    (850, 128, 910,  90),   # worker     -> model
    (850, 148, 910, 186),   # worker     -> mail
]

def diagram_svg(p):
    w, h = 1080, 250
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="How Applying runs: extension and scrapers into Next.js, Postgres and a worker, through a queue, out to Claude and email">',
        f'<rect width="{w}" height="{h}" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<text x="28" y="34" font-family="{SANS}" font-size="13" letter-spacing="0.09em" fill="{p["subtle"]}">APPLYING, AS IT RUNS</text>',
    ]
    for x1, y1, x2, y2 in EDGES:
        mx = (x1 + x2) / 2
        out.append(
            f'<path d="M{x1} {y1} C{mx} {y1}, {mx} {y2}, {x2} {y2}" fill="none" '
            f'stroke="{p["line"]}" stroke-width="1.5"/>'
        )
    for x, y, bw, label, sub, strong in NODES:
        stroke = p['accent'] if strong else p['line']
        sw = 2 if strong else 1.2
        out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="72" rx="10" fill="{p["bg"]}" stroke="{stroke}" stroke-width="{sw}"/>')
        out.append(
            f'<text x="{x + bw/2:.0f}" y="{y + 31}" text-anchor="middle" '
            f'font-family="{SANS}" font-size="15" fill="{p["ink"]}">{label}</text>'
        )
        out.append(
            f'<text x="{x + bw/2:.0f}" y="{y + 52}" text-anchor="middle" '
            f'font-family="{SANS}" font-size="11.5" fill="{p["subtle"]}">{sub}</text>'
        )
    out.append('</svg>')
    return '\n  '.join(out) + '\n'



# ── where the commits are ───────────────────────────────────────────────────
# Counted with `git rev-list --count HEAD` in each repository on 2026-10-08.
# This replaced a github-readme-stats card that reported "Total Commits: 3",
# because that card reads public repositories only and twelve of fourteen are
# private. A graph that under-reports by three orders of magnitude is worse
# than no graph, which is the same reason there is no top-languages card.
REPOS = [
    ('Applying',      1680),
    ('Quill',          267),
    ('Workspace',       65),
    ('Exynex site',     28),
    ('ICP pipelines',    2),
]

def commits_svg(p):
    # 272 tall, not 250. Five rows from top=58 at 38px pitch put the last bar's
    # bottom edge at exactly 232, and the footnote baseline was at h-18 = 232:
    # the two collided precisely, and only a render showed it. The footnote now
    # sits at h-20 = 252, twenty clear of the last bar.
    w, h = 1080, 272
    left, top, barh, gap = 190, 58, 22, 16
    maxv = max(v for _, v in REPOS)
    track = w - left - 150
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Commits by repository: Applying 1680, Quill 267, workspace 65, Exynex site 28, ICP pipelines 2">',
        f'<rect width="{w}" height="{h}" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>',
        f'<text x="28" y="34" font-family="{SANS}" font-size="13" letter-spacing="0.09em" fill="{p["subtle"]}">WHERE THE COMMITS ARE</text>',
    ]
    for i, (name, v) in enumerate(REPOS):
        y = top + i * (barh + gap)
        bw = max(3, track * v / maxv)
        out.append(
            f'<text x="{left - 16}" y="{y + 16}" text-anchor="end" font-family="{SANS}" '
            f'font-size="14" fill="{p["ink"]}">{name}</text>'
        )
        out.append(f'<rect x="{left}" y="{y}" width="{track}" height="{barh}" rx="4" fill="{p["bg"]}"/>')
        out.append(f'<rect x="{left}" y="{y}" width="{bw:.0f}" height="{barh}" rx="4" fill="{p["accent"]}"/>')
        out.append(
            f'<text x="{left + bw + 12:.0f}" y="{y + 16}" font-family="{SANS}" '
            f'font-size="13.5" fill="{p["muted"]}">{v:,}</text>'
        )
    out.append(
        f'<text x="28" y="{h - 20}" font-family="{SANS}" font-size="12" fill="{p["subtle"]}">'
        f'2,042 commits since April 2026. Counted in each repository, public and private.</text>'
    )
    out.append('</svg>')
    return '\n  '.join(out) + '\n'


written = []
for name, p in THEMES.items():
    hero = HERO.format(serif=SERIF, sans=SANS, **p)
    for base, body in (('hero', hero), ('metrics', metrics(p)), ('system', diagram_svg(p)), ('commits', commits_svg(p))):
        path = os.path.join(OUT, f'{base}-{name}.svg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(body)
        written.append((f'{base}-{name}.svg', len(body)))

for n, size in written:
    print(f'  {n:22} {size:>6} bytes')

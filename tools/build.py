"""Erzeugt die SVGs in assets/. Aufruf: python3 tools/build.py"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
MONO = "ui-monospace,'JetBrains Mono','Cascadia Code',Consolas,monospace"
SANS = "-apple-system,'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
CW = 9.05  # Zeichenbreite Monospace bei 15px

# ---------- Hero: Terminal, das "bootet" ----------
LINES = [  # (art, text, start in s)
    ("cmd", "whoami", 0.6),
    ("out", "Emre. Ich baue Software, die dir gehört.", 1.4),
    ("cmd", "ls ~/projekte", 2.0),
    ("out", "cinemamax/  kelimo/  speedload/  giga-share/  werwolf/  gym-ranker/", 2.9),
    ("cmd", "cat prinzipien.txt", 3.5),
    ("ok", "✓ kein Konto   ✓ kein Tracking   ✓ läuft lokal   ✓ open source", 4.5),
]


def hero():
    rows, y = [], 108
    for i, (kind, text, t) in enumerate(LINES):
        if kind == "cmd":
            w = (len(text) + 1) * CW
            rows.append(f'''
  <clipPath id="c{i}"><rect x="160" y="{y-16}" height="22" width="0">
    <animate attributeName="width" from="0" to="{w:.0f}" begin="{t}s" dur="{len(text)*0.06:.2f}s" fill="freeze"/></rect></clipPath>
  <g opacity="0"><set attributeName="opacity" to="1" begin="{t-0.3}s" fill="freeze"/>
    <text x="40" y="{y}" class="m"><tspan fill="#7ee787">emre@1001</tspan><tspan fill="#6e7681">:</tspan><tspan fill="#79c0ff">~</tspan><tspan fill="#6e7681">$</tspan></text>
    <text x="160" y="{y}" class="m" fill="#e6edf3" clip-path="url(#c{i})">{text}</text></g>''')
        else:
            fill = "#7ee787" if kind == "ok" else "#c9d1d9"
            rows.append(f'''
  <text x="40" y="{y}" class="m" fill="{fill}" opacity="0"><set attributeName="opacity" to="1" begin="{t}s" fill="freeze"/>{text}</text>''')
        y += 34 if kind == "cmd" else 50
    end = LINES[-1][2] + 0.5
    rows.append(f'''
  <g opacity="0"><set attributeName="opacity" to="1" begin="{end}s" fill="freeze"/>
    <text x="40" y="{y}" class="m"><tspan fill="#7ee787">emre@1001</tspan><tspan fill="#6e7681">:</tspan><tspan fill="#79c0ff">~</tspan><tspan fill="#6e7681">$</tspan></text>
    <rect x="160" y="{y-15}" width="10" height="19" fill="#e6edf3" class="blink"/></g>''')

    # Seitenpanel: Geräte "verbinden" sich nacheinander
    devices = [("📺", "Android TV", "CinemaMax"), ("📱", "Handy", "Kelimo"),
               ("💻", "Linux / Windows", "Speedload"), ("🌐", "LAN + P2P", "Giga-Share"),
               ("🐺", "Spieleabend", "Werwolf Mobile"), ("🏋", "Training", "Gym Ranker")]
    panel, py = [], 128
    for i, (ico, dev, proj) in enumerate(devices):
        t = 0.8 + i * 0.7
        panel.append(f'''
  <g opacity="0.25"><animate attributeName="opacity" from="0.25" to="1" begin="{t}s" dur="0.3s" fill="freeze"/>
    <text x="960" y="{py}" font-size="16">{ico}</text>
    <text x="990" y="{py-1}" class="s" fill="#e6edf3" font-size="14" font-weight="600">{proj}</text>
    <text x="990" y="{py+15}" class="s" fill="#6e7681" font-size="11.5">{dev}</text>
    <circle cx="1170" cy="{py-4}" r="4" fill="#30363d"><set attributeName="fill" to="#7ee787" begin="{t}s" fill="freeze"/></circle></g>''')
        py += 42

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" role="img" aria-label="Emre: Ich baue Software, die dir gehört. Kein Konto, kein Tracking, läuft lokal, open source.">
<style>
  .m {{ font: 15px {MONO}; white-space: pre; }}
  .s {{ font-family: {SANS}; }}
  .blink {{ animation: b 1s steps(1) infinite; }}
  @keyframes b {{ 50% {{ opacity: 0; }} }}
  .scan {{ animation: sc 6s linear infinite; }}
  @keyframes sc {{ from {{ transform: translateY(-80px); }} to {{ transform: translateY(440px); }} }}
  .glow {{ animation: g 5s ease-in-out infinite alternate; transform-origin: 1050px 60px; }}
  @keyframes g {{ from {{ opacity: .35; transform: scale(1); }} to {{ opacity: .7; transform: scale(1.25); }} }}
</style>
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>
  <radialGradient id="rg"><stop offset="0" stop-color="#3E8BFF" stop-opacity=".5"/><stop offset="1" stop-color="#3E8BFF" stop-opacity="0"/></radialGradient>
  <linearGradient id="sl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ee787" stop-opacity="0"/><stop offset="1" stop-color="#7ee787" stop-opacity=".07"/></linearGradient>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3E8BFF"/><stop offset=".5" stop-color="#A855F7"/><stop offset="1" stop-color="#22C55E"/></linearGradient>
  <clipPath id="win"><rect x="1" y="1" width="1198" height="418" rx="16"/></clipPath>
</defs>
<g clip-path="url(#win)">
  <rect width="1200" height="420" fill="#0B0E14"/>
  <rect width="1200" height="420" fill="url(#grid)"/>
  <circle cx="1050" cy="60" r="260" fill="url(#rg)" class="glow"/>
  <rect y="0" width="1200" height="80" fill="url(#sl)" class="scan"/>
  <rect width="1200" height="44" fill="#0F131B"/>
  <line x1="0" y1="44" x2="1200" y2="44" stroke="#1F2630"/>
  <circle cx="26" cy="22" r="6" fill="#ff5f57"/><circle cx="46" cy="22" r="6" fill="#febc2e"/><circle cx="66" cy="22" r="6" fill="#28c840"/>
  <text x="600" y="27" text-anchor="middle" class="m" font-size="13" fill="#6e7681" style="font-size:13px">emre@1001 — ~/projekte — zsh</text>
  <line x1="930" y1="70" x2="930" y2="390" stroke="#1F2630"/>
  <text x="960" y="88" class="m" fill="#6e7681" style="font-size:12px">GERÄTE</text>
  {"".join(panel)}
  {"".join(rows)}
</g>
<rect x="1" y="1" width="1198" height="418" rx="16" fill="none" stroke="url(#bd)" stroke-opacity=".6" stroke-width="1.5"/>
</svg>
'''


# ---------- Projektkarten ----------
CARDS = [
    ("cinemamax", "CinemaMax", "IPTV-PLAYER · ANDROID TV · HANDY · PC", "#3E8BFF",
     ["Alles, was läuft. Auf jedem Bildschirm.", "M3U, Xtream, Stalker. Ohne Werbung und Tracking."], ["Flutter", "Dart"]),
    ("kelimo", "Kelimo", "KI-SPRACHTUTOR · ANDROID", "#22C55E",
     ["Sprachen lernen mit einer KI, die nur auf", "deinem Handy läuft. Kein Konto, kein Server."], ["Kotlin", "Compose", "LiteRT-LM"]),
    ("speedload", "Speedload", "DOWNLOAD-MANAGER · LINUX · WINDOWS", "#F97316",
     ["Bis zu 32 Verbindungen pro Datei.", "Setzt nach Abbruch fort. Eine Datei, 2 MB."], ["Rust"]),
    ("giga-share", "Giga-Share", "DATEITRANSFER · LAN + P2P", "#A855F7",
     ["Dateien zwischen allen Geräten senden.", "Keine Cloud, kein Konto, kein Größenlimit."], ["Rust", "Tauri", "React"]),
    ("werwolf-mobile", "Werwolf Mobile", "PARTYSPIEL · PWA · ONLINE + LOKAL", "#EF4444",
     ["Das Werwolf-Kartenspiel fürs Handy, mit", "automatischem Erzähler und 10 Rollen."], ["JavaScript", "PWA", "Firebase"]),
    ("gym-ranker", "Gym Ranker", "FITNESS · ANDROID · PWA", "#EAB308",
     ["Training als Rangliste: XP sammeln und", "33 Ränge aufsteigen. Wer skippt, verliert."], ["HTML", "JavaScript", "PWA"]),
]


def card(i, slug, title, tag, color, desc, chips):
    chip_svg, cx = [], 32
    for c in chips:
        w = len(c) * 7.4 + 22
        chip_svg.append(f'<rect x="{cx}" y="170" width="{w:.0f}" height="24" rx="12" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".45"/>'
                        f'<text x="{cx + w/2:.0f}" y="186" text-anchor="middle" class="m" fill="{color}">{c}</text>')
        cx += w + 8
    d = "".join(f'<text x="32" y="{120 + k*22}" class="d">{line}</text>' for k, line in enumerate(desc))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 220" width="480" height="220" role="img" aria-label="{title}: {' '.join(desc)}">
<style>
  .t {{ font: 700 30px {SANS}; fill: #f0f3f6; letter-spacing: -.5px; }}
  .g {{ font: 600 11px {MONO}; fill: {color}; letter-spacing: 1.2px; }}
  .d {{ font: 14.5px {SANS}; fill: #9aa4b2; }}
  .m {{ font: 600 12px {MONO}; }}
  .n {{ font: 700 64px {MONO}; fill: {color}; fill-opacity: .07; }}
  .p {{ animation: p 4s ease-in-out infinite alternate; transform-origin: 440px 20px; }}
  @keyframes p {{ from {{ opacity: .25; transform: scale(.9); }} to {{ opacity: .55; transform: scale(1.15); }} }}
  .bar {{ animation: w 3s ease-in-out infinite alternate; }}
  @keyframes w {{ from {{ stroke-dashoffset: 120; }} to {{ stroke-dashoffset: 0; }} }}
</style>
<defs>
  <radialGradient id="r"><stop offset="0" stop-color="{color}" stop-opacity=".55"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>
  <clipPath id="k"><rect x="1" y="1" width="478" height="218" rx="14"/></clipPath>
</defs>
<g clip-path="url(#k)">
  <rect width="480" height="220" fill="#0B0E14"/>
  <circle cx="440" cy="20" r="150" fill="url(#r)" class="p"/>
  <text x="462" y="206" text-anchor="end" class="n">{i:02d}</text>
  <line x1="32" y1="32" x2="152" y2="32" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-dasharray="120" class="bar"/>
  <text x="32" y="60" class="g">{tag}</text>
  <text x="32" y="96" class="t">{title}</text>
  {d}
  {"".join(chip_svg)}
</g>
<rect x="1" y="1" width="478" height="218" rx="14" fill="none" stroke="{color}" stroke-opacity=".35"/>
</svg>
'''


# ---------- Fußzeile ----------
def footer():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 90" width="1200" height="90" role="img" aria-label="Kein Konto. Kein Abo. Kein Tracking. Nur Software.">
<style>
  .f {{ font: 600 15px {MONO}; letter-spacing: 3px; fill: #8b949e; }}
  .l {{ stroke-dasharray: 6 10; animation: m 1.2s linear infinite; }}
  @keyframes m {{ to {{ stroke-dashoffset: -16; }} }}
  .x {{ animation: c 8s linear infinite; }}
  @keyframes c {{ 0%,100% {{ fill: #3E8BFF; }} 33% {{ fill: #A855F7; }} 66% {{ fill: #22C55E; }} }}
</style>
<line x1="0" y1="20" x2="1200" y2="20" stroke="#3E8BFF" stroke-opacity=".5" class="l"/>
<text x="600" y="62" text-anchor="middle" class="f">KEIN KONTO · KEIN ABO · KEIN TRACKING · <tspan class="x">NUR SOFTWARE</tspan></text>
</svg>
'''


if __name__ == "__main__":
    (OUT / "cards").mkdir(parents=True, exist_ok=True)
    (OUT / "hero.svg").write_text(hero(), encoding="utf-8")
    (OUT / "footer.svg").write_text(footer(), encoding="utf-8")
    for i, c in enumerate(CARDS, 1):
        (OUT / "cards" / f"{c[0]}.svg").write_text(card(i, *c), encoding="utf-8")

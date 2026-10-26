"""Erzeugt die SVGs in assets/<sprache>/<theme>/. Aufruf: python3 tools/build.py"""
import shutil
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
MONO = "ui-monospace,'JetBrains Mono','Cascadia Code',Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
CW = 9.05  # Zeichenbreite Monospace bei 15px
EASE = "cubic-bezier(.22,1,.36,1)"

# ---------- Tokens: neutrale Basis, ein Akzent ----------
THEMES = {
    "dark": dict(bg="#0f1115", surface="#15181e", inset="#1d2128", border="#ffffff", border_a=".08",
                 text="#e8e9ec", muted="#9a9fa8", faint="#5c616b", accent="#8fb0dc", ok="#8cc7a0"),
    "light": dict(bg="#f6f6f4", surface="#ffffff", inset="#efefec", border="#000000", border_a=".09",
                  text="#1a1b1e", muted="#5b5f67", faint="#a3a6ac", accent="#3d5a80", ok="#3c7a56"),
}

# Gemeinsames CSS: Startzustände stecken nur in den Animationen,
# bei reduzierter Bewegung ist sofort alles sichtbar.
BASE_CSS = f"""
  .in {{ animation: in .45s {EASE} both; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateY(6px); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}"""

# ---------- Texte ----------
I18N = {
    "de": dict(
        path="~/projekte", ls="ls ~/projekte", cat="cat prinzipien.txt", devices="GERÄTE",
        whoami="Emre. Ich baue Software, die dir gehört.",
        ok="✓ kein Konto   ✓ kein Tracking   ✓ läuft lokal   ✓ open source",
        dev=["Android TV", "Handy", "Linux / Windows", "LAN + P2P", "Spieleabend", "Training"],
        footer=("KEIN KONTO · KEIN ABO · KEIN TRACKING · ", "NUR SOFTWARE"),
        cards=[
            ("IPTV-PLAYER · ANDROID TV · HANDY · PC",
             ["Alles, was läuft. Auf jedem Bildschirm.", "M3U, Xtream, Stalker. Ohne Werbung und Tracking."]),
            ("KI-SPRACHTUTOR · ANDROID",
             ["Sprachen lernen mit einer KI, die nur auf", "deinem Handy läuft. Kein Konto, kein Server."]),
            ("DOWNLOAD-MANAGER · LINUX · WINDOWS",
             ["Bis zu 32 Verbindungen pro Datei.", "Setzt nach Abbruch fort. Eine Datei, 2 MB."]),
            ("DATEITRANSFER · LAN + P2P",
             ["Dateien zwischen allen Geräten senden.", "Keine Cloud, kein Konto, kein Größenlimit."]),
            ("PARTYSPIEL · PWA · ONLINE + LOKAL",
             ["Das Werwolf-Kartenspiel fürs Handy, mit", "automatischem Erzähler und 10 Rollen."]),
            ("FITNESS · ANDROID · PWA",
             ["Training als Rangliste: XP sammeln und", "33 Ränge aufsteigen. Wer skippt, verliert."]),
        ]),
    "en": dict(
        path="~/projects", ls="ls ~/projects", cat="cat principles.txt", devices="DEVICES",
        whoami="Emre. I build software that belongs to you.",
        ok="✓ no account   ✓ no tracking   ✓ runs locally   ✓ open source",
        dev=["Android TV", "Phone", "Linux / Windows", "LAN + P2P", "Game night", "Workout"],
        footer=("NO ACCOUNT · NO SUBSCRIPTION · NO TRACKING · ", "JUST SOFTWARE"),
        cards=[
            ("IPTV PLAYER · ANDROID TV · PHONE · PC",
             ["Everything that's on. On every screen.", "M3U, Xtream, Stalker. No ads, no tracking."]),
            ("AI LANGUAGE TUTOR · ANDROID",
             ["Learn languages with an AI that runs only", "on your phone. No account, no server."]),
            ("DOWNLOAD MANAGER · LINUX · WINDOWS",
             ["Up to 32 connections per file.", "Resumes after interruptions. One file, 2 MB."]),
            ("FILE TRANSFER · LAN + P2P",
             ["Send files between all your devices.", "No cloud, no account, no size limit."]),
            ("PARTY GAME · PWA · ONLINE + LOCAL",
             ["The Werewolf card game for your phone,", "with an automatic narrator and 10 roles."]),
            ("FITNESS · ANDROID · PWA",
             ["Training as a ranking: earn XP and", "climb 33 ranks. Skip a day, fall behind."]),
        ]),
    "tr": dict(
        path="~/projeler", ls="ls ~/projeler", cat="cat ilkeler.txt", devices="CİHAZLAR",
        whoami="Emre. Sana ait yazılımlar geliştiriyorum.",
        ok="✓ hesap yok   ✓ takip yok   ✓ yerelde çalışır   ✓ açık kaynak",
        dev=["Android TV", "Telefon", "Linux / Windows", "LAN + P2P", "Oyun gecesi", "Antrenman"],
        footer=("HESAP YOK · ABONELİK YOK · TAKİP YOK · ", "SADECE YAZILIM"),
        cards=[
            ("IPTV OYNATICI · ANDROID TV · TELEFON · PC",
             ["Yayında olan her şey. Her ekranda.", "M3U, Xtream, Stalker. Reklam yok, takip yok."]),
            ("YAPAY ZEKÂ DİL ÖĞRETMENİ · ANDROID",
             ["Sadece telefonunda çalışan bir yapay", "zekâyla dil öğren. Hesap yok, sunucu yok."]),
            ("İNDİRME YÖNETİCİSİ · LINUX · WINDOWS",
             ["Dosya başına 32 bağlantıya kadar.", "Kesintiden sonra devam eder. Tek dosya, 2 MB."]),
            ("DOSYA AKTARIMI · LAN + P2P",
             ["Tüm cihazların arasında dosya gönder.", "Bulut yok, hesap yok, boyut sınırı yok."]),
            ("PARTİ OYUNU · PWA · ÇEVRİMİÇİ + YEREL",
             ["Telefon için Vampir Köylü kart oyunu,", "otomatik anlatıcı ve 10 rol ile."]),
            ("FİTNES · ANDROID · PWA",
             ["Antrenman bir sıralama: XP topla ve", "33 rütbe yüksel. Atlayan geride kalır."]),
        ]),
}

PROJECTS = [  # (slug, Titel, Technik)
    ("cinemamax", "CinemaMax", ["Flutter", "Dart"]),
    ("kelimo", "Kelimo", ["Kotlin", "Compose", "LiteRT-LM"]),
    ("speedload", "Speedload", ["Rust"]),
    ("giga-share", "Giga-Share", ["Rust", "Tauri", "React"]),
    ("werwolf-mobile", "Werwolf Mobile", ["JavaScript", "PWA", "Firebase"]),
    ("gym-ranker", "Gym Ranker", ["HTML", "JavaScript", "PWA"]),
]

# Linien-Icons (16×16) statt Emoji
ICONS = [
    '<rect x="1" y="2.5" width="14" height="9.5" rx="1.5"/><path d="M5 14.5h6"/>',
    '<rect x="4" y="1" width="8" height="14" rx="2"/><path d="M7 12.3h2"/>',
    '<rect x="2.5" y="2.5" width="11" height="8" rx="1"/><path d="M1 13.5h14"/>',
    '<circle cx="3" cy="8" r="1.8"/><circle cx="13" cy="3" r="1.8"/><circle cx="13" cy="13" r="1.8"/><path d="M4.6 7.2 11.4 3.8M4.6 8.8l6.8 3.4"/>',
    '<circle cx="6" cy="5" r="2.4"/><path d="M1.5 14c0-2.6 2-4.2 4.5-4.2s4.5 1.6 4.5 4.2"/><circle cx="11.6" cy="5.6" r="1.9"/><path d="M11.4 9.9c1.9 0 3.3 1.3 3.3 3.6"/>',
    '<path d="M4 8h8M4 4.5v7M12 4.5v7M1.8 6.2v3.6M14.2 6.2v3.6"/>',
]


def prompt(x, y):
    return (f'<text x="{x}" y="{y}" class="m"><tspan class="ok">emre@1001</tspan><tspan class="f">:</tspan>'
            f'<tspan class="a">~</tspan><tspan class="f">$</tspan></text>')


# ---------- Hero: Terminal, das "bootet" ----------
def hero(L, c):
    lines = [("cmd", "whoami", 0.5), ("out", L["whoami"], 1.2), ("cmd", L["ls"], 1.8),
             ("out", "cinemamax/  kelimo/  speedload/  giga-share/  werwolf/  gym-ranker/", 2.6),
             ("cmd", L["cat"], 3.2), ("good", L["ok"], 4.1)]
    rows, y = [], 112
    for kind, text, t in lines:
        text = escape(text)
        if kind == "cmd":
            w = (len(text) + 1) * CW
            rows.append(f'''
  <g class="in" style="animation-delay:{t - 0.3:.2f}s">{prompt(40, y)}
    <text x="160" y="{y}" class="m tx">{text}</text>
    <rect x="158" y="{y - 17}" width="{w:.0f}" height="24" class="cover type" style="animation-delay:{t}s;animation-duration:{len(text) * 0.055:.2f}s"/></g>''')
        else:
            cls = "ok" if kind == "good" else "tx"
            rows.append(f'''
  <text x="40" y="{y}" class="m {cls} in" style="animation-delay:{t}s">{text}</text>''')
        y += 34 if kind == "cmd" else 48
    end = lines[-1][2] + 0.5
    rows.append(f'''
  <g class="in" style="animation-delay:{end}s">{prompt(40, y)}
    <rect x="160" y="{y - 15}" width="9" height="19" rx="1" class="cur"/></g>''')

    panel, py = [], 132
    for i, (proj, dev) in enumerate(zip([p[1] for p in PROJECTS], L["dev"])):
        t = 0.8 + i * 0.55
        panel.append(f'''
  <g class="dev" style="animation-delay:{t:.2f}s">
    <g transform="translate(958 {py - 13})" class="ico">{ICONS[i]}</g>
    <text x="986" y="{py - 1}" class="s tx" font-size="14" font-weight="600">{proj}</text>
    <text x="986" y="{py + 15}" class="s mu" font-size="12">{escape(dev)}</text>
    <circle cx="1166" cy="{py - 4}" r="3.5" class="dot" style="animation-delay:{t:.2f}s"/></g>''')
        py += 42

    label = escape(f"Emre: {L['whoami'].split('. ', 1)[1]} {L['ok'].replace('✓', '').strip()}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" role="img" aria-label="{label}">
<style>
  .m {{ font: 15px {MONO}; white-space: pre; }}
  .s {{ font-family: {SANS}; }}
  .tx {{ fill: {c["text"]}; }} .mu {{ fill: {c["muted"]}; }} .f {{ fill: {c["faint"]}; }}
  .ok {{ fill: {c["ok"]}; }} .a {{ fill: {c["accent"]}; }}
  .cover {{ fill: {c["surface"]}; }}
  .type {{ animation: type 1s steps(12, end) both; transform-box: fill-box; transform-origin: right; }}
  @keyframes type {{ from {{ transform: scaleX(1); }} to {{ transform: scaleX(0); }} }}
  .cur {{ fill: {c["text"]}; animation: blink 1.1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .ico {{ fill: none; stroke: {c["muted"]}; stroke-width: 1.4; stroke-linecap: round; stroke-linejoin: round; }}
  .dev {{ animation: dim .35s {EASE} both; }}
  @keyframes dim {{ from {{ opacity: .3; }} }}
  .dot {{ fill: {c["ok"]}; animation: dot .35s {EASE} both; }}
  @keyframes dot {{ from {{ fill: {c["inset"]}; }} }}{BASE_CSS}
</style>
<defs><clipPath id="win"><rect x="1" y="1" width="1198" height="418" rx="16"/></clipPath></defs>
<g clip-path="url(#win)">
  <rect width="1200" height="420" fill="{c["surface"]}"/>
  <rect width="1200" height="44" fill="{c["bg"]}"/>
  <line x1="0" y1="44.5" x2="1200" y2="44.5" stroke="{c["border"]}" stroke-opacity="{c["border_a"]}"/>
  <circle cx="26" cy="22" r="5.5" fill="{c["inset"]}"/><circle cx="44" cy="22" r="5.5" fill="{c["inset"]}"/><circle cx="62" cy="22" r="5.5" fill="{c["inset"]}"/>
  <text x="600" y="27" text-anchor="middle" class="m mu" style="font-size:13px">emre@1001 — {L["path"]}</text>
  <line x1="930.5" y1="74" x2="930.5" y2="386" stroke="{c["border"]}" stroke-opacity="{c["border_a"]}"/>
  <text x="958" y="92" class="m mu" style="font-size:11px;letter-spacing:1.5px">{L["devices"]}</text>
  {"".join(panel)}
  {"".join(rows)}
</g>
<rect x=".5" y=".5" width="1199" height="419" rx="16" fill="none" stroke="{c["border"]}" stroke-opacity="{c["border_a"]}"/>
</svg>
'''


# ---------- Projektkarten ----------
def card(n, title, chips, tag, desc, c):
    chip_svg, cx = [], 32
    for ch in chips:
        w = len(ch) * 7.3 + 20
        chip_svg.append(f'<rect x="{cx}" y="168" width="{w:.0f}" height="24" rx="6" fill="{c["inset"]}"/>'
                        f'<text x="{cx + w / 2:.0f}" y="184" text-anchor="middle" class="c">{ch}</text>')
        cx += w + 6
    d = "".join(f'<text x="32" y="{122 + k * 22}" class="d">{escape(line)}</text>' for k, line in enumerate(desc))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 220" width="480" height="220" role="img" aria-label="{escape(title)}: {escape(' '.join(desc))}">
<style>
  .t {{ font: 700 30px {SANS}; fill: {c["text"]}; letter-spacing: -.6px; }}
  .g {{ font: 600 11px {MONO}; fill: {c["accent"]}; letter-spacing: 1.2px; }}
  .d {{ font: 14.5px {SANS}; fill: {c["muted"]}; }}
  .c {{ font: 600 12px {MONO}; fill: {c["muted"]}; }}
  .n {{ font: 600 12px {MONO}; fill: {c["faint"]}; font-variant-numeric: tabular-nums; }}{BASE_CSS}
</style>
<rect x=".5" y=".5" width="479" height="219" rx="14" fill="{c["surface"]}" stroke="{c["border"]}" stroke-opacity="{c["border_a"]}"/>
<text x="448" y="48" text-anchor="end" class="n">{n:02d}</text>
<g class="in" style="animation-delay:.05s"><text x="32" y="48" class="g">{escape(tag)}</text>
<text x="32" y="88" class="t">{escape(title)}</text></g>
<g class="in" style="animation-delay:.12s">{d}</g>
<g class="in" style="animation-delay:.19s">{"".join(chip_svg)}</g>
</svg>
'''


# ---------- Fußzeile ----------
def footer(L, c):
    a, b = L["footer"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 80" width="1200" height="80" role="img" aria-label="{escape(a + b)}">
<style>
  .f {{ font: 600 14px {MONO}; letter-spacing: 3px; fill: {c["muted"]}; }}
  .x {{ fill: {c["accent"]}; }}
</style>
<line x1="0" y1="16.5" x2="1200" y2="16.5" stroke="{c["border"]}" stroke-opacity="{c["border_a"]}"/>
<text x="600" y="56" text-anchor="middle" class="f">{escape(a)}<tspan class="x">{escape(b)}</tspan></text>
</svg>
'''


# ---------- READMEs ----------
GH = "https://github.com/Emre1001"
README = {
    "de": dict(
        file="README.md", alt_hero="Emre: Ich baue Software, die dir gehört.",
        claim="Software, die auf <b>deinem</b> Gerät läuft – nicht auf fremden Servern.",
        intro="Vom Fernseher übers Handy bis zum PC: Ich baue Apps ohne Konto, ohne Abo und ohne Tracking.<br>\nLokal, schnell, quelloffen. Und mit Liebe zum Detail im Design.",
        h_build="Was ich baue", h_more="Noch mehr aus der Werkstatt", th=("Projekt", "Was es macht"),
        more=["P2P-Bildschirmfreigabe & Fernsteuerung in Rust, mit Live-Cursorn aller Zuschauer",
              "Aus Playlists werden MP3s. Windows, Linux, Android",
              "Macht dein Handy zur kabellosen HD-Webcam",
              "Portabler Windows-Debloater von Light bis Max",
              "All-in-One-Game-Launcher für Windows",
              "Finanz-Tracker als PWA, ohne Build-Schritt"],
        h_tools="Werkzeugkasten", h_how="Wie ich baue",
        how=["+ Lokal zuerst       Daten bleiben auf dem Gerät. Die KI auch.",
             "+ Klein & schnell    Speedload: eine Datei, 2 MB. Kein Electron, wenn's nicht sein muss.",
             "+ Überall            Android TV, Handy, Linux, Windows, Browser.",
             "+ Offen              MIT-Lizenz. Lies den Code, bau ihn selbst.",
             "- Konten, Abos, Werbung, Tracking"]),
    "en": dict(
        file="README.en.md", alt_hero="Emre: I build software that belongs to you.",
        claim="Software that runs on <b>your</b> device – not on someone else's servers.",
        intro="From the TV to the phone to the PC: I build apps without accounts, subscriptions or tracking.<br>\nLocal, fast, open source. And designed with care for the details.",
        h_build="What I build", h_more="More from the workshop", th=("Project", "What it does"),
        more=["P2P screen sharing & remote control in Rust, with live cursors for every viewer",
              "Turns playlists into MP3s. Windows, Linux, Android",
              "Turns your phone into a wireless HD webcam",
              "Portable Windows debloater, from Light to Max",
              "All-in-one game launcher for Windows",
              "Finance tracker as a PWA, no build step"],
        h_tools="Toolbox", h_how="How I build",
        how=["+ Local first       Data stays on the device. The AI too.",
             "+ Small & fast      Speedload: one file, 2 MB. No Electron unless it has to be.",
             "+ Everywhere        Android TV, phone, Linux, Windows, browser.",
             "+ Open              MIT license. Read the code, build it yourself.",
             "- Accounts, subscriptions, ads, tracking"]),
    "tr": dict(
        file="README.tr.md", alt_hero="Emre: Sana ait yazılımlar geliştiriyorum.",
        claim="Yabancı sunucularda değil, <b>senin</b> cihazında çalışan yazılımlar.",
        intro="Televizyondan telefona, telefondan bilgisayara: Hesapsız, aboneliksiz ve takipsiz uygulamalar geliştiriyorum.<br>\nYerel, hızlı, açık kaynak. Ve tasarımda her ayrıntıya özen.",
        h_build="Neler geliştiriyorum", h_more="Atölyeden daha fazlası", th=("Proje", "Ne yapar"),
        more=["Rust ile P2P ekran paylaşımı ve uzaktan kontrol, tüm izleyicilerin canlı imleçleriyle",
              "Çalma listelerini MP3'e dönüştürür. Windows, Linux, Android",
              "Telefonunu kablosuz bir HD web kamerasına dönüştürür",
              "Light'tan Max'e taşınabilir Windows debloater",
              "Windows için hepsi bir arada oyun başlatıcı",
              "Derleme adımı olmadan PWA olarak finans takibi"],
        h_tools="Alet çantası", h_how="Nasıl geliştiriyorum",
        how=["+ Önce yerel        Veriler cihazda kalır. Yapay zekâ da.",
             "+ Küçük & hızlı     Speedload: tek dosya, 2 MB. Gerekmedikçe Electron yok.",
             "+ Her yerde         Android TV, telefon, Linux, Windows, tarayıcı.",
             "+ Açık              MIT lisansı. Kodu oku, kendin derle.",
             "- Hesaplar, abonelikler, reklam, takip"]),
}
MORE = [("Screen-Clean", "Screen-Clean"), ("YT Music → MP3", "Ytms-to-mp3"), ("Phone-Cam", "Phone-Cam"),
        ("Debloatranium", "Debloatranium"), ("LaunchDeck", "LaunchDeck"), ("Financely", "Financely")]
REPOS = {"cinemamax": "CinemaMax", "kelimo": "kelimo", "speedload": "speedload",
         "giga-share": "Giga-Share", "werwolf-mobile": "Werwolf-Mobile", "gym-ranker": "Gym-Ranker"}
NAMES = {"de": "Deutsch", "en": "English", "tr": "Türkçe"}


def pic(lang, path, alt, width):
    """Bild, das GitHubs Hell-/Dunkel-Modus folgt."""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{lang}/dark/{path}">'
            f'<source media="(prefers-color-scheme: light)" srcset="assets/{lang}/light/{path}">'
            f'<img src="assets/{lang}/dark/{path}" width="{width}" alt="{alt}"></picture>')


def readme(lang, R, L):
    langs = " · ".join(f"<b>{NAMES[k]}</b>" if k == lang else f'<a href="{README[k]["file"]}">{NAMES[k]}</a>'
                       for k in README)
    cards = "\n".join(f'  <a href="{GH}/{REPOS[slug]}">{pic(lang, f"cards/{slug}.svg", title, "49%")}</a>'
                      for slug, title, _ in PROJECTS)
    more = "\n".join(f"| [{name}]({GH}/{repo}) | {what} |" for (name, repo), what in zip(MORE, R["more"]))
    a, b = L["footer"]
    icons = "rust,flutter,dart,kotlin,androidstudio,ts,react,tauri,firebase,linux,html,css&perline=12"
    return f'''<!-- Erzeugt von tools/build.py – bitte dort ändern. -->
<p align="right"><sub>{langs}</sub></p>

<a href="{GH}">{pic(lang, "hero.svg", R["alt_hero"], "100%")}</a>

<div align="center">

### {R["claim"]}

{R["intro"]}

</div>

## {R["h_build"]}

<p align="center">
{cards}
</p>

<details>
<summary><b>{R["h_more"]}</b></summary>
<br>

| {R["th"][0]} | {R["th"][1]} |
|---|---|
{more}

</details>

## {R["h_tools"]}

<p align="center">
  <picture><source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i={icons}&theme=light"><img src="https://skillicons.dev/icons?i={icons}&theme=dark" alt="Rust, Flutter, Dart, Kotlin, Android, TypeScript, React, Tauri, Firebase, Linux, HTML, CSS"></picture>
</p>

## {R["h_how"]}

```diff
{chr(10).join(R["how"])}
```

<a href="{GH}?tab=repositories">{pic(lang, "footer.svg", a + b, "100%")}</a>
'''


if __name__ == "__main__":
    for lang, R in README.items():
        (OUT.parent / R["file"]).write_text(readme(lang, R, I18N[lang]), encoding="utf-8")
    for old in [OUT / "cards", OUT / "hero.svg", OUT / "footer.svg"]:  # alte, einsprachige Ausgabe
        shutil.rmtree(old) if old.is_dir() else old.unlink(missing_ok=True)
    for lang, L in I18N.items():
        for theme, c in THEMES.items():
            d = OUT / lang / theme
            (d / "cards").mkdir(parents=True, exist_ok=True)
            (d / "hero.svg").write_text(hero(L, c), encoding="utf-8")
            (d / "footer.svg").write_text(footer(L, c), encoding="utf-8")
            for n, ((slug, title, chips), (tag, desc)) in enumerate(zip(PROJECTS, L["cards"]), 1):
                (d / "cards" / f"{slug}.svg").write_text(card(n, title, chips, tag, desc, c), encoding="utf-8")

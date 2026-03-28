"""
Generate output/index.html table of contents for À la recherche du temps perdu.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../epubkit'))

from epubkit.epub import extract_chapters
from epubkit.segment import segment_chapter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'docs')

VOLUMES = [
    {
        "epub":   os.path.join(os.path.dirname(__file__), 'Proust-01.epub'),
        "label":  "Volume I – Du côté de chez Swann",
        "prefix": "proust-01",
        "skip":   {0, 1, 2, 7},   # 0-based indices of front/back matter
        "titles": {4: "Combray", 5: "Un amour de Swann"},
    },
    {
        "epub":   os.path.join(os.path.dirname(__file__), 'Proust-02.epub'),
        "label":  "Volume II – À l'ombre des jeunes filles en fleurs",
        "prefix": "proust-02",
        "skip":   {0, 1, 5},      # 0-based indices of front/back matter
        "titles": {},
    },
]


def volume_rows(vol):
    chapters = extract_chapters(vol["epub"])
    rows = []
    for i, ch in enumerate(chapters):
        if i in vol["skip"]:
            continue
        num = i + 1
        segs = segment_chapter(ch)
        episode_id = f"{vol['prefix']}-ch{num}"
        html_file = os.path.join(OUTPUT_DIR, f"{episode_id}.html")
        available = os.path.exists(html_file)
        title = vol["titles"].get(num) or (
            ch.title if ch.title != f"Chapter {num}" else f"Chapitre {num}"
        )
        seg_label = f"{len(segs)} segments"
        if available:
            rows.append(f"""
            <a class="chapter-row available" href="{episode_id}.html">
                <span class="ch-num">{num}</span>
                <span class="ch-title">{title}</span>
                <span class="ch-meta">{seg_label}</span>
                <span class="ch-arrow">&#x276F;</span>
            </a>""")
        else:
            rows.append(f"""
            <div class="chapter-row unavailable">
                <span class="ch-num">{num}</span>
                <span class="ch-title">{title}</span>
                <span class="ch-meta">{seg_label}</span>
                <span class="ch-status">coming soon</span>
            </div>""")
    return rows


def main():
    sections = []
    for vol in VOLUMES:
        rows = volume_rows(vol)
        sections.append(f"""
        <div class="vol-header">{vol['label']}</div>
        {"".join(rows)}""")

    body_html = "\n".join(sections)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>À la recherche du temps perdu – Interleaved Reader</title>
    <style>
        :root {{ --primary: #004a99; --accent: #ffc107; --bg: #f0f2f5; }}
        body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; background: var(--bg); }}
        .header-box {{
            background: rgba(255,255,255,0.98); padding: 20px 24px;
            border-bottom: 3px solid var(--primary);
        }}
        .header-box h1 {{ margin: 0 0 4px; font-size: 1.4rem; color: var(--primary); }}
        .header-box .subtitle {{ font-size: 0.85rem; color: #555; }}
        .chapter-list {{
            max-width: 700px; margin: 24px auto; padding: 0 16px;
            display: flex; flex-direction: column; gap: 8px;
        }}
        .vol-header {{
            font-size: 0.75rem; font-weight: bold; text-transform: uppercase;
            letter-spacing: 0.05em; color: var(--primary);
            margin-top: 16px; margin-bottom: 4px; padding-left: 4px;
        }}
        .chapter-row {{
            display: flex; align-items: center; gap: 12px;
            background: white; border-radius: 12px; border: 1px solid #ddd;
            padding: 14px 16px; text-decoration: none; color: inherit;
        }}
        a.chapter-row.available {{ cursor: pointer; }}
        a.chapter-row.available:hover {{ border-color: var(--primary); background: #f0f6ff; }}
        .chapter-row.unavailable {{ opacity: 0.45; }}
        .ch-num {{
            font-size: 0.7rem; font-weight: bold; color: white;
            background: var(--primary); border-radius: 50%;
            width: 24px; height: 24px; display: flex; align-items: center;
            justify-content: center; flex-shrink: 0;
        }}
        .chapter-row.unavailable .ch-num {{ background: #aaa; }}
        .ch-title {{ flex: 1; font-weight: 600; font-size: 0.95rem; }}
        .ch-meta {{ font-size: 0.72rem; color: #888; white-space: nowrap; }}
        .ch-arrow {{ color: var(--primary); font-size: 0.9rem; }}
        .ch-status {{ font-size: 0.7rem; color: #aaa; font-style: italic; }}
    </style>
</head>
<body>
    <div class="header-box">
        <h1>À la recherche du temps perdu</h1>
        <div class="subtitle">Marcel Proust &nbsp;&middot;&nbsp; Interleaved French–English Reader</div>
    </div>
    <div class="chapter-list">
        {body_html}
    </div>
</body>
</html>"""

    out_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[*] Written {out_path}")


if __name__ == '__main__':
    main()

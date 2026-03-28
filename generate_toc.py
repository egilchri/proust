"""
Generate output/index.html table of contents for À la recherche du temps perdu I.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../epubkit'))

from epubkit.epub import extract_chapters
from epubkit.segment import segment_chapter

EPUB_PATH = os.path.join(os.path.dirname(__file__), 'Proust-01.epub')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'docs')


# Front/back matter chapter indices (0-based) to hide from the TOC
SKIP_CHAPTERS = {0, 1, 2, 7}  # chapters 1, 2, 3, 8

# Override titles for chapters whose epub headings are unhelpful
TITLE_OVERRIDES = {
    4: "Combray",           # epub title "I"
    5: "Un amour de Swann", # epub title "II"
}


def main():
    chapters = extract_chapters(EPUB_PATH)

    rows = []
    for i, ch in enumerate(chapters):
        if i in SKIP_CHAPTERS:
            continue

        num = i + 1
        segs = segment_chapter(ch)
        episode_id = f"proust-01-ch{num}"
        html_file = os.path.join(OUTPUT_DIR, f"{episode_id}.html")
        available = os.path.exists(html_file)

        title = TITLE_OVERRIDES.get(num) or (
            ch.title if ch.title != f"Chapter {num}" else f"Chapitre {num}"
        )
        seg_label = f"{len(segs)} segments"

        if available:
            row = f"""
            <a class="chapter-row available" href="{episode_id}.html">
                <span class="ch-num">{num}</span>
                <span class="ch-title">{title}</span>
                <span class="ch-meta">{seg_label}</span>
                <span class="ch-arrow">&#x276F;</span>
            </a>"""
        else:
            row = f"""
            <div class="chapter-row unavailable">
                <span class="ch-num">{num}</span>
                <span class="ch-title">{title}</span>
                <span class="ch-meta">{seg_label}</span>
                <span class="ch-status">coming soon</span>
            </div>"""
        rows.append(row)

    rows_html = "\n".join(rows)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>À la recherche du temps perdu I – Interleaved Reader</title>
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
        <h1>À la recherche du temps perdu I</h1>
        <div class="subtitle">Marcel Proust &nbsp;&middot;&nbsp; Interleaved French–English Reader</div>
    </div>
    <div class="chapter-list">
        {rows_html}
    </div>
</body>
</html>"""

    out_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[*] Written {out_path}")


if __name__ == '__main__':
    main()

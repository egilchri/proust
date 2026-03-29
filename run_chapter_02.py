"""
Run the interleaver pipeline for a single chapter of À la recherche du temps perdu II.

Usage:
    python3 run_chapter_02.py --chapter 3
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../interleaver'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../epubkit'))

from epubkit.epub import extract_chapters
from epubkit.segment import segment_chapter
from interleaver.pipeline import run_from_text
from interleaver.etymology import EtymologyCache

EPUB_PATH = os.path.join(os.path.dirname(__file__), 'Proust-02.epub')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'docs')
ETYMOLOGY_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'etymology_cache.json')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chapter', type=int, required=True, help='1-based chapter index')
    args = parser.parse_args()

    chapters = extract_chapters(EPUB_PATH)
    print(f"[*] Found {len(chapters)} chapters")

    idx = args.chapter - 1
    if idx < 0 or idx >= len(chapters):
        print(f"[!] Chapter {args.chapter} out of range (1-{len(chapters)})")
        sys.exit(1)

    chapter = chapters[idx]
    print(f"[*] Chapter {args.chapter}: {chapter.title!r}")

    segments = segment_chapter(chapter, max_chars=300)
    print(f"[*] {len(segments)} segments")

    episode_id = f"proust-02-ch{args.chapter}"
    etymology_cache = EtymologyCache(ETYMOLOGY_CACHE_PATH)

    run_from_text(
        segments=segments,
        source_lang='fr',
        output_dir=OUTPUT_DIR,
        episode_id=episode_id,
        title=f'À la recherche du temps perdu II – {chapter.title}',
        subtitle='Marcel Proust',
        etymology_cache=etymology_cache,
        ep_key=f'proust.vol2-ch{args.chapter}',
    )

if __name__ == '__main__':
    main()

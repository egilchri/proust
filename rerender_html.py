"""
Re-render HTML players for existing chapters without regenerating audio.
Reads transcript/vocab JSON already in docs/ and calls render_player directly.

Usage:
    python3 rerender_html.py                      # all chapters
    python3 rerender_html.py --episode proust-01-ch5
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../interleaver'))

from interleaver.player import render_player

DOCS_DIR = os.path.join(os.path.dirname(__file__), 'docs')


def ep_key_for(episode_id: str) -> str:
    """Convert 'proust-01-ch3' → 'proust.vol1-ch3'"""
    m = re.match(r'proust-0*(\d+)-ch(\d+)', episode_id)
    if not m:
        return episode_id
    return f'proust.vol{int(m.group(1))}-ch{int(m.group(2))}'


def title_for(episode_id: str) -> str:
    """Read title from the <title> tag in the existing HTML file."""
    html_path = os.path.join(DOCS_DIR, f"{episode_id}.html")
    if not os.path.exists(html_path):
        return episode_id
    with open(html_path, encoding='utf-8') as f:
        for line in f:
            m = re.search(r'<title>(.*?)</title>', line)
            if m:
                return m.group(1)
    return episode_id


def rerender(episode_id: str):
    json_path = os.path.join(DOCS_DIR, f"{episode_id}.json")
    vocab_path = os.path.join(DOCS_DIR, f"{episode_id}.vocab.json")
    html_path = os.path.join(DOCS_DIR, f"{episode_id}.html")

    with open(json_path, encoding='utf-8') as f:
        transcript_data = json.load(f)
    with open(vocab_path, encoding='utf-8') as f:
        vocab_data = json.load(f)

    title = title_for(episode_id)
    key = ep_key_for(episode_id)

    html = render_player(
        title=title,
        source_lang='fr',
        audio_path=f'{episode_id}.mp3',
        interleaved_audio_path=f'{episode_id}.bilingual.mp3',
        transcript_json_path=f'{episode_id}.json',
        vocab_json_path=f'{episode_id}.vocab.json',
        subtitle='Marcel Proust',
        transcript_data=transcript_data,
        vocab_data=vocab_data,
        ep_key=key,
    )
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[*] {os.path.basename(html_path)}  (ep_key={key!r})')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--episode', help='Single episode ID (e.g. proust-01-ch5)')
    args = parser.parse_args()

    if args.episode:
        episodes = [args.episode]
    else:
        episodes = sorted(
            f[:-5]  # strip .json
            for f in os.listdir(DOCS_DIR)
            if re.match(r'proust-\d+-ch\d+\.json$', f)
        )

    for ep in episodes:
        rerender(ep)
    print(f'[*] Done. Re-rendered {len(episodes)} player(s).')


if __name__ == '__main__':
    main()

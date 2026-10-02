#!/usr/bin/env python3
"""Create editorial read-along estimates. These are not audio-aligned timings."""
import argparse
import json
from pathlib import Path
import re


def stamp(milliseconds):
    value = int(milliseconds)
    hours, value = divmod(value, 3600000)
    minutes, value = divmod(value, 60000)
    seconds, millis = divmod(value, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02},{millis:03}'


def build(folder, wpm=120):
    manifest = json.loads((folder / 'story.json').read_text())
    pages = {p['id']: p for p in manifest['pages']}
    output = {'schema_version': 1, 'story_id': manifest['id'], 'title': manifest['title'],
              'timing_status': 'estimated_not_audio_aligned', 'audio_aligned': False,
              'enable_synchronized_highlighting': False,
              'estimate_model': {'words_per_minute': wpm, 'comma_pause_ms': 125,
                                 'sentence_pause_ms': 350},
              'offset_units': 'Unicode code points; convert to JS UTF-16 offsets before slicing',
              'segments': []}
    base = 60000 / wpm
    story_position = 0
    captions = []
    for segment in manifest['segments']:
        local_position = 0
        item = {'id': segment['id'], 'audio': segment['audio'],
                'story_start_ms': story_position, 'pages': []}
        for page_id in segment['pages']:
            page = pages[page_id]
            start = local_position
            words = []
            for match in re.finditer(r'\S+', page['narration']):
                token = match.group()
                end = local_position + base
                words.append({'text': token, 'char_start': match.start(), 'char_end': match.end(),
                              'start_ms': round(local_position), 'end_ms': round(end)})
                local_position = end
                punctuation = token.rstrip('"\u201d\u2019')
                if punctuation.endswith(('.', '!', '?')):
                    local_position += 350
                elif punctuation.endswith((',', ';', ':')):
                    local_position += 125
            page_item = {'id': page_id, 'text': page['narration'],
                         'pixelpop_image': page['pixelpop_image'], 'normal_image': page['normal_image'],
                         'start_ms': round(start), 'end_ms': round(local_position), 'words': words}
            item['pages'].append(page_item)
            # Eight-word caption chunks preserve the original script's character spans.
            for first in range(0, len(words), 8):
                chunk = words[first:first+8]
                captions.append((story_position + chunk[0]['start_ms'],
                                 story_position + chunk[-1]['end_ms'],
                                 page['narration'][chunk[0]['char_start']:chunk[-1]['char_end']]))
        item['duration_ms'] = round(local_position)
        output['segments'].append(item)
        story_position += item['duration_ms']
    output['duration_ms'] = story_position
    (folder / 'readalong.estimated.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n')
    subtitles = '\n\n'.join(f'{i}\n{stamp(a)} --> {stamp(b)}\n{text}'
                            for i, (a, b, text) in enumerate(captions, 1))
    (folder / 'readalong.estimated.srt').write_text(subtitles + '\n')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('story_dir', type=Path)
    parser.add_argument('--wpm', type=float, default=120)
    args = parser.parse_args()
    if args.wpm <= 0:
        parser.error('--wpm must be positive')
    result = build(args.story_dir, args.wpm)
    print(f"{result['title']}: estimated word timeline and captions saved; audio alignment still required")

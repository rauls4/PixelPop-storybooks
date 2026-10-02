#!/usr/bin/env python3
"""Combine final page WAVs and measure exact illustration cues; no API calls."""
import argparse
import json
from pathlib import Path
import wave


def assemble(story_dir):
    manifest_path = story_dir / 'story.json'
    manifest = json.loads(manifest_path.read_text())
    pages = {p['id']: p for p in manifest['pages']}
    prepared = []
    for segment in manifest['segments']:
        clips = []
        for page_id in segment['pages']:
            path = story_dir / pages[page_id]['audio_clip']
            with wave.open(str(path), 'rb') as source:
                fmt = (source.getnchannels(), source.getsampwidth(), source.getframerate(), source.getcomptype())
                if fmt != (1, 2, 16000, 'NONE'):
                    raise ValueError(f'{path}: expected mono 16-bit PCM at 16000 Hz, got {fmt}')
                frames = source.getnframes()
                pcm = source.readframes(frames)
                if frames <= 0 or len(pcm) != frames * 2:
                    raise ValueError(f'{path}: empty or truncated PCM')
                clips.append((frames, pcm))
        if len(clips) != 2:
            raise ValueError('Expected two page clips per segment')
        prepared.append((segment, clips))
    # Validate all source clips before writing any segment or measured manifest.
    for segment, clips in prepared:
        destination = story_dir / segment['audio']
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix('.tmp.wav')
        with wave.open(str(temporary), 'wb') as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(16000)
            for _, pcm in clips:
                output.writeframes(pcm)
        temporary.replace(destination)
        segment['page_start_frames'] = [0, clips[0][0]]
        segment['page_start_ms'] = [0, clips[0][0] * 1000 / 16000]
        segment['duration_frames'] = sum(frames for frames, _ in clips)
        segment['duration_ms'] = segment['duration_frames'] * 1000 / 16000
    manifest['audio_status'] = 'assembled_requires_listening_review'
    manifest['timing_status'] = 'measured_from_final_pcm_requires_playback_review'
    manifest['installable'] = False
    temporary_manifest = manifest_path.with_suffix('.tmp.json')
    temporary_manifest.write_text(json.dumps(manifest, indent=2) + '\n')
    temporary_manifest.replace(manifest_path)
    print(f"{manifest['title']}: six segments assembled with exact PCM frame cues; listening review still required")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('story_dir', type=Path)
    args = parser.parse_args()
    assemble(args.story_dir)

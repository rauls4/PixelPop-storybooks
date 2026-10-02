# Cursor: read-along text and timing

Four books now include word-level `readalong.estimated.json`, subtitle captions in `readalong.estimated.srt`, and a human-readable `READALONG_DRAFT.md`. story.json points to these files.

## Current timing status

These are editorial estimates at 120 words per minute, with 125 ms comma/semicolon/colon pauses and 350 ms sentence-end pauses. No recordings exist for the four new books. They are not measured timestamps. The filename and JSON timing_status explicitly say estimated; audio_aligned and enable_synchronized_highlighting are false. Do not present these estimates as verified playback synchronization. Existing story.json page_start_ms values remain null.

Use the text and its character spans to implement read-along layout now. Display the exact script; do not generate a substitute transcript or introduce spoken page labels. Page JSON contains its illustration paths and word tokens, including punctuation. char_start and char_end are offsets into the page's original text, counted in Unicode code points; JavaScript uses UTF-16, so convert offsets or tokenize the exact script in the client. All current tokens are checked against their source spans.

## Time coordinates

Word start_ms and end_ms, and each page start_ms/end_ms, are relative to the beginning of its six-part audio segment. Segment story_start_ms and the SRT cues use one continuous estimated story timeline with segments concatenated and no inter-segment gaps. Do not use continuous story time as the segment playback time. The player should select the active segment and read its audio position. Pauses freeze text highlighting; seeking selects the word containing the new position. During silence, clear the active word or retain the last completed word consistently. Use half-open intervals start_ms <= position < end_ms.

## Replace estimates after narration is recorded

1. Generate the twelve page narration clips using the exact saved script and consistent voice. Convert the final clips to mono 16-bit PCM at 16,000 Hz. Run assemble_narration.py to measure the six paired segment boundaries.
2. Obtain word boundaries from the actual final audio using forced alignment against the exact script, or a human-reviewed timestamp transcript. Audio transcription alone can change words; map alignment to the original script and flag discrepancies. Do not distribute page duration evenly across words and call that measured alignment.
3. For page one in a segment, segment-relative word start equals the word's measured page-clip start. For page two, add the first clip's final PCM-frame duration. If conversion, trimming, silence insertion or narration changes, remeasure and realign. Keep measured frame positions where possible.
4. Save verified files as readalong.aligned.json and readalong.aligned.srt; retain estimates as production references. The verified JSON uses the same segment/page/word structure, timing_status=audio_aligned, audio_aligned=true and enable_synchronized_highlighting=true. Update story.json to point to the aligned files only after listening review.
5. Validate every word: text matches the original character span, start < end, timestamps are monotonic, each word lies inside its page/segment, page two starts at its measured clip boundary, and all image/audio paths exist. Check read-along at normal playback, pause/resume, seek, segment transitions and delayed callbacks. Pinocchio art remains missing.

The picture reveal still begins at its measured page cue and lasts 260 ms. Word highlighting follows actual audio position independently; do not delay the transcript until the visual transition completes. Preserve existing volume behavior. Keep these drafts non-installable until audio, art, alignment and playback review are complete.

## Files

Each story folder (cinderella, thumbelina, pinocchio, snow-white) contains the three read-along files. The repeatable estimate generator is build_readalong.py. Production narrated audio and measured word alignment remain pending. Repository: https://github.com/rauls4/PixelPop-storybooks . No firmware or board changes were made for this content handoff.

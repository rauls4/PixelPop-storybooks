# PixelPop story content handoff

Content pack: this directory. Stories: Cinderella, Thumbelina, Pinocchio, Snow White. Each story has its own `SYNC_SCRIPT.md` and `story.json`. The scripts are the source of truth for the association between narration and illustrations.

## Synchronization contract

- Each story has six audio segments and twelve illustrated pages. Each segment contains two page narration clips, concatenated in page order.
- Generate each page's `narration` from `story.json` as its own audio clip. Use the same narrator, pace and audio format throughout. Do not add spoken page numbers or headings.
- Standalone page text is also saved under `narration/scripts/01.txt` through `12.txt`. The first spoken words shown in SYNC_SCRIPT.md identify the exact page-change sentence.
- Preserve all pauses inside each generated clip. Measure the final PCM clip duration from its sample count and sample rate after conversion. Concatenate the two clips with no additional gap. If an intentional gap is inserted, account for that gap in the second page's cue.
- Use a uniform PCM format compatible with the current Storybook decoder. Count PCM frames, not encoded file bytes or WAV header bytes. Retain cue positions in samples as well as milliseconds when possible to avoid rounding drift.
- Page one starts at segment position 0. Page two starts at the exact duration of page one's final clip. Write these measured offsets to `segments[].page_start_ms`. The current `null` means timing is unknown; never substitute half the segment length.
- Display page one before starting its audio segment. Drive page changes from the audio playback position, not from time spent loading files or the time when a network request began. Use sample position or the player’s actual playback clock where available.
- Begin the 260 ms page reveal at the page cue. Narration continues during the reveal. Cue means transition start; the new image is fully visible 260 ms later.
- Pause freezes narration and cue progression. On resume, preserve the playback position. Seek or restart selects the page containing the resulting playback position; a late callback jumps to the current correct page instead of replaying missed transitions.
- Preload the next image before its cue. Missing artwork must not stop narration; retain the last valid image, record the missing file and continue. Missing audio must be reported and handled without a stuck playback loop.
- Advance to the next segment on actual playback completion. A queued or requested audio segment has not necessarily started playing.
- Timing cannot be called verified until the actual rendered clips exist. Check every pair: second cue equals first clip length, combined length equals the sum of both clips, and all image paths resolve. Then watch/listen to playback through every boundary on a simulator or explicitly approved board.

Example: if page 01's final clip measures 13,240 ms and page 02 measures 17,680 ms, combined segment duration is 30,920 ms. Page 01 cue is 0; page 02 cue is 13,240 ms. These values are illustrative, not actual generated durations.

## Audio assembly

After generating the twelve page WAVs, convert each to mono, signed 16-bit PCM at 16,000 Hz and save under the manifest audio_clip path. Run `python3 assemble_narration.py <story-directory>`. It validates all twelve clips, concatenates six pairs without adding gaps, and writes page_start_frames, page_start_ms and segment durations. This measures synchronization; listen and verify playback before treating a book as ready. The script makes no API calls. Preserve the production page clips outside the board filesystem. Include a friendly AI-narrated credit in the book information.

## Asset and implementation rules

- PixelPop images: `pixelpop/01.jpg` through `12.jpg`, borderless 128×64. Normal images are separately retained for a future iPad app; do not copy them to the board.
- Keep existing Little Red Riding Hood content and volume behavior. Adapt the content manifest to the current module implementation after inspecting its current source.
- This Desktop reference currently uses signed 16-bit mono PCM at 16,000 Hz (`AudioOut.h`). Its Storybook loop still switches images using half the audio byte length. Cursor must replace that behavior with the measured per-page cue; changing only the content paths will not satisfy synchronization.
- Before implementation, read the current checkout's `COPILOT_HANDOFF.md` and `FLASHING.md`. The live firmware checkout has previously moved to `/Users/raul/dev/PixelPop`; confirm the current location. This pack contains content only.
- Verify image dimensions, complete page/audio references, monotonically increasing measured cues and filesystem capacity. Do not silently shorten scripts, resample to an unsupported format or remove another story to fit.
- Do not assume all recordings fit a 4 MB filesystem. At 16,000 Hz, mono 16-bit PCM needs 32,000 bytes/second: three minutes require 5,760,000 PCM bytes before images and filesystem overhead. Keep the complete library on GitHub; choose an implementation that stores only a fitting selected pack, caches individual segments, or streams supported audio. Never change partition layout merely to force the entire library onto a board.
- Prefer six combined segment WAVs on the board; twelve page WAVs are production intermediates and would duplicate narration storage. Preserve the measured page boundary when combining them.
- Firmware changes, builds and installation are Cursor's responsibility. Do not flash any board without the user's explicit approval and the project backup/coordination procedure.

## Readiness

This is a work-in-progress pack. Artwork and audio must be verified before installation. Narration scripts are complete; recorded audio and measured cues are pending. Repository: https://github.com/rauls4/PixelPop-storybooks . Draft book manifests are at `<story-id>/story.json`, illustration/narration scripts at `<story-id>/SYNC_SCRIPT.md`, and prepared images at `<story-id>/pixelpop/01.jpg` through `12.jpg`. Use the published ASSET_VALIDATION.json inventory to identify existing assets; Pinocchio image and new audio paths remain planned. Do not expose these drafts as installable books.

## Editorial preview and versioned artwork

`review.html` pairs each page with its exact narration and a true 64×32 preview. It opens locally without a server; keep its sibling story directories beside it. It does not simulate audio timing. Cinderella revised images are selected in story.json; use manifest paths rather than assuming all filenames are pixelpop/NN.jpg. Prior images are retained. Corrections cover the prince’s navy outfit, Cinderella’s everyday dress during slipper fitting, and her ball gown at midnight.

## Read-along text

See READALONG_HANDOFF.md and each book’s readalong.estimated.json / readalong.estimated.srt. These contain estimated word timestamps for editorial development; recorded audio does not exist yet. Preserve timing_status and disable synchronized highlighting until actual narration alignment and listening review.

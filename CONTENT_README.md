# PixelPop story content

Four original bedtime retellings: Cinderella, Thumbelina, Pinocchio and Snow White. These are production drafts, not install-ready story packs.

All four books have twelve page narration scripts, six segment definitions, standalone speech request bodies, and an explicit illustration-to-narration sync script. Cinderella, Thumbelina and Snow White each have twelve normal JPEGs and twelve borderless 128×64 close-up JPEGs. Cinderella normal pages are individual 1774×887 renders; the other two normal editions are sheet crops around 440×220 and need larger renders for a high-resolution iPad release. Original generated sheets and sources are retained.

Pinocchio artwork remains blocked by image-generation rejections. No new narration has been recorded because no narration API key was configured. Measured cue values remain null until real recordings exist. All four manifests explicitly set installable to false.

Read CURSOR_HANDOFF.md for playback rules, including the 260 ms reveal and measured PCM frame cues. Use assemble_narration.py after producing final mono 16-bit 16 kHz page WAVs; it combines six pairs and records exact page boundaries. ASSET_VALIDATION.json records dimensions and hashes for the 72 prepared JPEGs. IMAGE_PROMPTS.json, ADDITIONAL_IMAGE_PROMPTS.json and CINDERELLA_RESUME_PROMPTS.json retain generation prompts.

Thumbelina normal/source-sheet.png is reference-only; the matching edition comes from normal/matched-sheet.png. Cinderella costume continuity corrected in versioned assets; story.json selects the revisions. Earlier artwork is preserved. review.html pairs every page with its exact narration and a true 64×32 panel preview. No board playback has been tested.

Existing Little Red Riding Hood content remains unchanged in the repository. Firmware implementation and installation stay with Cursor.

---
name: video-edit
description: Edit any video into a captioned showcase — transcribe (any language, defaults to large-v3), present a transcript_review.txt for the user to fix mishears BEFORE rendering, then build a HyperFrames composition with liquid-glass caption pills, liquid blob background, liquid morph wipes, optional behind-subject text via background removal, and render the final video. Use whenever the user provides a video file and asks to edit it, caption it, add subtitles, fix existing captions, make a reel/promo/captioned tutorial, or "do the same" pattern as a prior captioned video. Supports English, Hebrew, and any Whisper-supported language. THE PIPELINE PAUSES FOR USER APPROVAL on the transcript before final render — this is the support mechanism for getting captions perfect (especially Hebrew). Pairs with hyperframes, hyperframes-cli, hyperframes-registry, and yuv-frontend-design skills.
---

# Video Edit — Captioned Showcase Pipeline

End-to-end captioned video editor on top of HyperFrames. The user gives you a video; you orchestrate transcribe → review → render and ALWAYS pause for transcript approval before the long render.

## When to invoke

- A path to a video file (mp4/mov/mkv) + a request to "edit", "caption", "add subtitles", "make a reel/promo", "do the same"
- "Fix the captions / Hebrew misspells" — re-enter at the review step on an existing project
- Any captioned tutorial / talking-head / promo build

## Workflow (12 steps)

1. **Probe the source** — `ffprobe` for dimensions, fps, duration, audio.
2. **Scaffold** — `npx hyperframes init <name> --video <path> --non-interactive`. Rename the copied video to `source.mp4`.
3. **Extract audio** — `ffmpeg -i source.mp4 -vn -ac 1 -ar 16000 audio.wav`.
4. **Transcribe** — copy `references/transcribe.py` into the project. Default model `large-v3` (best Hebrew). CUDA usually fails on Windows (missing cuDNN); the script falls back to CPU int8. Force `language="he"` for Hebrew, `language="en"` for English; otherwise auto-detect.
5. **Apply known corrections** — copy `references/corrections-hebrew.md` content into a `corrections.json` at the project root (keys = wrong token, values = correct token).
6. 🛑 **STOP — open the transcript editor and ask the user to review.** Copy `references/make_review.py` into the project and run `python make_review.py`. It applies `corrections.json` to transcript.json AND emits the human-editable `transcript_review.txt`.
   Then **launch the interactive editor**:
   ```bash
   start "" "C:\Users\User\.claude\skills\video-edit\transcript-editor\index.html"   # Windows
   open  "$HOME/.claude/skills/video-edit/transcript-editor/index.html"               # macOS
   ```
   Tell the user to load their `transcript.json` and source video into the editor, fix
   mishears (optional: enable WebLLM for AI suggestions), and save the new
   `transcript_review.txt` back into the project root. Send them the prompt from
   `references/transcript-review-workflow.md`. The editor offers a far better experience
   than Notepad — video-synced segment preview, RTL-aware editing, one-click
   dictionary apply, and optional in-browser LLM suggestions for Hebrew/English mishears.
   Do NOT proceed until they reply "continue" / "render it".
   When the user replies "continue": copy `references/apply_review.py` and run
   `python apply_review.py`. It re-tokenises edited lines and redistributes word timings
   back into `transcript.json` so caption sync still works.
7. **(Optional) Background removal** — if any talking-head segment needs behind-subject text, extract the segment as `outro.mp4` (or `intro.mp4`) and run `npx hyperframes remove-background <clip>.mp4 -o <name>_subject.webm --quality best`. CPU only on most setups (~3–8 min for a ~15s 1440p clip).
8. **Re-encode source with dense keyframes** — multi-worker render seeks freeze on sparse keyframes. Always run:
   ```bash
   ffmpeg -y -i source.mp4 -c:v libx264 -preset medium -crf 18 -r 30 -g 30 -keyint_min 30 -sc_threshold 0 -pix_fmt yuv420p -movflags +faststart -c:a copy footage.mp4
   ```
9. **Re-load the (edited) transcript** and generate the body sub-composition via `references/gen_body.py`. The generator emits the full `compositions/components/caption-body.html` with editorial + matrix alternating in liquid-glass pills, anchored lower-left-of-centre (clears bottom-right webcam PiPs).
10. **Wire the host `index.html`** from `references/host-template.html`. Layer order (z-index, NOT track-index):
    - z0: footage `.cam-bg`
    - z1: liquid blob background (`compositions/liquid-blobs.html`, `mix-blend-mode: screen`, full duration)
    - z2: parallax behind-subject caption (intro and/or outro, when bg-removal used)
    - z3: subject cut-out `.cam-out` / `.cam-sub` (with matching `data-media-start`)
    - z6: body captions
    - z46: progress bar + flash + liquid morph wipe
11. **Lint** — `npx hyperframes lint`. Must be 0 errors. Common fixes: GSAP/CSS transform conflict on the wipe element (use `xPercent/yPercent` or remove the CSS transform); overlapping tweens on the same property (add `overwrite: "auto"`).
12. **Render** — `npx hyperframes render --quality standard --fps 30 --output renders/<name>_FINAL.mp4`. Standard is the right delivery target — `high` roughly doubles render time. Verify with 6–8 spot-check frames from across the timeline before reporting done.

## Critical rules

- **Never render the final without explicit transcript approval.** The review step is the whole point.
- For Hebrew: `large-v3` + `language="he"` + `direction: rtl` + Rubik (700 + 900 for editorial dual-weight emphasis).
- Caption pills always need an opaque dark backing — bare light text vanishes on white app UI.
- Centre caption pills horizontally but shift the centre x-coord left (e.g. `left: 720px`) when the footage has a bottom-right webcam PiP.
- The behind-subject cut-out clip MUST carry `data-media-start` matching its `data-start` (or matching the offset from the source if the clip was extracted), or the cut-out plays from frame 0 and desyncs.
- The `remove-background` webm keeps the original RGB and writes only the alpha mask — `ffprobe` reports `yuv420p`, which looks like "no alpha". Confirm via `TAG:ALPHA_MODE=1` or composite over a solid colour.
- Outro/end cards with burned-in text — do NOT caption over them; they collide.

## File references

| File | Purpose |
| --- | --- |
| `transcript-editor/index.html` | **Interactive browser editor** — video preview, RTL editing, dictionary apply, optional WebLLM AI suggestions, saves `transcript_review.txt` |
| `references/setup.md` | Prerequisites + install commands for Node / Python / FFmpeg / faster-whisper |
| `references/transcribe.py` | faster-whisper transcribe with CPU fallback + word timestamps |
| `references/make_review.py` | Apply corrections + emit `transcript_review.txt` for the user to edit |
| `references/apply_review.py` | Parse edited review file, redistribute word timings, update `transcript.json` |
| `references/gen_body.py` | Caption-body generator (editorial + matrix in liquid-glass pills) |
| `references/host-template.html` | Full host composition with liquid effects + transition wipe |
| `references/liquid-blobs.html` | Full-duration drifting blob layer |
| `references/caption-parallax-outro.html` | Behind-subject caption template (English; clone for other languages) |
| `references/corrections-hebrew.md` | Known Hebrew Whisper mishears |
| `references/transcript-review-workflow.md` | The pause/approve step in detail |

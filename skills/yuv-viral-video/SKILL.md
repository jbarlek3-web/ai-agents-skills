---
name: yuv-viral-video
description: Edit raw selfie or screen-share footage into a viral short-form video in YUV.AI's signature style — Apple-style liquid-glass cards, dark-mode polish, MrBeast-paced cuts, neuroscience-friendly hooks, video-title karaoke captions, real backdrop blur, no fake content. Hebrew = Rubik Black, English = Anton uppercase. Always renders BOTH 9:16 and 16:9, always saves with _V<N> backup suffix. Trigger on requests to edit a video, make a viral cut, create Reels/TikTok/Shorts/YouTube content, or anything mentioning the source footage by path. Trigger on Hebrew terms like ערוך סרטון, סרטון ויראלי, להפוך לוויראלי, לקצר סרטון, ריל, שורט. Trigger when the user drops a path to an .mp4/.mov/.mkv and says "edit this." Do NOT use for podcast-style audio-only edits, or for non-Hebrew/English content (the styling, fonts, and BiDi handling are tuned for HE+EN).
---

# Yuv-Viral-Video

The complete style + pipeline that turns Yuval's raw footage into shippable shorts. Built incrementally from real edits across the `0423.mp4` (screen-share + speaker PIP) and `tt.mp4` (selfie) projects, with every painful lesson encoded as a hard rule.

## When to consult this skill

Any time the user drops a video file and says "edit this" / "make it viral" / "turn this into a short" / "ערוך לי את זה". Even a one-line ask like *"take this and edit it: C:\path\foo.mp4"* should trigger the full flow below. Don't ask for creative direction up front — Yuval's style is captured in the **Hard Rules** and the worked examples; just execute and iterate from feedback.

## Three things to internalize before touching ffmpeg

**1. NEVER invent content.** Every word on every card must trace to something the speaker actually said in the transcript. No "$$$" placeholders, no "100% הבנה" if they didn't say it, no "לינק בביו" if no link was mentioned. Yuval will catch it instantly and trust collapses fast. When in doubt, copy the literal Hebrew quote into the card.

**2. NEVER cover the speaker's face.** Position cards in the *opposite* half of the frame from the face, or use a top/bottom banner that sits above/below the face zone. For a full-frame selfie, the safe zones are y=0–400 (top banner) and y>1500 (bottom). For screen-share footage with the speaker in a corner PIP, cards live anywhere in the screen-content area.

**3. NEVER non-uniformly scale the speaker.** Source PIP aspect must equal target PIP aspect. If you scale a 470×460 source crop into a 920×580 box, the speaker comes out horizontally squished and Yuval will tell you it looks like garbage. Pick target dims that match source aspect, or use `force_original_aspect_ratio=decrease` + pad/center.

Everything below is a worked example or a tooling detail. The three above are non-negotiable.

## The pipeline (high-level)

```
source.mp4
   ↓  transcribe (ElevenLabs Scribe via the video-use skill)
transcript.json (word-level timestamps)
   ↓  pick word-snapped beats → edl.json
ranges with start/end (50ms head, 80ms tail padding, snap to word boundaries)
   ↓  build base.mp4 (per-aspect, per-segment extract + motion + grade + concat)
base_9x16_V<N>.mp4, base_16x9_V<N>.mp4
   ↓  render Apple-glass cards (PIL) with rounded masks
cards_9x16/, cards_16x9/  (paired card.png + card_mask.png + animation seqs)
   ↓  generate karaoke ASS (Hebrew = Rubik, English = Anton, video-title pop)
karaoke.ass, karaoke_16x9.ass
   ↓  composite (ffmpeg filter_complex)
   :   gblur sigma=24 backdrop → split → alphamerge with mask → overlay rounded blur
   :   → overlay scale-pop card on top → animations on top → subtitles LAST → loudnorm
final_9x16_V<N>.mp4, final_16x9_V<N>.mp4
```

## Hard Rules (the editor's bill of rights)

These are correctness rules. Deviation produces silent failures or angry users. Memorize them.

1. **Hebrew = Rubik Black. English = Anton uppercase, bold, thick.** Never mix. Never substitute. The avatar letter "א" in Anton renders as a hollow X — that's why Hebrew letters must use Rubik. Helpers/`apple_glass.py` defaults to Rubik for Hebrew strings via `python-bidi`.
2. **Subtitles are applied LAST in the filter chain.** After every overlay and animation. Otherwise overlays cover the captions.
3. **Per-segment extract → `-c copy` concat.** Single-pass filtergraphs cause double-encode of every segment. The video-use skill enforces this; mirror it.
4. **30 ms audio fades at every segment boundary.** `afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03`. Without this, audible pops at every cut.
5. **Word-boundary snapping.** All cut edges must come from the Scribe transcript's `word.start` / `word.end`. Plus 50 ms head, 80 ms tail padding. Tighter for fast pacing, looser for cinematic.
6. **Cache transcripts.** Never re-transcribe the same source. Scribe costs money.
7. **All Hebrew text in PIL goes through `bidi.get_display()`.** PIL has no built-in BiDi engine, so without this Hebrew comes out reversed. The shared `apple_glass.py` exposes `rtl()` — use it everywhere.
8. **Even pixel dimensions.** ffmpeg's `yuv420p` chroma subsampling requires even W and H. A target like 470×345 → ffmpeg silently crops to 470×344 → alphamerge fails with "Input frame sizes do not match (352x344 vs 352x345)". Always design with even dims.
9. **Aspect preservation on the speaker.** As above — no horizontal squish.
10. **NEVER make up content.** Audit every string against the transcript before render.
11. **Save every render with `_V<N>.mp4` suffix.** Each iteration writes a new versioned file (`final_9x16_V8.mp4`, `_V9.mp4`, etc.) so the user keeps backups. Never overwrite a previous final.
12. **All session outputs in `<videos_dir>/edit/`.** Never write inside the skill directory.

## Layout decisions (the most important call you make)

The first decision after transcribing is **what the source footage actually is**. There are two archetypes:

### Archetype 1 — "Screen-share with speaker PIP corner" (e.g. `0423.mp4`)

Source: 16:9 with a screen recording (browser, app, dashboard) filling most of the frame, and the speaker's webcam in a small corner PIP (typically bottom-right ~470×460 inside a 2560×1440 source).

**The screen content IS the visual story.** Hide it and the user gets angry. The composition rule:

| Output | Top zone (screen content) | Bottom / corner zone (speaker PIP) | Card real estate |
|--------|---------------------------|------------------------------------|------------------|
| 9:16 (1080×1920) | Top 2/3 (1080×1280) — crop 1215×1440 from x=660, scale to 1080×1280 | Bottom 1/3 — crop 470×460 PIP, scale to 600×588 (preserving aspect), rounded 56px corners, dark fill below | Floating glass cards in top 2/3, key-moment strip at y≈1180 (just above PIP) |
| 16:9 (1920×1080) | Full frame: scale source 2560×1440 → 1920×1080. PIP naturally lands at ~1530×712 size 352×344. | Round the existing PIP corners with a 36-radius alphamerged mask | Cards on left half (x=60–1140, y=80–820), key-strip across bottom |

### Archetype 2 — "Full-frame speaker / selfie" (e.g. `tt.mp4`)

Source: vertical or horizontal with the speaker filling the frame the entire time. There's no "screen" beyond the speaker themselves. **The speaker IS the content** — don't shrink them to a tiny corner; the user explicitly asked for them to stay prominent.

| Output | Speaker placement | Card real estate |
|--------|-------------------|------------------|
| 9:16 (1080×1920) | Full-frame: scale source to 1080×1920 directly | **Top banner only** (x=40–1040, y=80–460). Never side-cards on a full-frame selfie — they'll cover the face. |
| 16:9 (1920×1080) | Letterbox: crisp speaker scaled to 607×1080 centered, with a heavily-blurred (sigma=22) zoomed copy of the source filling the rest | Cards on left half (x=60–1140, y=80–820) — they sit on the blurred BG, not on the speaker. |

If the source is HYBRID (some beats are full speaker, others screen-share), pick the archetype per beat. `0423.mp4`'s HOOK beat (~1.8 s) is full-speaker; everything else is screen-share. Set `"layout": "A"` or `"layout": "B"` per range in `edl.json`.

## Apple-style liquid-glass cards

The card style is non-negotiable: rounded corners (`radius` 36–56), backdrop gaussian blur via `gblur sigma=24`, semi-translucent white tint at ~15 % alpha, top inner highlight gradient, 1 px white border at 110/255 alpha, and a soft drop shadow below.

The trick that makes them look like Apple-style frosted glass (not a flat semi-transparent rect) is **masked backdrop blur**:

```
[0:v] gblur=sigma=24, format=rgba, split=N → [bl0]…[blN-1]   # one blurred copy per glass card
for each card i with mask M_i:
  [M_i:v] format=gray → [m_i]
  [bl_i] [m_i] alphamerge → [rb_i]                          # blur cropped to rounded shape
  [base] [rb_i] overlay=0:0 enable=between(t, st_i, en_i) → [base+blur]
  [card_png_i] format=rgba, scale-pop, fade-in/out, setpts shift → [c_i]
  [base+blur] [c_i] overlay=center enable → [base'']
```

The mask PNG is a full-canvas grayscale image where white=card-shape, black=outside. Generate via `apple_glass.make_glass_mask()`. Each card gets its own `*.png` (RGBA content) and `*_mask.png` (grayscale shape). See `scripts/apple_glass.py`.

**Why split the blur?** Multiple `crop` operations on one stream serialize. Pre-splitting once gives N independent rounded-blur regions for N cards.

**Why `alphamerge` and not `crop` then overlay?** `crop` produces a rectangular blurred patch; the rectangle's corners would leak past the card's rounded shape. `alphamerge` with the mask shapes the patch's alpha to match the card exactly.

## Karaoke (video-title style)

Per-word ASS dialogues. Each word pops in with `\fscx150\fscy150\t(0,140,\fscx100\fscy100)` and `\fad(60,80)`. Active accent words (`מטורף / טירוף / אוטומטית / גדול / גרפיקות / ננו / בננה / חדש / מצליחים / מיינדסט / לשלם`) get a yellow color override + small rotation jitter for emphasis.

**Position depends on layout.**
- 9:16 screen-share (PIP at bottom): `MarginV=40` (caption rides the bottom of the speaker PIP). Font 108 pt HE / 124 pt EN.
- 9:16 full-speaker selfie: `MarginV=40` from bottom (over the speaker's chest, never their face).
- 16:9 screen-share or selfie: `MarginV=80` from bottom, `MarginR=440` (constrains to left 1480 px so it doesn't overlap a right-side speaker PIP).

**Encoding gotcha for libass on Windows:** ASS path passed to `subtitles=` filter must escape the colon → `subtitles='C\:/Users/.../karaoke.ass':fontsdir='C\:/Users/.../fonts'`. Forward-slash everything, backslash-escape every `:`.

**English brand tokens stay English.** The regex `^[A-Za-z][A-Za-z0-9-]*$` detects English/brand words and routes them to the EN style (Anton, uppercase). Hebrew flows through libass+FriBidi for RTL.

## Per-segment dynamic motion

Every segment gets a subtle MrBeast-style camera move baked into the extract. Valid kinds and amounts:

| Kind | Effect | Typical amount |
|------|--------|----------------|
| `push_in` | Slow zoom in | 0.04–0.07 |
| `pull_out` | Slow zoom out (revealing) | 0.05–0.07 |
| `snap_in` | Cubic ease-out punch zoom | 0.05–0.10 |
| `dolly_l` / `dolly_r` | Held zoom + horizontal drift | 0.04 |
| `hold` | No motion (use sparingly — for chip cards / clarity moments) | – |
| `shake` | First-300ms jitter then settle (only WOW-class moments) | 0.16 |

ffmpeg expression for `push_in` over duration `d`:
```
,scale=w='W*(1+a*min(t/d,1))':h='H*(1+a*min(t/d,1))':eval=frame:flags=bicubic
,crop=W:H:'(iw-W)/2':'(ih-H)/2':exact=1
```

Keep amounts subtle. The user notices anything ≥0.10 as "too much zoom" outside of WOW beats.

## Bottom key-moment strips

A small glass strip across the bottom of the frame summarising the current beat in 1–4 words. Hebrew on the right (RTL), English on the left (Anton uppercase), yellow accent stripe. Appears only on key beats (HOOK, REVEAL, METRICS, AUTO, NANO, WOW, CTA — not every single beat).

For 9:16 the strip lives at y=1170 (just above the speaker PIP top at y=1300). For 16:9 at y=920 (just above the bottom edge).

## Real animated diagrams (no fake data)

**Bar chart (METRICS-class beats):** 4 horizontal bars sized by hard-coded `target_ratio = [0.92, 0.72, 0.52, 0.95]`, NOT by fake numbers. Each bar gets a horizontal gradient (lighter at the inner end), a soft glow, and a stagger entrance with `ease_out_back`. Labels are the actual category names from the transcript (`המרות / הוצאות / תקציבים / קליקים`). Never display "1,247" / "$48K" / "12" / "89,432" — Yuval will call out the fake placeholder data immediately.

**Flow diagram:** glowing brand-color circular nodes (META blue, CLAUDE orange, AUTO yellow, RESULTS green) connected by animated yellow dashed arrows. Each node pops in with `ease_out_back`, the arrow draws between them with `ease_out_cubic`, and the dashes "flow" by phase-shifting the dash start each frame: `phase = (fi * 4) % 22`.

Both are rendered as 36-frame PNG sequences (1.2 s @ 30 fps) and extended via `tpad=stop_mode=clone:stop_duration=<rest>` to fill the rest of the beat.

## SFX library

Generated via ElevenLabs sound-generation API. Standard kit:
- `impact.mp3` (0.7 s) — HOOK punch + WOW slam
- `bass_drop.mp3` (0.7 s) — layered with impact for HOOK boom
- `whoosh.mp3` (0.5 s) — every cut transition
- `riser.mp3` (1.2 s) — building into WOW
- `ding.mp3` (0.5 s) — UI pop on card reveals + per-bar dings on bar-chart entrance
- `glitch.mp3` (0.5 s) — short transition glitch
- `typing.mp3` (1.4 s) — under any terminal/coding card

Mixed via `[a0][s0]…[sN]amix=inputs=N+1:normalize=0:duration=first`. Each SFX gets a `volume=0.4–0.65` and an `adelay=ms|ms` to land at the right output time.

## Versioning

**Every render writes a NEW file.** Find the highest existing `final_9x16_V<N>.mp4` and increment. The composite scripts split `BASE_VERSION` (read from) and `OUT_VERSION` (write to) so the base can be reused across multiple final iterations.

```python
# composite skeleton
BASE_VERSION = 8         # which base.mp4 to read
OUT_VERSION  = 9         # which final.mp4 to write (always > previous)
BASE_V = EDIT / f"base_9x16_V{BASE_VERSION}.mp4"
FINAL_V = EDIT / f"final_9x16_V{OUT_VERSION}.mp4"
```

## Common failure modes (and the fixes)

- **"Input frame sizes do not match (X vs Y)"** → odd target dimension. Round to even pixels for both W and H.
- **Hebrew letters render reversed** → Hebrew strings in PIL not wrapped in `bidi.get_display()`. All paths through `apple_glass.draw_text_safe` should use `rtl()` first.
- **Hebrew avatar letter renders as hollow X** → using Anton font for a Hebrew character. Anton is Latin-only. Switch to Rubik for any text containing Hebrew.
- **`Filter 'split' has output 0 unconnected`** → declared a split but didn't consume one of its outputs. Check labels match.
- **Speaker looks horizontally squished** → non-uniform scale on the PIP source crop. Match target aspect to source aspect.
- **Backdrop blur leaks past rounded card corners** → using `crop`+`overlay` instead of `alphamerge` with a rounded mask.
- **`subtitles=` filter fails on Windows** → unescaped colon in the path. Escape with `\:`.
- **`-shortest` ignored** → `-loop 1` on a PNG creates an infinite stream, and the looped input may not be terminated. Add `-t <dur>` to constrain the looped input too.
- **`-t` doesn't limit source duration** → `-t` is an *input option* and must come BEFORE the `-i` it applies to, not after. After `-i SRC` it applies to the *next* input.

## File layout (per project)

```
<videos_dir>/edit/
├── transcripts/<source>.json          (cached Scribe output)
├── edl.json                           (cut decisions, layout per range)
├── cards_9x16/                        (Apple-glass cards + masks + anim sequences)
│   ├── reveal.png, reveal_mask.png
│   ├── platforms.png, platforms_mask.png
│   ├── km_*.png, km_*_mask.png        (key-moment bottom strips)
│   ├── anim_metrics/{0001..0036}.png  (bar chart sequence)
│   └── anim_flow/{0001..0036}.png     (flow diagram sequence)
├── cards_16x9/                        (same shape, different dims)
├── karaoke.ass, karaoke_16x9.ass
├── sfx/                               (impact, bass_drop, whoosh, riser, ding, glitch, typing)
├── fonts/Anton-Regular.ttf, Rubik-Black.ttf, Rubik-Bold.ttf
├── base_9x16_V<N>.mp4, base_16x9_V<N>.mp4
└── final_9x16_V<N>.mp4, final_16x9_V<N>.mp4
```

## Setup

See `references/setup.md` for: ffmpeg, ElevenLabs API key, font download (Anton + Rubik), python-bidi, PIL, fontTools (woff2→ttf converter for Rubik). The setup is mostly inherited from the `video-use` skill which this builds on top of — install that first.

## Scripts

- `scripts/apple_glass.py` — `apple_glass_card()`, `make_glass_mask()`, `make_dark_bg()`, `rtl()`, `COLORS`, layout constants
- `scripts/build_screen_share.py` — base build for Archetype 1 (screen-share + corner PIP)
- `scripts/build_selfie.py` — base build for Archetype 2 (full-frame speaker)
- `scripts/make_cards.py` — card content rendering primitives + key-moment strip builder
- `scripts/make_anims.py` — bar chart + flow diagram PNG sequence generators (no fake numbers)
- `scripts/make_karaoke.py` — word-level ASS karaoke generator (HE = Rubik, EN = Anton)
- `scripts/composite.py` — full ffmpeg filter_complex builder (rounded-mask blur + scale-pop entrances + subs LAST + loudnorm)
- `scripts/make_sfx.py` — ElevenLabs SFX batch generator

## The unbreakable promise

If Yuval drops a video and asks for an edit, the output:
1. Shows the screen content if it's a screen-share (NEVER hide it under dark BG).
2. Shows the speaker prominently if it's a selfie (NEVER shrink to tiny corner).
3. Has every card text traceable to a real spoken word.
4. Renders both 9:16 AND 16:9.
5. Saves with `_V<N>` so the previous version is preserved.
6. Uses Rubik for Hebrew, Anton uppercase for English. Always.
7. Doesn't cover the face. Ever.

Get those right and you've delivered. Anything else is polish.

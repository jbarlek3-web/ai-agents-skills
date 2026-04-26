---
name: yuv-design
description: Yuval Avidani's signature web-design defaults — Anton + Rubik display, Inter + Assistant body, pink/yellow/bone palette, paper grain, warm shadows, asymmetric layouts, GSAP-first motion, RTL/LTR bilingual. Apply automatically to ANY frontend / web request from Yuval — websites, landing pages, dashboards, React components, HTML/CSS, marketing pages, design systems. Trigger words: website, landing page, web UI, React, component, HTML, CSS, frontend, dashboard, marketing page, design system, type, fonts, palette. Hebrew triggers: אתר, דף נחיתה, עיצוב אתר, פיתוח אתר, רכיב, דאשבורד. Override rule — when a project specifies its own brand system, the project wins. These defaults fill the vacuum.
---

# yuv-design

The mandatory web-design defaults for Yuval Avidani. Whenever you build any web surface (a marketing page, a dashboard, a single artifact, a React component) and a brand isn't explicitly specified by the project, these defaults apply. They give Yuval's work a recognizable fingerprint without any per-request copy-paste of fonts or colors.

This skill is the **frontend / web** counterpart to `yuv-viral-video` (which carries the same brand into rendered MP4s).

---

## When this skill applies

- The user is Yuval Avidani.
- The output is a web surface — a `.html` file, a React component, a Next.js page, a dashboard, a marketing site.
- The project hasn't specified its own palette, type system, or brand. (When the project HAS its own system, that wins — these are defaults for the empty state, not overrides.)

---

## Typography — mandatory defaults

### English

| Role | Font | Weight | Treatment |
|---|---|---|---|
| Display / headlines / hero text / CTAs / wordmarks | **Anton** | 400 (only weight) | UPPERCASE always · letter-spacing `-0.03em` to `-0.04em` · line-height 0.9–1.0 |
| Body / UI / paragraphs | **Inter** | 400 / 500 / 600 / 700 | line-height 1.5 · default tracking |

### Hebrew

| Role | Font | Weight | Treatment |
|---|---|---|---|
| Display / headlines / RTL hero text | **Rubik** | 900 (Black) | line-height 0.95–1.05 |
| Body / UI / paragraphs | **Assistant** | 400 / 500 / 600 / 700 | line-height 1.55–1.7 (Hebrew needs more) · `dir="rtl"` on container |

### Mixed bilingual

Stack both fonts in one `font-family` and let the browser route per-glyph:

```css
:root {
  --font-display: 'Anton', 'Rubik', sans-serif;
  --font-body:    'Inter', 'Assistant', sans-serif;
}
```

Latin chars take Anton/Inter, Hebrew chars fall through to Rubik/Assistant. One declaration handles bilingual text.

### Banned

- Serif fonts as defaults
- `system-ui` / default font stack
- Anton on Hebrew text (renders as hollow X — Anton is Latin-only)
- Title Case on display headlines (always uppercase or always lowercase, never mixed)

### Google Fonts import (always)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Assistant:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Rubik:wght@400;500;700;900&display=swap" rel="stylesheet">
```

Drop Hebrew fonts only if the project is English-only AND will never localize.

### RTL setup for Hebrew pages

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
```

```css
.card {
  padding-inline: 2rem;
  margin-inline-start: auto;
  border-inline-start: 2px solid var(--pink);
}
```

Use logical properties (`*-inline-*`) over physical (`*-left`, `*-right`).

---

## Color palette — the signature

```css
:root {
  --pink:       #FF1464;   /* primary brand · CTAs · accents · the thread */
  --yellow:     #E5FF00;   /* accent · dominates when used */
  --black:      #0A0A0A;   /* warm near-black, never blue-black */
  --off-white:  #FAFAF7;   /* paper-feel, replaces pure #FFFFFF entirely */
  --bone:       #F5EEE4;   /* transitional sections, cream */
  --charcoal:   #1A1A1A;   /* primary text on light */
  --warm-gray:  #8B8680;   /* secondary text on light */
  --light-gray: #A8A39D;   /* secondary text on dark */
}
```

### Strict rules

- **Pure `#FFFFFF` is banned.** Use `--off-white`. Page backgrounds, cards, inverted text — all `#FAFAF7`.
- **Blue is banned as a default.** No navy, no slate, no indigo, no cool tones. If the project legitimately requires blue (banking, medical), use it — otherwise warm family only.
- **Pink is the thread.** Logo, primary CTA, section accents. Used consistently across a site is what makes the work recognizable.
- **Yellow dominates when it appears.** Never timid. If yellow shows up, it's a full-bleed background block, a section divider, a hero highlight bar, or a large pull-quote field — not a tiny accent swatch.
- **Gradients only pink → yellow**, on small surfaces only (buttons, text underlines, icon fills). Never a full-page gradient wash.

### Tailwind config

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        pink:        '#FF1464',
        yellow:      '#E5FF00',
        black:       '#0A0A0A',
        'off-white': '#FAFAF7',
        bone:        '#F5EEE4',
        charcoal:    '#1A1A1A',
        'warm-gray':  '#8B8680',
        'light-gray': '#A8A39D',
      },
      fontFamily: {
        display: ['Anton', 'Rubik', 'sans-serif'],
        body:    ['Inter', 'Assistant', 'sans-serif'],
        mono:    ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      maxWidth: { content: '1440px' },
      boxShadow: {
        warm:     '0 8px 32px rgba(255, 20, 100, 0.08)',
        'warm-lg':'0 20px 60px rgba(255, 20, 100, 0.12)',
      },
    },
  },
};
```

Never use the default Tailwind palette names (`slate-*`, `zinc-*`, `gray-*`, `emerald-*`, `cyan-*`, `indigo-*`, `violet-*`, `rose-*`) in Yuval's projects.

---

## Layout & component defaults

| Property | Value | Reason |
|---|---|---|
| Border radius — cards | `0` (Brutalist) **or** `40–56px` (Glassmorphism) | The 8/12/16px "corporate-rounded" middle ground is the strongest AI-template tell on the planet. Avoid. |
| Border radius — pill CTAs | `999px` | Always. |
| Shadows | warm-toned, e.g. `0 20px 60px rgba(255, 20, 100, 0.12)` | Never the default blue-black `rgba(0,0,0,0.1)`. |
| Whitespace | generous | Premium feel comes from restraint, not density. |
| Layout | asymmetric > grid-perfect | Offset columns. Overlapping. One element breaking the grid. |
| Section padding (vertical) | desktop 120–160px · mobile 64–80px | Wide breathing room. |
| Max content width | 1440px centered | Don't stretch full-bleed by default. |
| Icons | Phosphor or Lucide, single-color stroke override | Never multicolor icon sets. |

### Grain texture (always on light backgrounds)

```css
body { background-color: var(--off-white); position: relative; }
body::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

Lift to 0.04 for more pronounced grain, drop to 0.01 for subtler.

---

## Animation defaults

Every animation needs a reason. The site should feel **alive but never restless**. Hovers are deliberate. Reveals are scroll-triggered. Numbers count up on viewport entry. Connecting lines draw themselves.

### Library preferences (in order)

1. **GSAP (https://gsap.com)** — primary. Use SplitText for headline reveals, ScrollTrigger for scroll-driven sequences, MotionPath for paths. Prefer over Framer Motion for non-trivial work — GSAP produces higher-end results and is seekable (matters for Hyperframes capture).
2. **Three.js with React Three Fiber** — for 3D when the project can justify it.
3. **MediaPipe** — for gesture/pose interactions when the project has a signature "wow" moment.
4. **Lottie** — when the designer ships a `.json` vector animation.
5. **CSS-only micro-interactions** — fine for hover states, focus rings, button press. Don't reach for a library.

### Easing vocabulary

| Use | Easing |
|---|---|
| Card entrance / overshoot | `back.out(1.7)` |
| SplitText reveal | `power3.out` or `power4.out` |
| Slam beats / hero punches | `expo.out` |
| Idle floats / breathing | `sine.inOut` |
| Playful springy | `elastic.out(1.2, 0.5)` |
| Mechanical / clinical | `power3.inOut` |

### GSAP SplitText hero reveal (reference)

```js
import gsap from 'gsap';
import { SplitText } from 'gsap/SplitText';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(SplitText, ScrollTrigger);

const split = new SplitText('.hero-headline', { type: 'words,chars' });
gsap.from(split.chars, {
  scrollTrigger: { trigger: '.hero-headline', start: 'top 80%' },
  yPercent: 100,
  opacity: 0,
  duration: 0.8,
  ease: 'power4.out',
  stagger: 0.02,
});
```

---

## Hyperframes compatibility (free insurance)

Yuval often captures sites as video for keynotes, social reels, and marketing. Hyperframes (https://github.com/heygen-com/hyperframes) renders HTML to deterministic, frame-by-frame video.

### Patterns to follow by default

- **Semantic HTML5 elements** (`<section>`, `<article>`, `<header>`, `<nav>`, `<footer>`). Div soup is harder to target for frame capture.
- **Mark video-destined regions:**

  ```html
  <!-- HYPERFRAMES_VIDEO_SLOT: hero -->
  <section class="hero">...</section>
  <!-- /HYPERFRAMES_VIDEO_SLOT -->
  ```

- **Prefer GSAP timelines (seek-driven) over CSS `@keyframes`** when a sequence might later be captured. GSAP can be seeked to an exact time (`tl.seek(2.5)`); CSS keyframes can't reliably.
- **Avoid wall-clock dependencies.** No `Date.now()`, no `setInterval` you can't seek. Use scroll position, explicit GSAP timelines, or `requestAnimationFrame` tied to a deterministic clock.

Not every project will be captured — but these patterns are free.

---

## What NOT to do (explicit defaults to avoid)

- **Stock photography.** No generic business people, abstract cityscapes, Unsplash textures. Prefer abstract geometric, custom-generated, or Yuval's own (Hope cheetah, Marcus lion, AI-generated big cat content) over stock.
- **Emoji in marketing / business / enterprise sites.** Personal blogs, casual projects, social content — fine. Enterprise / client work — no.
- **Soft drop-shadow rounded-corner "template" cards.** Flat white card, 12px radius, `0 4px 6px rgba(0,0,0,0.1)` shadow. The dominant AI-slop visual. Never ship this.
- **Default Tailwind palette names.** Use the custom palette or the project's brand.
- **Multicolor icon sets.** Phosphor / Lucide single-color stroke only.
- **Cookie banners, chat widgets, marketing popups in demos.** Production concerns. Demos stay clean.
- **The "AI-generated feel":** templated layouts, generic hero → features → pricing → footer with no personality. Lorem ipsum. Placeholder text like "Your tagline here." Write real copy or realistic placeholder copy specific to the project.
- **Pure `#FFFFFF`.** Use `#FAFAF7`.
- **Blue as a default accent.** Warm family only unless required.

---

## A starter snippet — English hero

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --pink: #FF1464;
      --yellow: #E5FF00;
      --black: #0A0A0A;
      --off-white: #FAFAF7;
      --charcoal: #1A1A1A;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: var(--off-white);
      color: var(--charcoal);
      line-height: 1.5;
    }
    .hero {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      align-items: center;
      padding: 120px 80px;
      max-width: 1440px;
      margin-inline: auto;
    }
    .hero h1 {
      font-family: 'Anton', sans-serif;
      font-size: clamp(4rem, 9vw, 10rem);
      text-transform: uppercase;
      letter-spacing: -0.04em;
      line-height: 0.9;
    }
    .hero h1 em { font-style: normal; color: var(--pink); }
    .cta {
      display: inline-block;
      margin-top: 3rem;
      padding: 1.25rem 2.5rem;
      background: var(--pink);
      color: var(--off-white);
      font-family: 'Anton', sans-serif;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      border-radius: 999px;
      text-decoration: none;
      font-size: 1.125rem;
    }
  </style>
</head>
<body>
  <!-- HYPERFRAMES_VIDEO_SLOT: hero -->
  <section class="hero">
    <div>
      <h1>Fly high<br>with <em>yuv.ai</em></h1>
      <a href="#" class="cta">Start learning</a>
    </div>
    <div><!-- right column reserved for image / 3D / animation --></div>
  </section>
  <!-- /HYPERFRAMES_VIDEO_SLOT -->
</body>
</html>
```

---

## A starter snippet — Hebrew RTL

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;500;600;700&family=Rubik:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    :root { --pink: #FF1464; --yellow: #E5FF00; --off-white: #FAFAF7; --charcoal: #1A1A1A; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Assistant', sans-serif;
      background: var(--off-white); color: var(--charcoal);
      line-height: 1.6;
    }
    .hero { padding-block: 120px; padding-inline: 80px; max-width: 1440px; margin-inline: auto; }
    .hero h1 {
      font-family: 'Rubik', sans-serif;
      font-weight: 900;
      font-size: clamp(3rem, 7vw, 8rem);
      line-height: 1;
    }
    .hero h1 em { font-style: normal; color: var(--pink); }
    .cta {
      display: inline-block;
      margin-block-start: 2rem;
      padding-block: 1rem;
      padding-inline: 2rem;
      background: var(--pink);
      color: var(--off-white);
      font-family: 'Rubik', sans-serif;
      font-weight: 700;
      border-radius: 999px;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <section class="hero">
    <h1>תעוף גבוה<br>עם <em>yuv.ai</em></h1>
    <a href="#" class="cta">בואו נתחיל</a>
  </section>
</body>
</html>
```

---

## One-line self-check before shipping

1. No `#FFFFFF` anywhere — replaced with `#FAFAF7`.
2. No default Tailwind color classes (`slate-*`, `zinc-*`, `indigo-*`, etc.).
3. Anton is uppercase with negative letter-spacing wherever it appears.
4. Hebrew pages have `dir="rtl"` on `<html>` and use logical CSS properties.
5. No 8px or 12px border radius — `0`, `999px`, or 40–56px (glass cards) only.
6. Shadows are warm-toned, not blue-black.
7. If the project involves Hebrew, both Hebrew font pairs (Rubik + Assistant) are loaded.
8. GSAP is used for any non-trivial motion (not Framer Motion / pure CSS keyframes).

If any of these fail, fix before delivering.

---

## Companion skill

For video output (rendered MP4), use [`yuv-viral-video`](../yuv-viral-video/) — same brand system, video-tuned hex values, same Anton+Rubik display fonts, but optimized for H264 rendering through Hyperframes.

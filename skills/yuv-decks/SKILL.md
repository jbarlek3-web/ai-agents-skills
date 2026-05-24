---
name: yuv-decks
description: Build cinematic, journey-themed presentation decks in Yuval Avidani's signature style using @open-slide/core. The user describes a topic and audience; this skill scaffolds an open-slide project, drafts the 4-act narrative arc (Boarding → Ascent → Cruise → Descent), writes every slide in the Yuval voice (plain-language, no jargon, story-driven), applies the sky-themed cinematic visual language, and orchestrates companion skills for hero images and video moments. Triggers on "make a deck", "create slides", "build a presentation", "build a deck", "new deck", "presentation about", "talk deck", "hackathon deck", "open-slide deck", "yuv-decks", "yuv deck", "deck like Yuval", "מצגת", "שקפים", "דק", "מצגת על", "להכין מצגת". Use proactively whenever the user asks for ANY slide-based presentation; the skill self-selects the right scope.
---

# yuv-decks — Build Yuval Avidani-style cinematic decks

A complete playbook for creating presentation decks that match Yuval's signature style: **eye-level voice, cinematic flight metaphor, story-driven case studies, real citations, zero jargon, and a unified visual language across every slide.**

This skill is the distillation of building "Build Agents That Ship" for the NICE pre-hackathon (May 2026). Read it end-to-end before drafting any slides.

**Reference implementation**: <https://github.com/hoodini/build-agents-that-ship> (private — contains the 24-slide deck this skill was extracted from).

---

## When to invoke this skill

The user wants a *talk* or *presentation* deck. Triggers:

- "Make me a deck about X"
- "Create slides for a talk on Y"
- "Build a presentation for the [company] hackathon"
- "I'm presenting about Z — help me build the deck"
- "מצגת על..." / "שקפים על..." / "דק על..."

Do NOT invoke for: a single landing page, a video, a document, a Google Slide PowerPoint export. This skill is for **open-slide React decks** rendered at 1920×1080 with cinematic motion.

---

## Step 0 — Bootstrap the project

```bash
# Pick a slug. Lowercase, hyphenated, descriptive.
npx @open-slide/cli init <deck-slug>
cd <deck-slug>
npm install
npm run dev   # starts the preview at http://localhost:5173
```

The scaffold creates `slides/getting-started/` (a demo). You will create your own slide under `slides/<deck-id>/index.tsx` and delete or ignore the demo.

---

## Step 1 — Scope the deck (ASK BEFORE WRITING)

Before drafting, lock in these four decisions via a single `AskUserQuestion` (multi-question form):

1. **Topic & audience** — what is the deck *for*, and *who* will be in the room? Get the customer's actual agenda if possible (literal bullets they expect to hear) — match 1:1.
2. **Page count** — Short (5–6), Standard (8–10), Deep dive (12–24).
3. **Language** — English / Hebrew / Bilingual. Yuval is bilingual; pick based on audience.
4. **Speaker context** — Is Yuval the presenter? Is this for a specific company (NICE, etc.)? Knowing the host lets you craft callback moments ("…yes, the company you're sitting in…").

Do NOT skip this step. Every redirect later in the build traces back to a wrong assumption here.

---

## Step 2 — The Yuval Voice (non-negotiable rules)

All copy follows these three rules:

### Rule 1 — Plain language, never jargon
Replace every term that isn't a household word:

| Don't say | Say instead |
|---|---|
| EBIT | real profit |
| PoC | the prototype / the demo phase |
| BYOC | your own cloud |
| service-account-as-god | admin-token-for-everything |
| RAG | lookup before answering |
| fine-tuning | training the model on your data |
| vLLM | local LLM runner |

If a *name* must stay (LiteLLM, Bedrock, Anthropic, Cognigy) — keep it, but **define it in 3 words on first mention** ("LiteLLM — an AI gateway library").

### Rule 2 — Short sentences. Punchy fragments. Like this.
Maximum **8–12 words per bullet**. Cut all "thus / therefore / however." If a sentence wraps to 3 lines, split or shorten.

**Calibration test** — transform this BEFORE writing any draft:

> ❌ "When Watson got a recommendation wrong, nothing learned from it. Same mistakes, repeated for years. The system never improved with use."
>
> ✅ "Watson made a mistake. Watson kept making it. For years."

### Rule 3 — Define every name on first mention
"Watson is IBM's AI. Won Jeopardy in 2011. Then aimed at hospitals."
"Klarna is Sweden's biggest fintech — Buy Now Pay Later, 150M customers."

Never assume the audience knows who/what.

---

## Step 3 — The Narrative Arc (4 acts)

The structure that survives audiences:

```
ACT I · BOARDING — The Stakes              (slides 1–4)
  Cover · Hook stat · Sources agree · Failure patterns

ACT II · ASCENT — The Stories              (slides 5–9)
  Failure case story · Why it failed (4 bullets) ·
  Success case story · Why it worked (4 bullets) ·
  Reference example (real product the audience knows)

ACT III · CRUISE — The Build               (slides 10–22)
  Anatomy · Agent types · MCP · Multi-agent · Where to apply ·
  Client stack · Server infra · Gateway · Routing · Tracking ·
  Optimization · Evals · MVP → Production

ACT IV · DESCENT — The Action              (slides 23–24)
  How to start tomorrow · Closing
```

**Structural laws:**
- Case studies CLUSTER together (slides 5–9). Don't interleave with considerations.
- Each case study is **TWO slides**: the *story* + the *lessons* (4 specific failure points or success moves). The lessons slide is where "aha tokens drop."
- Stories BEFORE considerations. The audience needs *why it matters* before *how to do it*.
- Cut anything not in the customer's agenda — even if you love it. (Examples cut in the NICE deck: ROI math, Mgmt Pitch, Skill-vs-Agent-vs-Feature-vs-Product, Obsolescence Check.)

---

## Step 4 — Case Study Triplet (failure + success + reference)

Always anchor with three **real, public, verifiable** stories:

| Role | What it is | Example used in the NICE deck |
|---|---|---|
| **Failure** | The most-funded, most-public AI/enterprise project that crashed. Name the *specific* failure points. | IBM Watson Health ($4B over 11 years, 0 patients helped) |
| **Success-with-caveat** | A real success that had to course-correct. Shows wins need humility. | Klarna AI Assistant (replaced 700 FTEs, then partly rehired) |
| **Reference** | A current production example the audience *already knows or owns*. **Bonus**: the company hosting the talk. | NICE Cognigy (NICE acquired it 2024) |

**Verifiable stats for the stakes act** (memorize these — they're real and citable):

- **MIT NANDA** "State of AI in Business 2025" (Aug 2025): **95% of GenAI pilots fail** to deliver measurable P&L impact.
- **Gartner** (mid-2024 forecast): **30%** of GenAI projects abandoned after PoC by end of 2025.
- **BCG** "Build for the Future 2024": **26%** of companies actually generate value from AI.
- **McKinsey** State of AI 2024–2025: **1 in 4** organizations see real profit from generative AI.
- **STAT News** + **University of Texas System Audit** (2017) for IBM Watson Health.
- **Klarna press release** (Feb 27, 2024) + Bloomberg/Fortune coverage (May 2025).

**Never fabricate a stat.** If you don't have a citation, use a *rule of thumb*, not a number with a fake source.

---

## Step 5 — Visual Language (the sky-themed cinematic flight metaphor)

Every deck shares the same visual vocabulary. The deck must FEEL like a flight.

### Palette
```ts
const design: DesignSystem = {
  palette: {
    bg: '#dceaf6',        // sky-blue base
    text: '#1a1814',      // charcoal
    accent: '#ff3b8a',    // hot pink — the trail color
  },
  fonts: {
    display: '"Anton", "Impact", "Helvetica Neue Condensed", system-ui, sans-serif',
    body: '"Inter", system-ui, -apple-system, sans-serif',
  },
  typeScale: { hero: 168, body: 36 },
  radius: 6,
};

const palette = {
  ...design.palette,
  yellow: '#ffd76e',      // soft sun
  cloudWhite: '#ffffff',  // card fill
  skyDeep: '#7ab0d4',
  warmGray: '#6b7a8a',
  red: '#c8403d',         // failure indicators
  green: '#2f7d4f',       // success indicators
  shadow: 'rgba(80, 120, 180, 0.20)',
  hairline: 'rgba(26, 60, 100, 0.18)',
};
```

### Typography
- **Display**: Anton — heavy condensed, ALL CAPS, sized 80–200px. Loaded via Google Fonts `@import` inside a `<style>` tag (no npm deps).
- **Body**: Inter — weights 500–700, sized 14–32px, letter-spacing 0.18–0.28em on small caps.
- **Mono** (for formulas/code): JetBrains Mono.

### The journey indicator (on every slide, top edge)

This is the **single most powerful unifying element**. Thin dashed flight-route line from "DEPART · [host company]" to "ARRIVE · [outcome]". Pink solid trail fills as you progress through the deck. A small ✈ airplane icon sits at the current position with **dynamic pitch**:
- Act I Boarding → 90° (level, taxiing)
- Act II Ascent → 58° (nose up, climbing)
- Act III Cruise → 90° (level, cruise)
- Act IV Descent → 115° (nose down, descending)

Three terminal-dots mark the act boundaries. Phase label below the bar: `II · ASCENT 2/4`.

### Cinematic backgrounds
Every non-video slide gets a **full-bleed nano-banana image at 100% opacity** with:
- A Ken Burns pan animation (`yuv-cinematic-pan`, 22s, `scale 1.04 → 1.06`, `translateX ±12px`)
- A directional bone-wash gradient (`textZone: 'left' | 'right' | 'bottom'`) keeping the text readable where it lives
- White content cards floating on top of the cinematic image

### Page entrance animation
```css
@keyframes yuv-page-enter {
  0%   { opacity: 0; transform: scale(1.06); filter: blur(10px); }
  60%  { opacity: 1; }
  100% { opacity: 1; transform: scale(1); filter: blur(0); }
}
```
Every slide enters with a 0.65s scale-and-defocus. Feels like a film cut.

---

## Step 6 — Companion skills (when to invoke which)

This skill orchestrates other skills. Invoke them at the right moment:

| Skill | When to invoke | What it does |
|---|---|---|
| **yuv-design** | At the start, for fonts, palette, motion fundamentals beyond what this skill specifies. | Yuval's full design system (typography pairings, signature elements). |
| **nano-banana-pro** (or `anthropic-skills:nano-banana-2`) | After Step 5 — to generate cinematic hero/atmospheric images for every major slide. **Requires `GEMINI_API_KEY`.** | Image generation. Use the prompt template below. |
| **hyperframes** | For 4–5 high-impact video moments (cover intro, big-number reveal, case-study timelines, closing flourish). | HTML/CSS/GSAP video composition → renders to MP4 embedded as `<video>` in the slide. |
| **mermaid-diagrams** | For technical architecture diagrams when SVG is heavier than needed. | Clean flowcharts/sequence diagrams. |
| **Excalidraw MCP** (`create_view`) | For live-in-chat hand-drawn workflow diagrams you can show the user during design discussion. | Interactive Excalidraw rendering. |
| **video-edit** / **yuv-viral-video** | If the talk includes pre-recorded selfie footage that needs to be embedded. | Video editing pipeline. |

### nano-banana prompt template (memorize this exact structure)

```
[Scene description — 1–2 sentences, 16:9 cinematic frame, single focal subject]

STYLE: Cinematic editorial poster meets aviation-noir aesthetic. Vibrant. Luminous.
Dark moody background with neon-glow accents. Hot pink (#ff3b8a) as primary luminous
accent, soft sun yellow (#ffe066) as warm glow, sky blue (#7ab0d4) deep tones,
charcoal (#1a1814) shadows. Sharp lighting contrast. Generous space for typography
overlay. Movie poster, not infographic. NO TEXT. NO LOGOS. NO READABLE LETTERS.
```

Always: single focal subject (not a montage), one third of the frame as quiet sky for typography, explicit NO-TEXT instruction.

---

## Step 7 — open-slide rules (hard constraints)

These are non-negotiable from the open-slide framework:

- **Canvas**: 1920×1080 FIXED. Use absolute pixel values (no `rem`, no `vh`, no `%` for type).
- **Files**: Every deck under `slides/<kebab-case-id>/index.tsx`. Assets under `slides/<id>/assets/`. Do NOT touch `package.json`, `open-slide.config.ts`, or sibling slides.
- **Dependencies**: Only `react` and standard web APIs. No GSAP, no Framer Motion, no Tailwind. Use CSS keyframes inside an injected `<style>` tag. Use Google Fonts via `@import` in the same `<style>`.
- **Export contract**: `export default [Page1, Page2, …] satisfies Page[]` and optional `export const meta: SlideMeta = { title: '…' }`.
- **Design tokens**: `export const design: DesignSystem = { … }` at module top makes the slide tweakable from the Design panel.
- **Vertical budget math** (CRITICAL): every page must fit 1080px. Do the math BEFORE writing JSX:
  ```
  font_size × line_height × lines + gaps + 2 × padding ≤ 1080
  ```
  If close, **split into two pages**. Do not use `overflow: auto` to hide content.
- **Bullet rule**: bullets must NOT wrap to a second line. If they would, either shorten the copy or move to its own page.

---

## Step 8 — Reusable templates (copy these patterns)

The build-agents-that-ship deck has 4 reusable component templates. Copy them into your new deck:

### `UseCase` — consideration slide with pill, headline, bullets, metric card
Used for the Act III consideration slides (10–22). Two-column grid: text left, offset-shadow metric card right. Supports optional `bgImage` + `cinematicBg` for the cinematic look.

### `CaseStudy` — story-arc slide for failure/success/reference
Used for the three case studies. Top: status pill + period. Big company name. Tagline below ("Klarna is Sweden's biggest fintech…"). 4 fact-rows on left, image/video on right, pivotal moment box, lesson card, citation strip.

### `LessonsGrid` — 4-card "Why it failed/worked" pattern
Used right after each case study. Headline + 4 numbered cards in a 2×2 grid + colored takeaway strip ("Take this with you · …").

### `JourneyBar` — flight-path indicator at the top of every slide
The unifying element. Renders the dashed full route, the pink solid trail filled to current %, three terminal dots, and the airplane icon with phase-dependent angle.

### `AtmosphericBg` — backdrop with `cinematic` mode
```tsx
<AtmosphericBg src={img} cinematic textZone="left" />
```

The full source for these templates is in `slides/claude-cowork-enterprise/index.tsx` in the reference repo. Copy verbatim, then adapt.

---

## Step 9 — The 12-step build workflow

```
1.  Get the customer's agenda (literal bullets). Map slides 1:1.
2.  Bootstrap: npx @open-slide/cli init <slug> && cd <slug> && npm install && npm run dev
3.  Ask the 4 scoping questions (Step 1). Lock in answers.
4.  Draft the 4-act outline (Step 3). Confirm with user before writing JSX.
5.  Write all slide components in a single index.tsx under slides/<deck-id>/.
    Use the reusable templates (UseCase, CaseStudy, LessonsGrid).
6.  Add JourneyBar with PHASES matching your 4 acts.
7.  Invoke nano-banana-pro: generate ~10 cinematic atmospheric images
    (one per major slide). Save to slides/<deck-id>/assets/.
8.  Invoke hyperframes for 4–5 video moments (cover intro, hook reveal,
    case-study timelines, closing). Render to MP4, drop into assets/.
9.  Wire images and videos into slides. Use AtmosphericBg cinematic for
    images, full <video> for the dramatic moments.
10. Verify in browser: walk every slide. Check vertical budget. Check
    that no bullet wraps. Check that fonts loaded.
11. Iterate with the customer. EXPECT 5+ redirects. Don't fight them —
    each one improves the deck.
12. Push to a private GitHub repo BEFORE the talk so it survives a
    laptop failure. Include a README with clone-and-run instructions.
```

---

## Step 10 — Anti-patterns (things that look good but fail)

- ❌ **ROI math with division formulas** → use plain English ("Did it pay for itself? = What you got back ÷ What you spent.")
- ❌ **"Should you build it?" as 4 bullet points** → use a 2×2 quadrant matrix (high/low volume × repetitive/creative). Visual matrix is 10× clearer than prose.
- ❌ **Mgmt-pitch slides** in a hackathon deck → cut. Wrong audience.
- ❌ **Light-on-bone palette** when the metaphor is flight → switch to sky-blue + cinematic dark. Aesthetic must match metaphor.
- ❌ **Same template for every slide** → looks uniform but boring. Add cinematic backgrounds per slide for unity-with-variety.
- ❌ **Citing fabricated stats** to a developer audience → use rules of thumb instead, or cut the number entirely.
- ❌ **EBIT, PoC, RAG, BYOC** dumped without definition → audience tunes out within 30 seconds.
- ❌ **"Watson failed because of misalignment"** → too abstract. Be specific: "Trained on textbook cases. Real patients aren't in the textbook."
- ❌ **Layouts that wrap text on bullets** → shorten or split.
- ❌ **`overflow: auto`** to hide overflowing content → the canvas doesn't scroll. Cropped content is gone.

---

## Step 11 — The DECK-PLAYBOOK.md file

After scaffolding, drop a `DECK-PLAYBOOK.md` at the project root for the speaker to add their personal notes. Section 10 of the playbook is intentionally a `TODO` checklist for the speaker to fill in after the talk:

> - [ ] _What worked in the room?_
> - [ ] _What would I do differently next time?_
> - [ ] _What surprised me?_

Each deck becomes feedback for the next deck. After 10 sessions, the playbook will be more accurate than the speaker's conscious memory.

---

## Step 12 — Repository structure (the deliverable)

```
<deck-slug>/
├── package.json               # @open-slide/core ^1.1.0
├── package-lock.json          # locks exact versions (commit this)
├── README.md                  # clone-and-run instructions
├── DECK-PLAYBOOK.md           # this skill, distilled for the speaker
├── AGENTS.md / CLAUDE.md      # symlinked open-slide rules + playbook link
├── open-slide.config.ts
├── slides/
│   └── <deck-id>/
│       ├── index.tsx          # ALL slides in one file (typically 22–24)
│       └── assets/            # *.mp4 (videos) + *.png (nano-banana images)
└── .gitignore                 # node_modules, .env*, .DS_Store
```

Push to a **private** GitHub repo before the talk:
```bash
gh repo create <user>/<deck-slug> --private --source=. --remote=origin --push \
  --description "..."
```

---

## Reference implementation

The exact pattern this skill describes was implemented at:

**<https://github.com/hoodini/build-agents-that-ship>** (private — clone if you have access)

That repo includes:
- 24 production slides in one `index.tsx` (~3000 lines)
- 5 HyperFrames-rendered MP4 videos
- 14 nano-banana cinematic backgrounds
- Reusable templates (UseCase, CaseStudy, LessonsGrid, JourneyBar, AtmosphericBg)
- The DECK-PLAYBOOK.md this skill is derived from

When unsure how to implement a pattern described in this skill, **read the corresponding file in that repo**.

---

## Closing principle

**The deck is for the audience, not for the speaker.**

Every layer of polish — voice, story, visual, motion — exists to make the audience feel they're on a journey, that the lessons are theirs to take, and that the speaker respects their time and intelligence.

If a slide doesn't pass the "would this drop an aha-token in the audience's mind" test, cut or rewrite it. Hollywood, not corporate. Story, not summary. Flight, not boxes.

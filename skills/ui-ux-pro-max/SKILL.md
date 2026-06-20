---
name: ui-ux-pro-max
description: "AI-powered UI/UX design intelligence with 67 styles, 161 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 15 tech stacks. Use when building websites, landing pages, dashboards, admin panels, e-commerce, SaaS, portfolios, mobile apps, or any UI components. Triggers on: design, UI, UX, layout, color palette, typography, accessibility, glassmorphism, dark mode, responsive, button, modal, navbar, card, form, chart."
license: MIT
---

# UI/UX Pro Max — Design Intelligence

Comprehensive design guide for web and mobile applications. Contains 67 UI styles, 161 color palettes, 57 font pairings, 161 product types with reasoning rules, 99 UX guidelines, and 25 chart types across 15 technology stacks.

## When to Apply

**Must Use** for:
- Designing new pages (Landing Page, Dashboard, Admin, SaaS, Mobile App)
- Creating or refactoring UI components (buttons, modals, forms, tables, charts)
- Choosing color schemes, typography systems, spacing, or layout systems
- Reviewing UI code for UX, accessibility, or visual consistency
- Implementing navigation structures, animations, or responsive behavior

**Skip** for: pure backend logic, API/database design, infrastructure/DevOps, non-visual scripts.

## Rule Categories by Priority

| Priority | Category | Impact | Key Checks |
|----------|----------|--------|------------|
| 1 | Accessibility | CRITICAL | Contrast 4.5:1, Alt text, Keyboard nav, Aria-labels |
| 2 | Touch & Interaction | CRITICAL | Min 44×44px, 8px spacing, Loading feedback |
| 3 | Performance | HIGH | WebP/AVIF, Lazy loading, CLS < 0.1 |
| 4 | Style Selection | HIGH | Match product type, Consistency, SVG icons |
| 5 | Layout & Responsive | HIGH | Mobile-first, Viewport meta, No horizontal scroll |
| 6 | Typography & Color | MEDIUM | Base 16px, Line-height 1.5, Semantic color tokens |
| 7 | Animation | MEDIUM | 150–300ms, transform/opacity only, reduced-motion |
| 8 | Forms & Feedback | MEDIUM | Visible labels, Error near field, Submit feedback |
| 9 | Navigation Patterns | HIGH | Predictable back, Bottom nav ≤5, Deep linking |
| 10 | Charts & Data | LOW | Legends, Tooltips, Accessible colors |

## Quick Reference — Critical Rules

### 1. Accessibility (CRITICAL)
- **color-contrast**: Minimum 4.5:1 ratio for normal text (large text 3:1)
- **focus-states**: Visible focus rings on interactive elements (2–4px)
- **alt-text**: Descriptive alt text for meaningful images
- **aria-labels**: aria-label for icon-only buttons
- **keyboard-nav**: Tab order matches visual order; full keyboard support
- **reduced-motion**: Respect prefers-reduced-motion

### 2. Touch & Interaction (CRITICAL)
- **touch-target-size**: Min 44×44pt (Apple) / 48×48dp (Material)
- **touch-spacing**: Minimum 8px gap between touch targets
- **hover-vs-tap**: Use click/tap for primary; don't rely on hover alone
- **loading-buttons**: Disable during async; show spinner

### 3. Performance (HIGH)
- **image-optimization**: WebP/AVIF, responsive images (srcset/sizes), lazy load
- **font-loading**: Use font-display: swap; reserve space to reduce CLS
- **lazy-loading**: Lazy load non-hero components
- **virtualize-lists**: Virtualize lists with 50+ items

### 4. Style Selection (HIGH)
- **style-match**: Match style to product type
- **no-emoji-icons**: Use SVG icons (Heroicons, Lucide), not emojis
- **dark-mode-pairing**: Design light/dark variants together
- **primary-action**: Each screen has only one primary CTA

### 5. Layout & Responsive (HIGH)
- **viewport-meta**: width=device-width initial-scale=1 (never disable zoom)
- **mobile-first**: Design mobile-first, scale up to desktop
- **breakpoint-consistency**: Use 375 / 768 / 1024 / 1440
- **readable-font-size**: Minimum 16px body text on mobile

### 6. Typography & Color (MEDIUM)
- **line-height**: Use 1.5–1.75 for body text
- **font-scale**: Consistent type scale (12 14 16 18 24 32)
- **color-semantic**: Define semantic color tokens (primary, error, surface)
- **weight-hierarchy**: Bold headings (600–700), Regular body (400)

### 7. Animation (MEDIUM)
- **duration-timing**: 150–300ms for micro-interactions; ≤400ms complex
- **transform-performance**: Use transform/opacity only; avoid width/height
- **easing**: ease-out entering, ease-in exiting; no linear for UI transitions
- **interruptible**: Animations must be interruptible by user input

### 8. Forms & Feedback (MEDIUM)
- **input-labels**: Visible label per input (not placeholder-only)
- **error-placement**: Show error below the related field
- **inline-validation**: Validate on blur (not keystroke)
- **progressive-disclosure**: Reveal complex options progressively

### 9. Navigation Patterns (HIGH)
- **bottom-nav-limit**: Bottom navigation max 5 items with labels + icons
- **back-behavior**: Back navigation must be predictable; preserve scroll/state
- **deep-linking**: All key screens reachable via deep link / URL
- **modal-escape**: Modals offer clear close/dismiss affordance

### 10. Charts & Data (LOW)
- **chart-type**: Match chart to data (trend→line, comparison→bar, proportion→pie)
- **legend-visible**: Always show legend near the chart
- **tooltip-on-interact**: Hover/tap tooltips showing exact values
- **color-guidance**: Accessible palettes; avoid red/green-only pairs

## Available UI Styles (67)

**General (49):** Glassmorphism, Claymorphism, Minimalism, Brutalism, Neumorphism, Bento Grid, Dark Mode, Light Mode, Flat Design, Material Design, Skeuomorphism, Retro/Vintage, Cyberpunk, Vaporwave, Memphis, Swiss/International, Art Deco, Bauhaus, Japandi, Wabi-Sabi, and more.

**Landing Page (8):** Hero-Centric, Social-Proof-First, Problem-Solution, Feature Showcase, Video-First, Minimal CTA, Story-Driven, Product-Led.

**Dashboard/Analytics (10):** Data-Dense, Executive Summary, Real-Time Monitoring, KPI-Focused, Dark Analytics, Clean Metrics, Financial, Healthcare, Operations, Marketing.

## Supported Tech Stacks (15)
React, Next.js, Vue, Nuxt.js, Nuxt UI, Svelte, Astro, Angular, Laravel (Blade/Livewire/Inertia), SwiftUI, Jetpack Compose, React Native, Flutter, HTML + Tailwind, shadcn/ui.

## Workflow

### Step 1: Analyze Requirements
- Product type: SaaS, e-commerce, portfolio, healthcare, fintech, entertainment, etc.
- Target audience and context (mobile/desktop, age group)
- Style keywords: minimal, dark, vibrant, professional, playful
- Tech stack

### Step 2: Select Design System
Match product type to recommended patterns:

| Product | Recommended Style | Color Mood | Anti-Pattern |
|---------|------------------|------------|--------------|
| SaaS/B2B | Minimalism, Bento Grid | Professional blue/purple | Too decorative |
| Fintech/Banking | Clean Minimal, Dark | Trust navy/green | AI gradients |
| Healthcare | Clean Light, Accessible | Calming blue/teal | Aggressive red |
| E-commerce | Feature Showcase, Card-Heavy | Vibrant accent | Cluttered |
| Portfolio | Bold, Typography-First | Personal brand color | Generic |
| Gaming | Cyberpunk, Dark Mode | Neon, high contrast | Washed out |
| Beauty/Spa | Elegant, Glassmorphism | Warm rose/gold | Corporate blue |
| AI/Chatbot | Dark Mode, Minimal | Purple/cyan gradient | Overcrowded |

### Step 3: Apply Color System
- Define primary, secondary, accent, error, warning, success, surface tokens
- Ensure 4.5:1 contrast for all text/background pairs
- Design both light and dark variants simultaneously
- Test with WCAG contrast checkers

### Step 4: Typography
- Heading + Body font pairing (personality match)
- Type scale: 12/14/16/18/24/32/48px
- Line-height 1.5 body, 1.2 headings
- Font-weight: 700 headings, 400 body, 500–600 labels

### Step 5: Components
Apply rules from sections 1–9 above. Use this checklist:

**Visual Quality:**
- [ ] SVG icons (no emojis)
- [ ] Consistent icon family
- [ ] Semantic color tokens (no raw hex in components)
- [ ] Press states don't shift layout

**Interaction:**
- [ ] Touch targets ≥44×44pt
- [ ] Micro-interactions 150–300ms
- [ ] Disabled states visually clear
- [ ] Focus order matches visual order

**Responsive:**
- [ ] Mobile-first tested at 375px
- [ ] No horizontal scroll
- [ ] Safe areas respected (mobile)
- [ ] Readable text measure on tablets

**Accessibility:**
- [ ] All images have alt text
- [ ] Form fields labeled
- [ ] Color not only indicator
- [ ] reduced-motion supported

## Common Anti-Patterns to Avoid
- Using emojis as navigation icons
- Placeholder-only form labels (no visible label)
- Horizontal scroll on mobile
- hover-only interactions (mobile has no hover)
- Mixing flat + skeuomorphic styles randomly
- AI purple/pink gradients for banking/healthcare
- Icon-only navigation without text labels
- Animations that block user input
- Gray-on-gray text (contrast failure)
- CLS-causing layouts (no reserved image space)

## Pre-Delivery Checklist
Run through Critical (1–2) and High (3–5, 9) rules before shipping any UI:

1. Contrast ratio ≥4.5:1 for all text
2. All touch targets ≥44px
3. Images use WebP, have width/height attributes
4. Mobile tested at 375px wide
5. No horizontal scroll on any breakpoint
6. Focus states visible on all interactive elements
7. Form labels visible (not placeholder-only)
8. Loading/error states handled
9. Back navigation works predictably
10. Dark mode tested if supported

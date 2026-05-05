# RuBase Workshop — CHANGELOG

## 2026-05-05 — HCSS dashboard restyle, slide-deck unification, gate sweep

Massive restyle pass to align the workshop site with the rubase-sunburst-template / rubase.org design system. Three repos in lockstep:
- this repo (`sdspieg/rubase-workshop`, generic / latest)
- `sdspieg/rubase-workshop-irsem-2703` (IRSEM Paris snapshot)
- `sdspieg/rubase-workshop-fletcher-2603` (Fletcher School snapshot)

### Restyle (110 HTML files across the 3 repos)
- Palette swap: cyberpunk `#0a0e27/#00ffff/#9400d3/...` → HCSS dashboard `--bg #0d1f3c / --db #1a3761 / --gold #dbad50 / --lb #82a0bc / --wh #e8edf3`. Legacy CSS variables aliased to dashboard tokens so existing class names keep mapping.
- Font swap: dropped `'Titillium Web'` Google Fonts import + `font-family` references; switched to `system-ui, -apple-system, "Segoe UI", Helvetica, sans-serif`.
- Removed neon glow text-shadows + cyan/purple/green gradients; replaced with solid `var(--db)` cards with 4px gold `border-left` (matches dashboard card pattern).

### Header redesign — 2-row banner
- Row 1: HCSS knight + GT logo (left) · centered title · CCNY + RuBase logos (right). Dropped Koninklijke Landmacht.
- Row 2: Home / Resources / RuBase Deliverables Overview / version selector — centered, with a thin top divider.
- Logo height 36px → 40px. Title font 1.05rem → 1.15rem.
- Hide legacy top chrome (`.partner-logos`, `.top-buttons`, `.home-btn`, etc.) on slide-deck pages.

### Slide-deck chrome (every page with `.slide` markup)
- **`.hcss-fs-chip`** — fullscreen toggle pill, fixed bottom-right, gold-bordered. Hides any pre-existing `.fullscreen-btn`.
- **`.hcss-home-chip`** — bottom-left mirror of fs-chip on welcome decks (back to workshop home).
- **`.hcss-progress-monitor`** — slim gold pill bottom-center: prev arrow / dots / next arrow. Auto-binds to `.slide` count + `.active` class. Hides any pre-existing `.nav-controls` / `.slide-indicator` to avoid double pills.
- **slide-fit JS** — measures each slide's natural width/height, applies `transform: scale(s)` with `transform-origin: center center` to fit viewport. Re-fits on resize/orientation/active-class change.
- **slim chrome overrides** — `!important` rules tightening pre-existing nav-controls, indicator-dot, slide-counter, prev/next/first-btn so every deck's chrome is uniform and slim.
- **Inactive-slide hide** — `.slide:not(.active) { display: none !important }` to override per-deck overrides like `.title-slide { display: flex }`.

### Sweep tooling (`/tmp/`)
- `restyle_workshop_pages.py` — palette + Titillium → system-ui sweep (idempotent via sentinel)
- `add_fullscreen_chip.py` — inject `.hcss-fs-chip` + JS
- `add_slide_fit.py` — inject viewport-fit JS
- `slim_deck_chrome.py` — inject `!important` overrides
- `add_progress_monitor.py` — inject `.hcss-progress-monitor` pill
- `fix_missing_js.py` — re-inject JS sentinels in files where `</head>` got stripped
- `deck_gate_check.py` — static gate over 11 must-fix items per deck
- `sweep_v2.py` — Playwright batch: navigate each deck, screenshot every slide, DOM-probe per slide for fs-chip, overlap, content-overflow, viewport-fit, broken images, console errors, real scrollbars, Titillium computed font
- `pm.py` — colorful one-page CLI dashboard showing repo state + gate coverage + live sweep progress (Rich `Live`, refresh 2s)

### Companion fixes
- `presentation-styles.css` (top-level shared) had Titillium `@import` and `--font-primary` → patched
- `wacko-slides.css` (Fletcher only) had Titillium → patched
- 73 files were missing `</head>` after an earlier sweep with a buggy regex → restored
- Stripped stray `U+0001` control characters that an earlier sweep injected (caused 27px container offset on every deck → CENTERX failures)
- Fixed `MutationObserver` calls against null `document.body` — they fired before DOM was ready on every deck
- `wacko-nlm-presentation.html` preload loop tried to load `slide-16.png` which doesn't exist (loop count was 16 but the 16 files include `slide-3b.png`, so the loop was off-by-one)

### Per-deck audit
After 8 sweep rounds + the disastrous experimental `position:fixed` rollback, currently **965/1068 (90.4%)** of slide-probes pass all 10 gate items. Remaining 103 failures concentrate in ~10 specific decks where per-deck CSS/JS quirks defeat the generic sweeps:
- ottoman_bank case_study + ottoman-bank-working-backup — slide BBox naturally extends past viewport center horizontally (CENTERX 56–69 px off, just outside the ±50 px tolerance)
- openalex / exercise / welcome-day3 / landing / wacko-presentation-backup — `CONTENT_OVERFLOW` flagged at mobile viewport (slide-fit re-fit doesn't always apply on viewport change)

### Boundary
- Visual sweep ran 8 rounds. Each round catches more issues than the last because the probe gets stricter (added viewport-fit check after the user pointed out internal-overflow gate didn't catch slides taller than the window).
- The remaining 103 issues need per-deck manual audit; a further sweep round 9 is in flight at the time of this commit.

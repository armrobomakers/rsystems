# UI References

This stage used public 21st.dev community references as visual guidance for the first-screen modernization.

## 1. Navbar Components

- URL: https://21st.dev/community/components/s/navbar
- Takeaway: compact nav patterns, floating bar treatment, clear CTA placement, mobile-first menu grouping.

## 2. Hero Components

- URL: https://21st.dev/community/components/s/hero
- Takeaway: large hero headline, split layout, strong contrast between copy and supporting visual block.

## 3. Glassmorphism Trust Hero

- URL: https://21st.dev/%40easemize
- Components inspected: Flow Field Background, Modern Mobile Menu, Dynamic Hero, Animated Glassy Pricing.
- Takeaway: premium trust and motion can live in a layered glass surface without overwhelming the first screen.

## 4. Modern Mobile Menu

- URL: https://21st.dev/%40easemize
- Takeaway: mobile menu should feel like a deliberate layer, not a generic dropdown. Smooth open/close and clear touch targets.

## 5. Flow Field Background

- URL: https://21st.dev/community/components/easemize/flow-field-background/default
- Takeaway: background can carry atmosphere without becoming noisy. Useful as a reference for deep ambient layers and motion.

## 6. 3D / Generative Background collections

- URL: https://21st.dev/community/components/s/3d-background
- URL: https://21st.dev/community/components/s/shader-bg-for-hero
- Takeaway: hero background can be atmospheric and premium even without literal imagery.

## Practical application in this stage

- Use the navbar logic from the mobile menu references, but keep the current HTML/CSS/JS stack.
- Use the hero hierarchy and trust-panel logic from the hero references.
- Use the background references only as atmospheric guidance, not as framework-specific implementation.

## Stage 2 — Services and Benefits

References used for the central sections:

### 1. Bento Grid

- URL: https://21st.dev/community/components/s/bento-grid
- What worked: modular card rhythm, clear separation of value blocks, compact hierarchy.
- What was not copied: framework code, component API, and any interactive behavior.
- Adaptation for vanilla HTML/CSS: use a static 2-column feature layout with stronger spacing and card depth.

### 2. Feature Grid

- URL: https://21st.dev/community/components/s/feature-grid
- What worked: scannable feature grouping, repeated card language, high signal-to-noise ratio.
- What was not copied: React structure and any registry-specific patterns.
- Adaptation for vanilla HTML/CSS: use plain grid, consistent card paddings, and equalized information density.

### 3. Feature Card

- URL: https://21st.dev/community/components/s/feature-card
- What worked: one card, one message, one visual anchor.
- What was not copied: code, props, or framework dependencies.
- Adaptation for vanilla HTML/CSS: keep service cards self-contained, with one icon, one headline, one short body, one action.

### 4. Cards

- URL: https://21st.dev/community/components/s/cards
- What worked: layered surfaces, borders, spacing, and restrained shadows.
- What was not copied: card implementation details or interactions.
- Adaptation for vanilla HTML/CSS: preserve the current card system, but increase depth contrast and hierarchy.

### 5. Section Heading

- URL: https://21st.dev/community/components/s/section-heading
- What worked: balanced heading/subheading rhythm and clean section introductions.
- What was not copied: any component code or layout framework.
- Adaptation for vanilla HTML/CSS: refine only the section heading spacing and balance inside services/packages blocks.

## Stage 3 — Social Proof, CTA and Footer

References used for the lower page:

- `$21st-cli-use` was invoked during the stage, but `21st search` was unavailable because the session was not signed in.
- No 21st components were installed.
- Visual guidance came from public 21st.dev pages plus the `$ui-ux-pro-max` index.
- React, Next.js, Tailwind CSS, shadcn/ui, and Motion were not transferred into this project.

### 1. Stats

- URL: https://21st.dev/community/components/s/stats
- What worked: compact metric rhythm, scannable numbers, trust-forward hierarchy.
- What was not copied: any counter animation, framework component code, or JavaScript behavior.
- Adaptation for vanilla HTML/CSS: keep the trust-strip static, more compact, and readable on mobile.
- Applied to: `trust-strip`.

### 2. Testimonial Section

- URL: https://21st.dev/community/components/s/testimonial-section
- What worked: testimonial block ordering, social-proof density, and clear separation from the CTA.
- What was not copied: carousel logic, framework-specific wrappers, or dynamic state.
- Adaptation for vanilla HTML/CSS: use the existing review grid, strengthen the card surface, and keep the section static.
- Applied to: `reviews`.

### 3. Testimonial Card

- URL: https://21st.dev/community/components/s/testimonial
- What worked: quote marker, avatar + name + role grouping, and strong trust cue hierarchy.
- What was not copied: component code, data models, or generated motion.
- Adaptation for vanilla HTML/CSS: refine each review card with cleaner spacing, subtler borders, and readable attribution.
- Applied to: individual `review-card` elements.

### 4. CTA

- URL: https://21st.dev/community/components/s/cta
- What worked: single primary action, clear end-of-page closure, and concise supporting copy.
- What was not copied: form mechanics, component props, or any JS-driven conversion flow.
- Adaptation for vanilla HTML/CSS: keep one primary Telegram action, improve spacing, and visually connect CTA to the footer.
- Applied to: `#contact`.

### 5. Footer

- URL: https://21st.dev/community/components/s/footer
- What worked: compact information density, simple link cluster, and strong page closure.
- What was not copied: any framework layout or generated data.
- Adaptation for vanilla HTML/CSS: keep the existing links, tighten the rhythm, and add a restrained top divider.
- Applied to: `.footer`.

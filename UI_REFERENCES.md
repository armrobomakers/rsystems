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

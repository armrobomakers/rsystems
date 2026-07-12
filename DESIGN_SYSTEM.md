# R Systems Design System

## Stage 1 goal

Сделать первый экран более премиальным, спокойным и конверсионным, не меняя смысл, тексты, URL и структуру страницы целиком.

## Visual direction

- Основа: тёмный editorial / founder-led лендинг.
- Настроение: дорогой, спокойный, уверенный, без визуального шума.
- Акценты: тёплый бронзовый, мягкий свет, стеклянные поверхности, глубокие тени.
- Главный принцип: один сильный фокус на экране, остальное поддерживает его.

## Typography

- `Cormorant Garamond` используется как выразительный serif для hero, карточек и акцентных чисел.
- `Manrope` используется как основной UI-шрифт для навигации, тела текста, кнопок и служебной информации.
- `Unbounded` используется точечно для микро-подписей, маркеров и строгих интерфейсных элементов.
- Заголовки должны быть крупными, плотными и с мягким отрицательным трекингом.

## Color system

### Core

- Background: `#07090d`
- Elevated background: `#0d1117`
- Surface: `rgba(13, 16, 22, 0.86)`
- Surface strong: `rgba(17, 21, 30, 0.94)`
- Text: `#f4efe7`
- Muted text: `rgba(244, 239, 231, 0.64)`

### Accent

- Primary accent: `#d6a86e`
- Highlight accent: `#f0c48b`
- Soft accent fill: `rgba(214, 168, 110, 0.12)`
- Stroke accent: `rgba(214, 168, 110, 0.18 - 0.28)`

### Background layers

- Use layered radial gradients for depth.
- Keep grain subtle, never noisy.
- Use warm highlights only where they help guide attention.

## Layout rules

- Desktop-first composition.
- Max content width stays centered and compact.
- Hero should carry the visual weight.
- Secondary sections should stay quieter than the hero.
- Use generous spacing between major blocks.
- Avoid full-width bright panels or hard contrasts in the first stage.

## Header rules

- Header is a floating premium bar, not a full-screen block.
- It must feel detached from the page surface.
- On scroll, the header should leave the screen smoothly instead of sitting as a background strip.
- The mobile menu must be clearly layered above content and must not feel glued to the page body.

## Hero rules

- Keep current copy and CTA wording unchanged.
- Make the left copy block stronger with calmer spacing and tighter hierarchy.
- Keep the right panel as the visual anchor.
- The hero background should feel intentional through gradients, glow, and soft depth.
- The second CTA stays visually lighter than the primary CTA.

## Buttons

- Primary button:
  - warm gradient fill
  - strong contrast
  - subtle elevation
- Secondary button:
  - transparent / glass style
  - clear outline
  - lighter than the primary action
- Hover:
  - small lift
  - slightly stronger border or glow
  - no harsh animation

## Cards

- Cards use rounded corners and soft borders.
- Glass effect is allowed but must stay restrained.
- Shadows are deep but not muddy.
- Right hero panel may use layered abstract visuals instead of literal illustration.

## Motion

- Keep motion short and premium.
- Header hide/show should feel smooth and deliberate.
- Menu open/close should avoid snapping.
- No heavy motion system in stage 1.

## Responsive rules

- Desktop keeps the original composition.
- Tablet collapses hero into a single column when needed.
- Mobile should preserve:
  - readable title
  - visible CTA
  - manageable header
  - no horizontal overflow
- Header and hero spacing must feel intentional on small screens.

## Stage 1 boundaries

Allowed:

- global variables and body background
- header, logo, nav, mobile menu
- hero copy block
- CTA buttons
- hero panel styling
- hero background layers
- minimal menu interaction in `app.js`

Not allowed in this stage:

- redesign of lower sections
- framework migration
- new dependencies
- CMS / backend changes
- copy rewrite

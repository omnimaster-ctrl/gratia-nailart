# Design System: Gratia Nail Art — Hada del Bosque

## 1. Visual Theme & Atmosphere

Gratia Nail Art's website is an enchanted forest fairy garden brought to digital life — whimsical, ethereal, and artistic. The design operates on a foundation of Light Cream (`#e5e4d0`) with Mustard Gold (`#cda255`) as the primary accent, creating a warm dusk-in-the-forest atmosphere where every element feels like it belongs in a fairy tale.

The brand is built around "Hada del Bosque" (Forest Fairy) — a chibi fairy boy mascot with pointed ears and wings who guides users through the experience. Collection names like "Manantial Encantado", "Ópalo Místico", and "Espejo de Hada" reinforce the mystical identity. The visual language evokes a fairy garden at golden hour: warm ambient lighting, soft organic shadows, and golden sparkle accents.

Typography pairs Noto Serif for headlines (evoking fairy-tale chapter headings) with Manrope for body text (clean, modern readability). This contrast creates a "storybook meets modern studio" feel — artisanal yet professional.

What distinguishes this design is the complete absence of hard edges. No 1px borders, no sharp box-shadows. Instead, surfaces float with soft ambient shadows that mimic candlelight. The Dark Olive (`#515942`) anchors dark sections like an enchanted forest canopy, while Sage Green (`#b7bba2`) and Warm Beige (`#d6c9b0`) create layered depth like forest floor foliage.

**Key Characteristics:**
- Enchanted forest fairy garden at golden hour — warm, whimsical, ethereal
- Light Cream canvas (`#e5e4d0`) with Mustard Gold (`#cda255`) as singular brand accent
- Dark Olive (`#515942`) for hero sections and headers — the forest canopy
- Noto Serif headlines + Manrope body — storybook meets modern studio
- Soft ambient shadows only — no hard 1px borders anywhere
- Chibi fairy mascot as recurring visual element
- Photography-forward portfolio — nail art is the hero content
- Golden sparkle/particle accents for magical moments
- Spanish language throughout (Mexican Spanish)
- Mobile-first, 390px primary breakpoint

## 2. Color Palette & Roles

### Primary Brand
- **Dark Olive** (`#515942`): Primary — backgrounds, headers, hero sections, nav, forest canopy feel
- **Primary Container** (`#3d4435`): Darker variant — hover states on dark surfaces, deep forest

### Accent & CTAs
- **Mustard Gold** (`#cda255`): Secondary — ALL CTAs, buttons, highlights, active states, links, the "golden light" of the fairy garden
- **Warm Brown** (`#a18b63`): Tertiary — secondary accents, supporting elements, wood/bark tones

### Surfaces
- **Warm Beige** (`#d6c9b0`): Surface high — cards, containers, elevated content, parchment feel
- **Sage Green** (`#b7bba2`): Surface dim — section backgrounds, alternating sections, mossy undertone
- **Light Cream** (`#e5e4d0`): Background — page foundation, the meadow clearing

### Text Scale
- **Dark Forest** (`#2a2e25`): On-background — primary text on light surfaces, warm near-black
- **Olive Text** (`#5c6152`): On-surface-variant — secondary text, descriptions, captions
- **Muted Olive** (`#8a8d7e`): Outline — borders, dividers, placeholder text

### Functional
- **On Primary** (`#e5e4d0`): Text on dark olive backgrounds — light cream for readability
- **On Secondary** (`#ffffff`): Text on gold buttons — white for maximum contrast
- **Error Red** (`#ba1a1a`): Error states, validation failures
- **Error Container** (`#ffdad6`): Error background, error message containers

### State Variants
- **Inverse Surface** (`#2a2e25`): Tooltips, snackbars, overlays
- **Inverse Primary** (`#b7bba2`): Accent on dark overlays
- **Surface Bright** (`#f2efe6`): Highest elevation surface, modal backgrounds
- **Surface Lowest** (`#f2efe6`): Lowest elevation, page chrome

## 3. Typography Rules

### Font Families
- **Headlines:** `Noto Serif` — serif, elegant fairy-tale chapter heading energy. Weights: 400 (regular), 700 (bold). Use italic sparingly for testimonial quotes.
- **Body/Labels:** `Manrope` — sans-serif, clean modern readability. Weights: 300 (light), 400 (regular), 600 (semibold), 800 (extra-bold for impact).

### Type Scale

| Element | Font | Size | Weight | Letter-spacing | Color |
|---------|------|------|--------|---------------|-------|
| Hero title | Noto Serif | 48px / 3rem | 700 | -0.5px | `#e5e4d0` on dark, `#2a2e25` on light |
| Page title | Noto Serif | 36px / 2.25rem | 700 | -0.3px | `#2a2e25` |
| Section heading | Noto Serif | 28px / 1.75rem | 700 | -0.2px | `#2a2e25` |
| Card title | Manrope | 18px / 1.125rem | 600 | 0 | `#2a2e25` |
| Body text | Manrope | 16px / 1rem | 400 | 0 | `#2a2e25` |
| Small body | Manrope | 14px / 0.875rem | 400 | 0 | `#5c6152` |
| Label | Manrope | 12px / 0.75rem | 600 | 0.5px | `#5c6152` |
| Caption | Manrope | 11px / 0.6875rem | 400 | 0.3px | `#8a8d7e` |
| CTA button | Manrope | 16px / 1rem | 600 | 0.5px | `#ffffff` |
| Nav links | Manrope | 14px / 0.875rem | 400 | 0 | `#e5e4d0` |

### Typography Rules
- Headlines in Noto Serif create the "fairy-tale chapter" feeling — always use for section openers
- Body text always in Manrope — never mix serif into body paragraphs
- Slight negative letter-spacing on large headlines for intimacy
- Positive letter-spacing on labels and buttons for legibility at small size
- Line height: 1.2 for headlines, 1.5 for body text, 1.4 for cards
- Max line width: 65ch for body paragraphs

## 4. Component Stylings

### Buttons

| Variant | Background | Text | Border | Radius | Padding | Shadow |
|---------|-----------|------|--------|--------|---------|--------|
| Primary CTA | `#cda255` | `#ffffff` | none | 8px | 12px 32px | `0 2px 8px rgba(205,162,85,0.3)` |
| Primary CTA (hover) | `#b8903d` | `#ffffff` | none | 8px | 12px 32px | `0 4px 12px rgba(205,162,85,0.4)` |
| Secondary | `transparent` | `#515942` | 1.5px solid `#515942` | 8px | 12px 32px | none |
| Secondary (hover) | `#515942` | `#e5e4d0` | 1.5px solid `#515942` | 8px | 12px 32px | none |
| Ghost/Text | `transparent` | `#cda255` | none | 4px | 8px 16px | none |
| Disabled | `#b7bba2` | `#8a8d7e` | none | 8px | 12px 32px | none |

### Cards

| Variant | Background | Radius | Shadow | Border |
|---------|-----------|--------|--------|--------|
| Default | `#d6c9b0` | 12px | `0 2px 8px rgba(42,46,37,0.08)` | none |
| Elevated | `#e5e4d0` | 12px | `0 4px 16px rgba(42,46,37,0.12)` | none |
| Dark surface | `#3d4435` | 12px | `0 4px 16px rgba(0,0,0,0.2)` | none |
| Selected | `#d6c9b0` | 12px | `0 2px 8px rgba(42,46,37,0.08)` | 3px left `#cda255` |
| Interactive (hover) | `#d6c9b0` | 12px | `0 6px 20px rgba(42,46,37,0.15)` | none |

### Navigation
- **Glass nav bar:** `backdrop-filter: blur(12px)`, background `rgba(81,89,66,0.85)`, sticky top
- **Logo:** "Gratia Nail Art" in Noto Serif italic, `#cda255` gold
- **Nav links:** Manrope 14px regular, `#e5e4d0`, hover underline in gold
- **CTA pill:** `#cda255` background, `#515942` text, 20px radius, Manrope 14px semibold
- **Mobile nav:** Full-screen overlay, dark olive background, centered links, fairy mascot at bottom

### Form Inputs
- **Default:** Light cream `#e5e4d0` background, no border, subtle bottom line in `#b7bba2`
- **Focus:** Bottom line transitions to gold `#cda255`, subtle gold glow `0 0 0 2px rgba(205,162,85,0.2)`
- **Label:** Floating label in Manrope 12px, `#5c6152`, moves up and shrinks on focus
- **Error:** Bottom line turns `#ba1a1a`, error message in 12px below
- **Radius:** 8px top-left and top-right, 0 bottom (to expose bottom line)
- **Padding:** 16px horizontal, 12px vertical

### Pills / Tabs
- **Inactive:** `#d6c9b0` background, `#5c6152` text, 20px radius
- **Active:** `#cda255` background, `#2a2e25` text, 20px radius
- **Horizontal scroll** with hidden scrollbar, 8px gap between pills

### Progress Stepper (Booking Flow)
- **Completed step:** Gold `#cda255` filled circle with white checkmark, gold connecting line
- **Active step:** Gold `#cda255` circle outline with step number, bold label
- **Upcoming step:** `#8a8d7e` outline circle, grey connecting line, muted label
- **Circle size:** 32px diameter
- **Connecting line:** 2px thick, spans between circles

### Gallery / Portfolio Grid
- **Layout:** CSS Grid, 2 columns on mobile, 3-4 on desktop
- **Image cards:** Square aspect ratio (1:1), 12px radius, overflow hidden
- **Label overlay:** Bottom-left, `rgba(81,89,66,0.75)` backdrop, Manrope 11px semibold, `#e5e4d0` text, 4px radius
- **Hover:** Slight scale `transform: scale(1.03)`, deeper shadow, 300ms ease

## 5. Layout Principles

### Spacing System
- Base unit: 8px
- Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px
- Section vertical padding: 64px (mobile), 96px (desktop)
- Card internal padding: 16px (mobile), 24px (desktop)
- Grid gap: 12px (mobile gallery), 16px (card grids), 24px (section elements)

### Grid
- **Mobile (390px):** Single column, 16px horizontal page margins
- **Tablet (768px):** 2-column content grid, 32px margins
- **Desktop (1280px):** Max-width 1200px container, centered, 3-4 column grids
- **Gallery:** 2 columns mobile, 3 columns tablet, 4 columns desktop

### Whitespace Philosophy
- Generous breathing room between sections — the fairy garden has clearings
- Cards never touch — minimum 12px gap
- Text blocks have 24px minimum margin from container edges
- Hero sections use 40% of viewport height minimum
- Between-section spacing creates a scroll rhythm: content → breathing room → content

### Content Width
- **Body text:** max-width 65ch for readability
- **Cards container:** max-width 1200px
- **Hero text:** max-width 600px (mobile), 800px (desktop)
- **Full-bleed sections:** Dark olive and gold CTA banners extend edge-to-edge

## 6. Depth & Elevation

### Shadow System
Shadows are warm-tinted (using `rgba(42,46,37,...)` — the dark olive base) rather than pure black. This keeps shadows feeling like natural forest shade.

| Level | Shadow | Use |
|-------|--------|-----|
| Level 0 | none | Flat elements, backgrounds |
| Level 1 | `0 1px 4px rgba(42,46,37,0.06)` | Subtle lift — pills, tags |
| Level 2 | `0 2px 8px rgba(42,46,37,0.08)` | Cards, containers |
| Level 3 | `0 4px 16px rgba(42,46,37,0.12)` | Elevated cards, modals |
| Level 4 | `0 8px 32px rgba(42,46,37,0.16)` | Floating elements, dropdowns |
| Gold glow | `0 2px 8px rgba(205,162,85,0.3)` | CTA buttons — golden fairy light |

### Surface Hierarchy
1. **Page background** (`#e5e4d0`) — the meadow clearing
2. **Section alternate** (`#b7bba2`) — mossy ground, every other section
3. **Cards** (`#d6c9b0`) — floating parchment, Level 2 shadow
4. **Dark sections** (`#515942`) — forest canopy, used for hero and CTA banners
5. **Deepest dark** (`#3d4435`) — deep forest, nav glass effect base
6. **Modals/overlays** (`#f2efe6`) — bright fairy glade, Level 3+ shadow

### Transitions
- **Default:** `all 200ms ease-out` — smooth, not snappy
- **Hover lift:** `transform 300ms ease, box-shadow 300ms ease`
- **Focus glow:** `box-shadow 150ms ease-in`
- **Page transitions:** `opacity 400ms ease` — gentle fade like morning mist

## 7. Do's and Don'ts

### Do
- Use soft ambient shadows from the warm shadow system — never `rgba(0,0,0,...)` pure black shadows
- Apply Mustard Gold (`#cda255`) only for CTAs, active states, and key accent moments — it's the golden fairy light
- Use Dark Olive (`#515942`) for dark sections — it's the enchanted forest, not generic dark mode
- Keep all corners rounded (8px minimum) — no sharp rectangles in a fairy garden
- Use Noto Serif exclusively for headlines and section titles — the fairy-tale voice
- Use Manrope for all body text, labels, and UI elements — the modern voice
- Let photography be the hero content — nail art images need breathing room
- Include the fairy mascot character on key pages — he's the brand guide
- Add subtle golden sparkle/particle effects for success states and hero sections
- Use Spanish throughout — "Agenda tu cita", not "Book now"
- Maintain warm color temperature — everything should feel like golden hour

### Don't
- **NEVER** show prices or costs on the public landing page or services page
- Never use pure black (`#000000`) for text — use Dark Forest (`#2a2e25`)
- Never use hard 1px solid borders — use shadows or color change for separation
- Never use cold blues or grays — this is a warm enchanted forest, not a tech dashboard
- Never use more than one accent color per section — gold is the only "pop"
- Never make the fairy mascot too small — he should be prominent when present
- Never use generic stock photos — only real nail art work by Gratia
- Never center-align body paragraphs — left-align for readability, center only for headlines
- Never use aggressive animations — movements should be gentle and organic (200-400ms)
- Never break the warm tonal range — if it doesn't feel like sunset in a forest, it doesn't belong

## 8. Responsive Behavior

### Breakpoints

| Name | Width | Layout changes |
|------|-------|---------------|
| Mobile | 390px | Single column, stacked layout, hamburger nav, 16px margins |
| Tablet | 768px | 2-column grids, expanded nav, 32px margins |
| Desktop | 1024px | 3-column grids, full nav bar, max-width containers |
| Wide | 1280px | 4-column gallery, 1200px max container, generous whitespace |

### Mobile-First Priorities
- Touch targets: minimum 44px height for all interactive elements
- CTA buttons: full-width on mobile, auto-width on desktop
- Navigation: hamburger menu → full horizontal nav at 768px+
- Gallery: 2 columns at 390px, never single column (nail art needs side-by-side)
- Booking flow bottom bar: fixed to viewport bottom on mobile, inline on desktop
- Hero section: fairy mascot below headline on mobile, beside it on desktop
- Cards: stack vertically on mobile, grid on tablet+

### Collapsing Strategy
- Nav links collapse to hamburger at <768px
- "Más de Gratia" cards: horizontal scroll on mobile, grid on tablet+
- Service category tabs: horizontal scroll with peek on all breakpoints
- Footer: stacked single column on mobile, multi-column on desktop
- Calendar (booking): full-width on mobile, centered card on desktop

## 9. Agent Prompt Guide

### Quick Color Reference
- Page background: Light Cream (`#e5e4d0`)
- Primary/dark sections: Dark Olive (`#515942`)
- CTA/accent/gold: Mustard Gold (`#cda255`)
- Cards/surfaces: Warm Beige (`#d6c9b0`)
- Alternate sections: Sage Green (`#b7bba2`)
- Text primary: Dark Forest (`#2a2e25`)
- Text secondary: Olive (`#5c6152`)
- Text on dark: Light Cream (`#e5e4d0`)
- Borders/muted: Muted Olive (`#8a8d7e`)
- Error: `#ba1a1a`

### Ready-to-Use Component Prompts

- "Create a nav bar: glass effect with `backdrop-filter: blur(12px)`, `rgba(81,89,66,0.85)` background, sticky top. Logo 'Gratia Nail Art' in Noto Serif italic gold `#cda255` left. Nav links in Manrope 14px `#e5e4d0` center. Gold pill CTA 'Agenda tu cita' right. 20px radius pill, `#cda255` bg, `#515942` text."

- "Create a hero section: Dark Olive `#515942` background full-width. Large 'Gratia Nail Art' in Noto Serif 48px bold `#e5e4d0`. Subtitle 'Uñas & Nail Art — Técnicas mixtas' in Manrope 18px `#b7bba2`. Gold CTA button 'Agenda tu cita' — `#cda255` bg, white text, 8px radius, golden glow shadow. Fairy mascot character positioned right side. Decorative nail art gem images scattered left."

- "Create a portfolio gallery: Section title 'Mi Trabajo' in Noto Serif 28px. CSS grid 2 columns on mobile. Square image cards with 12px radius, overflow hidden. Bottom-left label overlay with `rgba(81,89,66,0.75)` backdrop, small white text ('Nail Art', 'Técnica Mixta'). Hover: slight scale(1.03), deeper shadow, 300ms ease."

- "Create a gold CTA banner: Full-width `#cda255` background. Text '¿Te gustó un diseño? Agenda tu cita' in Manrope 18px semibold `#515942`. Centered. Padding 24px vertical. No shadow needed — the gold IS the emphasis."

- "Create a service card: Warm Beige `#d6c9b0` background, 12px radius, Level 2 shadow. Square thumbnail top with rounded top corners. Service name in Manrope 18px semibold. Description in 14px `#5c6152`, 2 lines max. Clock icon + duration '~2 hrs' in small text. Gold 'Agendar' button at bottom. NO PRICES."

- "Create a booking stepper: 4 steps horizontal. Completed = gold `#cda255` filled circle + white checkmark. Active = gold outline circle + number. Upcoming = grey `#8a8d7e` outline. 32px circles. 2px connecting lines. Labels below: 'Servicio', 'Fecha y Hora', 'Tus Datos', 'Confirmar'."

- "Create a form input: `#e5e4d0` background, 8px top radius, 0 bottom radius. Subtle bottom line in `#b7bba2`. On focus: bottom line gold `#cda255`, soft gold glow `0 0 0 2px rgba(205,162,85,0.2)`. Floating label in Manrope 12px. 16px horizontal padding."

- "Create a footer: Dark Olive `#515942` background. Instagram and Facebook icons in `#e5e4d0`. '@gratia.nailart' text. 'SOFTWARE BY OMNIFRACTAL' in Manrope 10px caps `#8a8d7e`. '© 2026 Gratia Nail Art' below. Centered layout. 32px padding."

### Design Philosophy Summary
> Gratia Nail Art is an enchanted forest fairy garden at golden hour. Every surface is a mossy stone or parchment scroll (warm beige, sage green). The gold accent is fairy light breaking through the canopy. Dark olive is the deep forest. There are no sharp edges, no cold colors, no harsh shadows. The fairy mascot guides visitors through a magical world of nail art. Photography is the hero — let the art speak. Spanish language, Mexican heart, fairy soul.

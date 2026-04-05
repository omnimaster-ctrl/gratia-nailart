## Project: Gratia Nail Art — Booking + Landing Page

**Client:** Hazael Gonzalez (@gratia.nailart) — Nail artist in Morelia, Michoacán
**Referred by:** Paloma (David's wife) — founding client rate
**Company:** Omnifractal (David's company building this as a SaaS product)

### The Vision

A custom landing page + booking system for Gratia Nail Art. This is Omnifractal's first external client — Hazael becomes the proof of concept to sell this service to other nail artists.

### Brand Identity: "Hada del Bosque" (Forest Fairy)

Hazael's brand is built around an enchanted woodland fairy aesthetic — whimsical, ethereal, artistic. Key brand elements:
- **Chibi fairy boy mascot** with pointed ears and wings
- **"Jardín de las Hadas"** — his academy concept
- **Mystical nail art collection names:** Manantial Encantado, Ópalo Místico, Espejo de Hada, Lágrima de Sirena, Corazón de Aragón, Telaraña de Fuego
- **Sub-brands:** Gratia Nail Shop (products), Gratia Academy (education), Booking (reservas)
- **Instagram:** @gratia.nailart (1004 posts, 4350 followers)

### Color Palette (from Hazael's brand guide)

| Swatch | Hex | Role |
|--------|-----|------|
| Dark Olive | `#515942` | Primary — backgrounds, headers |
| Warm Brown | `#a18b63` | Tertiary — secondary accents |
| Mustard Gold | `#cda255` | Secondary — CTAs, highlights, buttons |
| Warm Beige | `#d6c9b0` | Surface — cards, containers |
| Sage Green | `#b7bba2` | Surface variant — section backgrounds |
| Light Cream | `#e5e4d0` | Background — foundation color |

### Typography
- **Headlines:** Noto Serif — elegant, fairy-tale chapter headings
- **Body/Labels:** Manrope — clean, modern readability

### Design Rules
- NO pricing or cost information on the public landing page
- Dark backgrounds with warm golden lighting (fairy garden at dusk)
- Soft ambient shadows — no hard borders or 1px lines
- Gold (#cda255) for all CTAs and accent highlights
- The fairy mascot character must be prominent
- Spanish language throughout
- Mobile-first design

### Pricing (agreed with client)

| Item | Amount | Notes |
|------|--------|-------|
| Setup fee | $2,700 MXN | One-time: design, dev, infra setup |
| Monthly | $600 MXN | Hosting, servers, maintenance |
| Raw infra cost | ~$300 MXN/mo | Railway (frontend + backend + MongoDB) + domain |

Future full-price tiers for other clients: $9,000 setup + $900/mo (keeping 9s frequency)

### Infrastructure (Basic Tier)

| Service | ~Cost/mo USD |
|---------|-------------|
| Railway frontend | $5 |
| Railway backend (FastAPI) | $5-10 |
| Railway MongoDB | $5 |
| Resend (email) | $0 (free tier) |
| Domain | $1 (amortized) |
| **Total** | **~$15-20 USD (~$300 MXN)** |

No AI bot / no Gemini for basic tier.

### Stitch Design Project

- **Project ID:** `1318442603202433328`
- **URL:** https://stitch.withgoogle.com/projects/1318442603202433328
- **Design System:** "Gratia Nail Art - Hada del Bosque" (updated with client palette)

Key screens:
| Screen | ID | Status |
|--------|-----|--------|
| Original landing (dark green/gold) | `89b7b364d9234327b0e35aa47f6cfc65` | Client approved layout |
| Palette-updated landing | `113e84b01cad4ef9959209adfe073f6f` | Updated with sage/olive palette |
| Variant B | `b0989dbaf97a4d1ba2d22e0be6e1c14c` | Alternative variant |
| Full mobile landing (Gratia Inicio) | `51b8dcf90378455f8d848cc7c535a546` | Has HTML code |
| Booking step 1 (Reserva Paso 1) | `2c8ed193ed2248bfbce8e1fcb6d2efd0` | Has HTML code |

### Landing Page Structure (approved by client)

1. **Nav** — "Gratia Nail Art" logo, Home, Servicios, Enseñamos, Contacto, "Agenda tu cita" CTA
2. **Hero** — Large "Gratia Nail Art" headline, subtitle "Uñas & Nail Art — Técnicas mixtas", CTA button, fairy mascot right side, decorative nail art gems left side, dark enchanted background
3. **"Mi Trabajo" Gallery** — Portfolio grid with nail art, labels (Nail Art, Técnica Mixta), NO PRICES
4. **Gold CTA Banner** — "¿Te gustó un diseño? Agenda tu cita"
5. **"Más de Gratia"** — Three cards: Gratia Nail Shop, Jardín de las Hadas (academy), Reserva tu cita
6. **Footer** — IG + FB icons, @gratia.nailart, SOFTWARE BY OMNIFRACTAL, © 2026 Gratia Nail Art

### Design System

The project uses the **DESIGN.md** format (from [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)). The `DESIGN.md` file at project root is the single source of truth for all visual decisions. **Always read `DESIGN.md` before generating any UI code or design prompts.** It contains exact hex values, shadow systems, component specs, typography rules, and agent-ready prompts.

### Tech Stack (planned — same as La Pop Nails)

- **Frontend:** React (landing page + booking wizard)
- **Backend:** FastAPI
- **Database:** MongoDB via Motor
- **Payments:** MercadoPago (deposit per booking)
- **Hosting:** Railway
- **Notifications:** WhatsApp (future), Email (Resend)

### Domain

Pending — waiting for Hazael to choose (suggested: gratianailart.com, gratianails.mx, or similar)

---

## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

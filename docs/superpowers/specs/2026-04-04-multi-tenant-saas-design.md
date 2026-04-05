# Multi-Tenant Nail Art SaaS Platform — Design Spec

**Date:** 2026-04-04
**Author:** David Tello / Omnifractal
**Status:** Draft — pending approval
**Codebase:** `/Users/davidtello/landingpopnails` (to be renamed `omnifractal-nails`)

---

## 1. Problem Statement

Omnifractal has a working nail art booking system for La Pop Nails. A second client (Gratia Nail Art) needs the same system with different branding. Today everything is hardcoded — colors, copy, fonts, Instagram handles, email templates, database names, CORS origins. Adding a client means forking the repo and maintaining two codebases forever.

**Goal:** Convert the existing single-tenant system into a multi-tenant SaaS platform where adding a new client means creating a config file + deploying a new Railway stack.

---

## 2. Architecture Decisions

### 2.1 Deployment Model: Separate deploys, shared codebase

Each client gets their own Railway project with independent frontend, backend, and MongoDB instances. All deploys come from the same git repo.

**Why not single deployment with domain routing?**
- Billing isolation: each client's infra cost is directly traceable
- Failure isolation: one client's crash doesn't affect others
- Independent scaling: heavy-traffic clients don't compete for resources
- Simpler SSL/domain config per Railway project

**Trade-off:** Double infra cost (~$30-40 USD/mo for two clients vs ~$15-20 for one). Acceptable given the $600 MXN/mo per client pricing.

### 2.2 Branding: Static config files (hybrid with database)

| Data | Where it lives | Why |
|------|----------------|-----|
| Colors, fonts, logo, copy, font URLs | `tenants/{slug}.json` in repo | Bundled at build time, zero runtime overhead, version-controlled |
| Feature flags (defaults) | `tenants/{slug}.json` | Deployed with the code, predictable |
| Services, pricing, deposit amount | MongoDB `tenant_settings` + `services` collections | Admin-editable without redeploy |
| Schedule, blocked dates, hours | MongoDB `scheduling` + `blocked_dates` | Changes frequently, admin manages |
| Appointments, clients, discounts | MongoDB | Dynamic business data |

**Key rule:** The tenant JSON is the source of truth for *how things look*. MongoDB is the source of truth for *how things work*. Route handlers never read the JSON file for business logic — only for branding (email templates, notification copy).

### 2.3 Frontend Theming: CSS Custom Properties + TenantContext

At build time, the tenant JSON is copied into the bundle. At runtime:
1. `applyTheme()` sets 13+ CSS custom properties on `:root`
2. `<TenantProvider>` wraps the app, exposing config via `useTenant()` hook
3. Components use `var(--color-primary)` in styles and `useTenant()` for copy/features
4. Tailwind arbitrary values `bg-[var(--color-secondary)]` for utility classes

### 2.4 Feature Flags: Config-driven, component-level

Features are toggled per tenant in the JSON config. Components check flags and render or skip:

```jsx
const { features } = useTenant();
if (!features.ai_chat) return null;
```

All features are built and shipped in every deploy. Disabled features are simply not rendered. No code splitting by tenant — keeps the build simple.

---

## 3. Tenant Config Schema

```json
{
  "slug": "gratia",
  "business_name": "Gratia Nail Art",
  "legal_name": "Gratia Nail Art",
  "tagline": "Uñas & Nail Art — Técnicas mixtas",
  "logo_url": "/assets/tenants/gratia/logo.png",
  "mascot_url": "/assets/tenants/gratia/hada.png",
  "favicon_url": "/assets/tenants/gratia/favicon.ico",

  "google_fonts_url": "https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400&family=Manrope:wght@300;400;600;800&display=swap",
  "fonts": {
    "headline": "Noto Serif",
    "body": "Manrope"
  },

  "colors": {
    "primary": "#515942",
    "primary_container": "#3d4435",
    "secondary": "#cda255",
    "tertiary": "#a18b63",
    "surface_high": "#d6c9b0",
    "surface_dim": "#b7bba2",
    "background": "#e5e4d0",
    "surface_bright": "#f2efe6",
    "on_background": "#2a2e25",
    "on_surface_variant": "#5c6152",
    "outline": "#8a8d7e",
    "on_primary": "#e5e4d0",
    "on_secondary": "#ffffff",
    "error": "#ba1a1a",
    "error_container": "#ffdad6"
  },

  "contact": {
    "instagram_handle": "gratia.nailart",
    "instagram_url": "https://instagram.com/gratia.nailart",
    "facebook_handle": "",
    "facebook_url": "",
    "whatsapp_number": "",
    "email_from": "citas@gratianailart.com",
    "email_reply_to": "hazael@gratianailart.com"
  },

  "copy": {
    "hero_headline": "Gratia Nail Art",
    "hero_subtitle": "Uñas & Nail Art — Técnicas mixtas",
    "cta_primary": "Agenda tu cita",
    "cta_gallery": "¿Te gustó un diseño? Agenda tu cita",
    "chat_welcome": "¡Hola! Soy tu asistente de Gratia Nail Art. ¿En qué puedo ayudarte?",
    "booking_policy": "Para confirmar tu cita, se requiere un apartado que se descuenta del costo total del servicio.",
    "footer_attribution": "SOFTWARE BY OMNIFRACTAL",
    "copyright": "© 2026 Gratia Nail Art"
  },

  "features": {
    "ai_chat": false,
    "whatsapp_notifications": false,
    "discounts": true,
    "reschedule": true,
    "google_calendar": true,
    "email_notifications": true,
    "show_prices_on_landing": false,
    "shop_page": false,
    "academy_page": false,
    "instagram_landing": false
  },

  "landing": {
    "sections": ["hero", "gallery", "ctaBanner", "masDeGratia", "footer"],
    "hero_style": "enchanted",
    "gallery_columns_mobile": 2,
    "gallery_columns_desktop": 4
  },

  "meta": {
    "title": "Gratia Nail Art | Hada del Bosque",
    "description": "Nail art de autor en Morelia, Michoacán. Técnicas mixtas y diseños únicos. Agenda tu cita.",
    "og_image": "/assets/tenants/gratia/og-image.jpg"
  }
}
```

### La Pop Nails Config (matching current behavior exactly)

```json
{
  "slug": "lapopnails",
  "business_name": "La Pop Nails",
  "legal_name": "La Pop Nails",
  "tagline": "Servicios profesionales de manicura",
  "logo_url": "/assets/tenants/lapopnails/logo.png",
  "mascot_url": null,
  "favicon_url": "/assets/tenants/lapopnails/favicon.ico",

  "google_fonts_url": "",
  "fonts": {
    "headline": "Playlist Script",
    "body": "Funnel Sans"
  },
  "local_fonts": [
    { "family": "Playlist Script", "src": "/fonts/PlaylistScript.otf", "weight": "400" },
    { "family": "Funnel Sans", "src": "/fonts/FunnelSans-VariableFont_wght.ttf", "weight": "300 800" },
    { "family": "Chewy", "src": "/fonts/Chewy-Regular.ttf", "weight": "400" }
  ],

  "colors": {
    "primary": "#3A2E3F",
    "primary_container": "#2A1E2F",
    "secondary": "#B884C9",
    "tertiary": "#D9B55A",
    "surface_high": "#F8D9E2",
    "surface_dim": "#EDE7F3",
    "background": "#F6EFE8",
    "surface_bright": "#ffffff",
    "on_background": "#3A2E3F",
    "on_surface_variant": "#6A5C72",
    "outline": "#9A8DA2",
    "on_primary": "#ffffff",
    "on_secondary": "#ffffff",
    "error": "#ba1a1a",
    "error_container": "#ffdad6"
  },

  "contact": {
    "instagram_handle": "lapopnails",
    "instagram_url": "https://instagram.com/___lapopnails",
    "facebook_handle": "",
    "facebook_url": "",
    "whatsapp_number": "+524431234567",
    "email_from": "citas@lapopnails.mx",
    "email_reply_to": "lapopnails@gmail.com"
  },

  "copy": {
    "hero_headline": "La Pop Nails",
    "hero_subtitle": "Te espero para crear magia en tus uñas ✨",
    "cta_primary": "Agendar Ahora",
    "cta_gallery": "",
    "chat_welcome": "¡Hola! Soy tu asistente de La Pop Nails. ¿En qué puedo ayudarte?",
    "booking_policy": "Para confirmar tu cita, se requiere un anticipo de $250 MXN.",
    "footer_attribution": "SOFTWARE BY OMNIFRACTAL",
    "copyright": "© 2026 La Pop Nails"
  },

  "features": {
    "ai_chat": true,
    "whatsapp_notifications": true,
    "discounts": true,
    "reschedule": true,
    "google_calendar": true,
    "email_notifications": true,
    "show_prices_on_landing": true,
    "shop_page": false,
    "academy_page": false,
    "instagram_landing": true
  },

  "landing": {
    "sections": ["hero", "services", "process", "hygiene", "contact", "footer"],
    "hero_style": "default",
    "gallery_columns_mobile": 2,
    "gallery_columns_desktop": 3
  },

  "meta": {
    "title": "La Pop Nails | Reserva tu cita",
    "description": "Servicios profesionales de manicura en Morelia. Agendar ahora.",
    "og_image": "/assets/tenants/lapopnails/og-image.jpg"
  }
}
```

---

## 4. New Files to Create

### Frontend

| File | Purpose |
|------|---------|
| `tenants/lapopnails.json` | La Pop Nails static branding config |
| `tenants/gratia.json` | Gratia Nail Art static branding config |
| `frontend/src/tenant/TenantContext.js` | React context + `TenantProvider` component |
| `frontend/src/tenant/useTenant.js` | `useTenant()` hook — returns full config |
| `frontend/src/tenant/applyTheme.js` | Sets CSS custom properties on `:root` from tenant colors, injects font `<link>` |
| `frontend/src/tenant/tenantConfig.js` | Build-time resolved config (copied from `tenants/{slug}.json` by build script) |
| `frontend/src/tenant/FeatureGate.js` | `<FeatureGate feature="ai_chat">` wrapper component |
| `frontend/public/assets/tenants/gratia/` | Gratia logos, mascot, favicon, OG image |
| `frontend/public/assets/tenants/lapopnails/` | La Pop Nails assets (moved from current locations) |

### Backend

| File | Purpose |
|------|---------|
| `backend/tenant_config.py` | Loads `tenants/{slug}.json` at startup, exposes `get_tenant_static_config()` |

### Build

| File | Purpose |
|------|---------|
| `scripts/build-tenant.sh` | Build script: copies tenant JSON, injects font URL into index.html, runs `craco build` |

---

## 5. Files to Modify

### Frontend — Phase 1 (CSS Custom Properties)

| File | Change |
|------|--------|
| `App.css` | Replace `#D9B55A`, `#F6EFE8`, `#F8D9E2` → `var(--color-tertiary)`, `var(--color-background)`, `var(--color-surface-high)` |
| `LandingPage.css` | Move `@font-face` declarations to conditional loading via `local_fonts` config. Replace hardcoded colors → CSS vars |
| `WizardBooking.css` | Replace `#ec4899, #f43f5e` gradient → `var(--color-secondary)` gradient |
| `index.js` | Add `applyTheme()` call + wrap app in `<TenantProvider>` |
| `public/index.html` | Add `<!-- FONT_LINK_PLACEHOLDER -->` comment for build script injection |

### Frontend — Phase 2 (Extract Copy + Features)

| File | Change |
|------|--------|
| `App.js` | Replace hardcoded Instagram handle, logo URL, API_BASE_URL → `useTenant()` |
| `LandingPage.js` | Replace hardcoded services array, hero copy, section structure → `useTenant()` + API fetch |
| `AIChatWidget.js` | Replace "La Pop Nails" → `useTenant().business_name`. Wrap in `<FeatureGate feature="ai_chat">` |
| `WizardBooking.js` | Replace policy text → `useTenant().copy.booking_policy` |
| `InstagramLanding.js` | Wrap in `<FeatureGate feature="instagram_landing">` |
| `BookingPage.js` | Replace logo URL → `useTenant().logo_url` |
| `PaymentSuccess.js` | Replace business name → `useTenant().business_name` |

### Backend

| File | Change |
|------|--------|
| `database.py` | `client[os.environ.get('MONGO_DB_NAME', 'lapopnails_db')]` |
| `tenant.py` | `DEFAULT_TENANT_ID = os.environ.get('DEFAULT_TENANT_ID', '<current-uuid>')` and same for slug |
| `server.py` | `ALLOWED_ORIGINS = json.loads(os.environ.get('ALLOWED_ORIGINS', '["http://localhost:3000"]'))` |
| `email_service.py` | Accept `tenant_config` param. Replace 5 hardcoded color tokens with `tenant_config['colors']` values |
| `whatsapp_service.py` | Replace business name in message templates with `tenant_config['business_name']` |
| `scheduling.py` | Move `WEEKDAY_MORNING_TIMES`, `SATURDAY_MORNING_TIMES` to read from tenant DB doc instead of module constants |
| `config/featureFlags.js` | Rewrite to read from tenant config object instead of raw env vars |

---

## 6. Data Flow

### Build Time
```
REACT_APP_TENANT_SLUG=gratia npm run build
  → scripts/build-tenant.sh:
    1. cp tenants/gratia.json frontend/src/tenant/tenantConfig.json
    2. Read google_fonts_url from JSON
    3. sed -i "s|FONT_LINK_PLACEHOLDER|<link href='...' rel='stylesheet'>|" public/index.html
    4. Read local_fonts array → generate @font-face CSS if present
    5. craco build
```

### Frontend Runtime
```
index.js
  → import tenantConfig from './tenant/tenantConfig.json'
  → applyTheme(tenantConfig.colors)
      → document.documentElement.style.setProperty('--color-primary', '#515942')
      → ... (13 properties)
      → document.documentElement.setAttribute('data-tenant', 'gratia')
  → <TenantProvider config={tenantConfig}>
      → <App />
          → useTenant() → { colors, fonts, features, copy, contact, ... }
          → <FeatureGate feature="ai_chat"> → renders or skips
          → LandingPage reads landing.sections → renders in order
```

### Backend Runtime
```
Railway env vars:
  TENANT_SLUG=gratia
  MONGO_DB_NAME=gratia_db
  DEFAULT_TENANT_ID=<uuid>
  ALLOWED_ORIGINS=["https://gratianailart.com","http://localhost:3000"]
  MP_ACCESS_TOKEN=<gratia-specific>
  RESEND_API_KEY=<shared-or-separate>
  ...

server.py startup:
  → load_tenant_config('gratia') → reads tenants/gratia.json
  → connect to gratia_db
  → ensure_default_tenant() → upserts tenant doc with defaults
  → all routes scope queries by DEFAULT_TENANT_ID

email_service.py:
  → send_confirmation(appointment, tenant_config=get_tenant_static_config())
  → HTML template uses tenant_config['colors']['secondary'] for CTA button
  → From: tenant_config['contact']['email_from']
```

---

## 7. Environment Variables Per Deployment

### Railway: Gratia Frontend
```
REACT_APP_TENANT_SLUG=gratia
REACT_APP_BACKEND_URL=https://gratia-backend-production.up.railway.app
REACT_APP_MP_PUBLIC_KEY=<gratia-mercadopago-public-key>
```

### Railway: Gratia Backend
```
TENANT_SLUG=gratia
MONGO_DB_NAME=gratia_db
DEFAULT_TENANT_ID=<new-uuid>
DATABASE_URL=mongodb+srv://<gratia-cluster>
FRONTEND_URL=https://gratianailart.com
ALLOWED_ORIGINS=["https://gratianailart.com","http://localhost:3000"]
MP_PUBLIC_KEY=<gratia-key>
MP_ACCESS_TOKEN=<gratia-token>
MP_WEBHOOK_SECRET=<gratia-secret>
RESEND_API_KEY=<shared-key>
JWT_SECRET=<unique-secret>
ADMIN_USERNAME=hazael
ADMIN_PASSWORD_HASH=<bcrypt-hash>
GOOGLE_CALENDAR_ID=<gratia-calendar>
GOOGLE_SERVICE_ACCOUNT=<service-account-json>
# AI (disabled in config but credentials ready for future activation)
GROQ_API_KEY=<key>
# WhatsApp (disabled but ready)
TWILIO_ACCOUNT_SID=<sid>
TWILIO_AUTH_TOKEN=<token>
```

---

## 8. Migration Phases

Each phase ends with a verification step. La Pop Nails must work identically after each phase.

### Phase 1: Foundation (CSS Custom Properties + TenantContext)

**Goal:** Replace all hardcoded colors with CSS vars. No visual change.

1. Create `tenants/lapopnails.json` with exact current color values
2. Create `frontend/src/tenant/TenantContext.js`, `useTenant.js`, `applyTheme.js`
3. Create `frontend/src/tenant/tenantConfig.json` (copy of lapopnails.json for now)
4. Update `index.js` — import config, call `applyTheme()`, wrap in `<TenantProvider>`
5. Replace all hardcoded hex colors in CSS files with `var(--color-*)` references
6. Replace Tailwind color utilities in JSX (`from-pink-500`) with `bg-[var(--color-secondary)]` arbitrary values
7. Handle local fonts: move `@font-face` from `LandingPage.css` to dynamically generated CSS based on `local_fonts` config

**Verification:** Deploy to Railway staging. Visual pixel-diff La Pop Nails before/after. Run full booking flow.

### Phase 2: Backend Configuration

**Goal:** Remove all hardcoded backend config. No behavior change.

1. Update `database.py` — use `MONGO_DB_NAME` env var
2. Update `tenant.py` — use `TENANT_SLUG` and `DEFAULT_TENANT_ID` env vars
3. Update `server.py` — use `ALLOWED_ORIGINS` env var
4. Create `backend/tenant_config.py` — loads tenant JSON, exposes getter
5. Update `email_service.py` — parameterize 5 color tokens from tenant config
6. Update `whatsapp_service.py` — parameterize business name
7. Add env vars to La Pop Nails Railway: `MONGO_DB_NAME=lapopnails_db`, `TENANT_SLUG=lapopnails`, `ALLOWED_ORIGINS=["https://lapopnails.mx"]`

**Verification:** Deploy to production. Confirm booking flow + email delivery + WhatsApp unchanged.

### Phase 3: Feature Flags

**Goal:** All optional features wrapped in flags. La Pop Nails flags all set to `true` (current behavior).

1. Rewrite `featureFlags.js` to read from tenant config
2. Create `<FeatureGate>` component
3. Wrap `AIChatWidget` in `<FeatureGate feature="ai_chat">`
4. Wrap `InstagramLanding` route in `<FeatureGate feature="instagram_landing">`
5. Add `show_prices_on_landing` check in `LandingPage.js` service cards
6. Add `shop_page`, `academy_page` route guards
7. Add `whatsapp_notifications`, `discounts`, `reschedule` backend checks

**Verification:** Toggle each La Pop Nails flag to `false` one at a time, confirm feature disappears. Reset all to `true`.

### Phase 4: Extract Hardcoded Copy

**Goal:** All business-specific strings come from tenant config. No hardcoded "La Pop Nails" anywhere.

1. `LandingPage.js` — hero copy, services (fetch from API), process steps from config
2. `App.js` — Instagram handle, header content, logo URL
3. `AIChatWidget.js` — welcome message, business name
4. `WizardBooking.js` — policy text, form labels if customized
5. `BookingPage.js` — logo, title
6. `PaymentSuccess.js` — business name, confirmation copy
7. `RescheduleBooking.js` — business name references
8. `public/index.html` — `<title>` and meta tags via build script from `meta` config

**Verification:** `grep -r "La Pop Nails" frontend/src/` returns zero results (only in `tenants/lapopnails.json`). Full booking flow works.

### Phase 5: Create Gratia Tenant + Deploy

**Goal:** Gratia Nail Art running on its own Railway stack.

1. Create `tenants/gratia.json` with full Hada del Bosque config
2. Create `frontend/public/assets/tenants/gratia/` with logo, mascot, favicon, OG image
3. Create `scripts/build-tenant.sh` build script
4. Set up Railway: gratia-frontend, gratia-backend, gratia-mongodb
5. Configure all env vars (MercadoPago sandbox first)
6. Seed Gratia MongoDB: services catalog, scheduling config, deposit amount, admin user
7. Deploy and test full flow with MercadoPago sandbox

**Verification:** End-to-end booking on Gratia: select service → pick date/time → fill info → sandbox payment → email confirmation received.

### Phase 6: Gratia Landing Page Customization

**Goal:** Gratia-specific landing page matching the Stitch prototypes.

1. Create a section renderer that reads `landing.sections` array from config
2. Implement Gratia-specific sections: `hero` (enchanted style with mascot), `gallery` (portfolio grid, no prices), `ctaBanner` (gold full-width), `masDeGratia` (three cards)
3. La Pop Nails keeps its existing sections via its own `landing.sections` config
4. Connect domain, SSL, go live

**Verification:** Both sites render their correct landing pages. Both booking flows work. Cross-test: change a Gratia color in JSON, rebuild, confirm it takes effect.

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Tailwind JIT classes can't use CSS vars directly | Broken styles | Use `bg-[var(--color-secondary)]` arbitrary value syntax (Tailwind 3.4+) |
| Font loading flash (FOUT) on first visit | Ugly text flash | Inject `<link>` into HTML at build time, not runtime. Add `font-display: swap` |
| Local fonts (La Pop) vs Google Fonts (Gratia) | Build complexity | `local_fonts` array in config; build script generates `@font-face` CSS conditionally |
| Email HTML has 200+ lines with hardcoded colors | Broken email branding | Parameterize only the 5 color tokens at function level, don't rewrite template |
| Scheduling slot times are module constants | Gratia gets wrong hours | Move to tenant DB doc (already has `schedule.time_blocks` field in tenant.py) |
| `grep "La Pop"` misses some hardcoded string | Wrong branding shown | Phase 4 verification: automated grep check in CI |
| MercadoPago webhook URL shared confusion | Wrong payments attributed | Each deploy has its own webhook URL pointing to its own backend |
| Admin credentials in env vars | Security | Each deployment has unique JWT_SECRET and admin credentials |
| CSS var fallback in older browsers | Broken for some users | Target audience is young Mexican women on modern phones; CSS vars have 97%+ support |

---

## 10. Future Client Onboarding Checklist

When Omnifractal signs a new client, the process is:

1. Create `tenants/{slug}.json` — fill in branding, colors, fonts, copy, features
2. Add tenant assets to `frontend/public/assets/tenants/{slug}/`
3. Create Railway project (frontend + backend + MongoDB)
4. Set all env vars (MercadoPago, Resend, Google Calendar, etc.)
5. Run `scripts/build-tenant.sh` to build and deploy
6. Seed MongoDB with services, scheduling, admin user
7. Connect domain + SSL
8. Client UAT → go live

**Estimated time:** 1-2 days for standard branding, 3-5 days if custom landing page sections needed.

---

## 11. Out of Scope (for this iteration)

- **Multi-tenant admin panel** (managing all clients from one dashboard) — future
- **Self-service onboarding** (client signs up and configures their own site) — future
- **Shared MongoDB** (all tenants in one DB with tenant_id scoping) — decided against for billing isolation
- **A/B testing** of landing page variants — future
- **i18n / multi-language** — all clients are Mexican Spanish for now
- **Custom domain email** (hazael@gratianailart.com) — use Resend domain verification per client

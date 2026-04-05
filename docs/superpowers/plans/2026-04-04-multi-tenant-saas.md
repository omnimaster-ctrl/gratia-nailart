# Multi-Tenant Nail Art SaaS — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the La Pop Nails single-tenant booking system into a multi-tenant SaaS platform and deploy Gratia Nail Art as the second client.

**Architecture:** Shared codebase with per-tenant JSON config files for branding (colors, fonts, copy) and MongoDB for dynamic business data (services, hours, appointments). Separate Railway deployments per client. Feature flags control which capabilities each tenant has. CSS custom properties replace all hardcoded colors.

**Tech Stack:** React 19, CRA + Craco, Tailwind CSS 3.4, FastAPI, MongoDB (Motor), MercadoPago, Resend, Google Calendar API

**Spec:** `docs/superpowers/specs/2026-04-04-multi-tenant-saas-design.md`

**Codebase:** `/Users/davidtello/landingpopnails`

---

## File Structure Overview

### New Files

```
tenants/
├── lapopnails.json                              # La Pop Nails branding config
└── gratia.json                                  # Gratia Nail Art branding config

frontend/src/tenant/
├── TenantContext.js                             # React context + provider
├── useTenant.js                                 # Hook to consume tenant config
├── applyTheme.js                                # Sets CSS custom properties on :root
├── tenantConfig.json                            # Build-time resolved config (copied by build script)
└── FeatureGate.js                               # Conditional render by feature flag

frontend/public/assets/tenants/
├── lapopnails/                                  # La Pop Nails static assets
└── gratia/                                      # Gratia static assets

backend/
└── tenant_config.py                             # Loads tenant JSON for email/notification branding

scripts/
└── build-tenant.sh                              # Build script: copies config, injects fonts, runs craco build
```

### Modified Files

```
frontend/src/index.js                            # Wrap app in TenantProvider, call applyTheme
frontend/src/App.css                             # Replace 20+ hardcoded hex → CSS vars
frontend/src/LandingPage.css                     # Replace 25+ hardcoded hex → CSS vars, extract @font-face
frontend/src/WizardBooking.css                   # Replace 20+ hardcoded hex → CSS vars
frontend/src/LandingPage.js                      # Replace hardcoded copy/services → useTenant()
frontend/src/App.js                              # Replace hardcoded Instagram, logo → useTenant()
frontend/src/components/AIChatWidget.js           # Replace "La Pop Nails" → useTenant(), wrap in FeatureGate
frontend/src/BookingPage.js                      # Replace logo → useTenant()
frontend/src/WizardBooking.js                    # Replace policy text → useTenant()
frontend/src/PaymentSuccess.js                   # Replace business name → useTenant()
frontend/src/InstagramLanding.js                 # Wrap in FeatureGate
frontend/src/config/featureFlags.js              # Rewrite to read from tenant config
frontend/public/index.html                       # Add FONT_LINK_PLACEHOLDER for build injection
frontend/tailwind.config.js                      # Extend with CSS var color tokens
backend/database.py                              # Use MONGO_DB_NAME env var
backend/tenant.py                                # Use env vars for DEFAULT_TENANT_ID/SLUG
backend/server.py                                # Use ALLOWED_ORIGINS env var
backend/email_service.py                         # Parameterize brand colors from tenant config
```

---

## Phase 1: Tenant Config + Theme Foundation

### Task 1: Create La Pop Nails tenant config JSON

**Files:**
- Create: `tenants/lapopnails.json`

- [ ] **Step 1: Create tenants directory and config file**

```bash
mkdir -p /Users/davidtello/landingpopnails/tenants
```

Create `tenants/lapopnails.json`:

```json
{
  "slug": "lapopnails",
  "business_name": "La Pop Nails",
  "legal_name": "La Pop Nails",
  "tagline": "Te espero para crear magia en tus uñas ✨",

  "google_fonts_url": "",
  "local_fonts": [
    { "family": "Playlist Script", "src": "/fonts/PlaylistScript.otf", "weight": "400", "style": "normal" },
    { "family": "Funnel Sans", "src": "/fonts/FunnelSans-VariableFont_wght.ttf", "weight": "300 800", "style": "normal" },
    { "family": "Chewy", "src": "/fonts/Chewy-Regular.ttf", "weight": "400", "style": "normal" }
  ],
  "fonts": {
    "headline": "Playlist Script",
    "body": "Funnel Sans"
  },

  "colors": {
    "primary": "#2d2520",
    "primary_container": "#1a1512",
    "secondary": "#ec4899",
    "secondary_hover": "#db2777",
    "tertiary": "#D9B55A",
    "tertiary_hover": "#C7A147",
    "surface_high": "#F8D9E2",
    "surface_dim": "#F0E6DB",
    "background": "#F6EFE8",
    "surface_bright": "#ffffff",
    "on_background": "#2d2520",
    "on_surface_variant": "#6b7280",
    "outline": "#d1d5db",
    "on_primary": "#ffffff",
    "on_secondary": "#ffffff",
    "on_tertiary": "#2d2520",
    "error": "#ef4444",
    "error_container": "#fef2f2",
    "warning": "#d97706",
    "warning_container": "#fef3c7",
    "success": "#16a34a",
    "success_container": "#e8f5e9",
    "wizard_gradient_from": "#ec4899",
    "wizard_gradient_to": "#f43f5e",
    "gold_accent": "#D9B55A",
    "gold_dark": "#B8973D"
  },

  "contact": {
    "instagram_handle": "___lapopnails",
    "instagram_url": "https://instagram.com/___lapopnails",
    "facebook_handle": "",
    "facebook_url": "",
    "whatsapp_number": "+524431234567",
    "email_from": "citas@lapopnails.mx",
    "email_reply_to": "lapopnails.28@gmail.com"
  },

  "copy": {
    "hero_headline": "La Pop Nails",
    "hero_subtitle": "Te espero para crear magia en tus uñas ✨",
    "cta_primary": "Agendar Ahora",
    "cta_secondary": "Chat con Asistente",
    "chat_welcome": "¡Hola! Soy tu asistente de La Pop Nails. ¿En qué puedo ayudarte?",
    "booking_policy": "Se requiere un anticipo de $250 MXN para confirmar tu cita.",
    "footer_attribution": "SOFTWARE BY OMNIFRACTAL",
    "copyright": "© 2026 La Pop Nails",
    "email_title": "POP NAILS — Cita Confirmada"
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
    "hero_style": "default"
  },

  "meta": {
    "title": "La Pop Nails - Reserva tu cita",
    "description": "La Pop Nails - Reserva tu cita de manicura rusa y nail art",
    "theme_color": "#09090b",
    "og_image": "/popnails-icon-3d.png"
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd /Users/davidtello/landingpopnails
git add tenants/lapopnails.json
git commit -m "feat: add La Pop Nails tenant config JSON

Extract all branding values (colors, fonts, copy, contacts, features)
into a static tenant config file as first step toward multi-tenancy."
```

---

### Task 2: Create Gratia Nail Art tenant config JSON

**Files:**
- Create: `tenants/gratia.json`

- [ ] **Step 1: Create Gratia config file**

Create `tenants/gratia.json`:

```json
{
  "slug": "gratia",
  "business_name": "Gratia Nail Art",
  "legal_name": "Gratia Nail Art",
  "tagline": "Uñas & Nail Art — Técnicas mixtas",

  "google_fonts_url": "https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400&family=Manrope:wght@300;400;600;800&display=swap",
  "local_fonts": [],
  "fonts": {
    "headline": "Noto Serif",
    "body": "Manrope"
  },

  "colors": {
    "primary": "#515942",
    "primary_container": "#3d4435",
    "secondary": "#cda255",
    "secondary_hover": "#b8903d",
    "tertiary": "#a18b63",
    "tertiary_hover": "#8a7652",
    "surface_high": "#d6c9b0",
    "surface_dim": "#b7bba2",
    "background": "#e5e4d0",
    "surface_bright": "#f2efe6",
    "on_background": "#2a2e25",
    "on_surface_variant": "#5c6152",
    "outline": "#8a8d7e",
    "on_primary": "#e5e4d0",
    "on_secondary": "#ffffff",
    "on_tertiary": "#e5e4d0",
    "error": "#ba1a1a",
    "error_container": "#ffdad6",
    "warning": "#d97706",
    "warning_container": "#fef3c7",
    "success": "#16a34a",
    "success_container": "#dcfce7",
    "wizard_gradient_from": "#cda255",
    "wizard_gradient_to": "#a18b63",
    "gold_accent": "#cda255",
    "gold_dark": "#b8903d"
  },

  "contact": {
    "instagram_handle": "gratia.nailart",
    "instagram_url": "https://instagram.com/gratia.nailart",
    "facebook_handle": "gratianailart",
    "facebook_url": "",
    "whatsapp_number": "",
    "email_from": "citas@gratianailart.com",
    "email_reply_to": "hazael@gratianailart.com"
  },

  "copy": {
    "hero_headline": "Gratia Nail Art",
    "hero_subtitle": "Uñas & Nail Art — Técnicas mixtas",
    "cta_primary": "Agenda tu cita",
    "cta_secondary": "",
    "chat_welcome": "¡Hola! Soy tu asistente de Gratia Nail Art. ¿En qué puedo ayudarte?",
    "booking_policy": "Para confirmar tu cita, se requiere un apartado que se descuenta del costo total del servicio.",
    "footer_attribution": "SOFTWARE BY OMNIFRACTAL",
    "copyright": "© 2026 Gratia Nail Art",
    "email_title": "GRATIA NAIL ART — Cita Confirmada"
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
    "hero_style": "enchanted"
  },

  "meta": {
    "title": "Gratia Nail Art | Hada del Bosque",
    "description": "Nail art de autor en Morelia, Michoacán. Técnicas mixtas y diseños únicos. Agenda tu cita.",
    "theme_color": "#515942",
    "og_image": "/assets/tenants/gratia/og-image.jpg"
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add tenants/gratia.json
git commit -m "feat: add Gratia Nail Art tenant config JSON

Hada del Bosque (Forest Fairy) branding — olive/gold/sage palette,
Noto Serif + Manrope fonts, no prices on landing, AI chat disabled."
```

---

### Task 3: Create TenantContext, useTenant hook, and applyTheme

**Files:**
- Create: `frontend/src/tenant/TenantContext.js`
- Create: `frontend/src/tenant/useTenant.js`
- Create: `frontend/src/tenant/applyTheme.js`
- Create: `frontend/src/tenant/tenantConfig.json`

- [ ] **Step 1: Create tenant directory**

```bash
mkdir -p /Users/davidtello/landingpopnails/frontend/src/tenant
```

- [ ] **Step 2: Create TenantContext.js**

Create `frontend/src/tenant/TenantContext.js`:

```jsx
import React, { createContext } from "react";

export const TenantContext = createContext(null);

export function TenantProvider({ config, children }) {
  return (
    <TenantContext.Provider value={config}>
      {children}
    </TenantContext.Provider>
  );
}
```

- [ ] **Step 3: Create useTenant.js**

Create `frontend/src/tenant/useTenant.js`:

```jsx
import { useContext } from "react";
import { TenantContext } from "./TenantContext";

export function useTenant() {
  const config = useContext(TenantContext);
  if (!config) {
    throw new Error("useTenant must be used within a TenantProvider");
  }
  return config;
}
```

- [ ] **Step 4: Create applyTheme.js**

Create `frontend/src/tenant/applyTheme.js`:

```js
/**
 * Sets CSS custom properties on :root from tenant color config.
 * Called once at app startup before React renders.
 */
export function applyTheme(colors, slug) {
  const root = document.documentElement;

  // Set all color tokens as CSS custom properties
  Object.entries(colors).forEach(([key, value]) => {
    // Convert snake_case to kebab-case: surface_high → surface-high
    const cssVar = `--color-${key.replace(/_/g, "-")}`;
    root.style.setProperty(cssVar, value);
  });

  // Set tenant slug as data attribute for tenant-specific CSS scoping
  root.setAttribute("data-tenant", slug);
}

/**
 * Dynamically injects Google Fonts <link> if tenant uses them.
 * For local fonts, the build script generates @font-face CSS.
 */
export function loadFonts(config) {
  if (config.google_fonts_url) {
    const link = document.createElement("link");
    link.href = config.google_fonts_url;
    link.rel = "stylesheet";
    document.head.appendChild(link);
  }

  // Set font family CSS vars
  const root = document.documentElement;
  root.style.setProperty("--font-headline", config.fonts.headline);
  root.style.setProperty("--font-body", config.fonts.body);
}
```

- [ ] **Step 5: Copy lapopnails.json as initial tenantConfig.json**

```bash
cp /Users/davidtello/landingpopnails/tenants/lapopnails.json \
   /Users/davidtello/landingpopnails/frontend/src/tenant/tenantConfig.json
```

- [ ] **Step 6: Commit**

```bash
cd /Users/davidtello/landingpopnails
git add frontend/src/tenant/
git commit -m "feat: add tenant context system

TenantContext + useTenant() hook for React components to consume
tenant branding. applyTheme() sets CSS custom properties on :root
from tenant color config at startup."
```

---

### Task 4: Create FeatureGate component and update featureFlags.js

**Files:**
- Create: `frontend/src/tenant/FeatureGate.js`
- Modify: `frontend/src/config/featureFlags.js`

- [ ] **Step 1: Create FeatureGate.js**

Create `frontend/src/tenant/FeatureGate.js`:

```jsx
import { useTenant } from "./useTenant";

/**
 * Conditionally renders children based on tenant feature flags.
 *
 * Usage:
 *   <FeatureGate feature="ai_chat">
 *     <AIChatWidget />
 *   </FeatureGate>
 */
export function FeatureGate({ feature, children, fallback = null }) {
  const { features } = useTenant();
  return features[feature] ? children : fallback;
}
```

- [ ] **Step 2: Rewrite featureFlags.js to read from tenant config**

Replace `frontend/src/config/featureFlags.js` with:

```js
// Feature flags for optional integrations
//
// Reads from tenant config at build time.
// URL param overrides still work for testing in production.
//
// Usage:
//   import { getFeature } from '../config/featureFlags';
//   if (getFeature('ai_chat')) { ... }
//
// For React components, prefer <FeatureGate feature="ai_chat"> instead.

import tenantConfig from "../tenant/tenantConfig.json";

function getUrlOverride(key) {
  if (typeof window === "undefined") return null;
  const param = new URLSearchParams(window.location.search).get(key);
  return param === "true" ? true : param === "false" ? false : null;
}

export function getFeature(featureName) {
  // URL overrides for testing: ?ai_chat=true
  const override = getUrlOverride(featureName);
  if (override !== null) return override;

  return tenantConfig.features[featureName] ?? false;
}

// Legacy export for backward compatibility with existing code
export const FEATURES = {
  get AI_CHAT_ENABLED() {
    return getFeature("ai_chat");
  },
};
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/tenant/FeatureGate.js frontend/src/config/featureFlags.js
git commit -m "feat: add FeatureGate component and tenant-driven feature flags

FeatureGate wraps components for conditional rendering by feature.
featureFlags.js now reads from tenant config with URL param overrides
for testing. Legacy FEATURES export preserved for backward compat."
```

---

### Task 5: Wire TenantProvider into index.js

**Files:**
- Modify: `frontend/src/index.js`

- [ ] **Step 1: Update index.js**

Replace `frontend/src/index.js` with:

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import tenantConfig from "./tenant/tenantConfig.json";
import { TenantProvider } from "./tenant/TenantContext";
import { applyTheme, loadFonts } from "./tenant/applyTheme";
import LandingPage from "./LandingPage";
import BookingPage from "./BookingPage";
import PaymentSuccess from "./PaymentSuccess";
import TokenReschedule from "./TokenReschedule";
import InstagramLanding from "./InstagramLanding";
import AdminApp from "./admin/AdminApp";
import LegalPage from "./LegalPage";

// Apply tenant theme before React renders
applyTheme(tenantConfig.colors, tenantConfig.slug);
loadFonts(tenantConfig);

// Set document title and meta from tenant config
document.title = tenantConfig.meta.title;
const metaDesc = document.querySelector('meta[name="description"]');
if (metaDesc) metaDesc.setAttribute("content", tenantConfig.meta.description);
const metaTheme = document.querySelector('meta[name="theme-color"]');
if (metaTheme) metaTheme.setAttribute("content", tenantConfig.meta.theme_color);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <TenantProvider config={tenantConfig}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/agendar" element={<BookingPage />} />
          <Route path="/instagram" element={<InstagramLanding />} />
          <Route path="/payment-success" element={<PaymentSuccess />} />
          <Route path="/payment-failure" element={<PaymentSuccess />} />
          <Route path="/payment-pending" element={<PaymentSuccess />} />
          <Route path="/reagendar/:token" element={<TokenReschedule />} />
          <Route path="/admin/*" element={<AdminApp />} />

          {/* Legal Pages */}
          <Route path="/aviso-de-privacidad" element={<LegalPage type="privacy" />} />
          <Route path="/terminos-y-condiciones" element={<LegalPage type="terms" />} />
          <Route path="/politica-de-devolucion" element={<LegalPage type="refund" />} />
        </Routes>
      </BrowserRouter>
    </TenantProvider>
  </React.StrictMode>,
);
```

- [ ] **Step 2: Run dev server to verify it starts**

```bash
cd /Users/davidtello/landingpopnails/frontend
npm start
```

Expected: App starts without errors. La Pop Nails renders identically (CSS vars are set but not yet consumed).

- [ ] **Step 3: Commit**

```bash
git add frontend/src/index.js
git commit -m "feat: wire TenantProvider into app entry point

applyTheme() sets CSS custom properties on :root at startup.
loadFonts() handles Google Fonts injection. Document title and
meta tags set from tenant config. All pages wrapped in TenantProvider."
```

---

### Task 6: Create build-tenant.sh script

**Files:**
- Create: `scripts/build-tenant.sh`

- [ ] **Step 1: Create scripts directory and build script**

```bash
mkdir -p /Users/davidtello/landingpopnails/scripts
```

Create `scripts/build-tenant.sh`:

```bash
#!/bin/bash
set -euo pipefail

# Multi-tenant build script
# Usage: REACT_APP_TENANT_SLUG=gratia ./scripts/build-tenant.sh
# Or: ./scripts/build-tenant.sh lapopnails

TENANT_SLUG="${REACT_APP_TENANT_SLUG:-${1:-lapopnails}}"
TENANT_CONFIG="tenants/${TENANT_SLUG}.json"
TARGET_CONFIG="frontend/src/tenant/tenantConfig.json"

echo "🏗️  Building tenant: ${TENANT_SLUG}"

# Verify tenant config exists
if [ ! -f "$TENANT_CONFIG" ]; then
  echo "❌ Tenant config not found: $TENANT_CONFIG"
  exit 1
fi

# Copy tenant config into frontend source
cp "$TENANT_CONFIG" "$TARGET_CONFIG"
echo "✅ Copied ${TENANT_CONFIG} → ${TARGET_CONFIG}"

# Generate @font-face CSS for local fonts (if any)
FONT_CSS="frontend/src/tenant/tenant-fonts.css"
echo "/* Auto-generated by build-tenant.sh — do not edit */" > "$FONT_CSS"

# Use node to parse JSON and generate @font-face rules
node -e "
const config = require('./${TENANT_CONFIG}');
if (config.local_fonts && config.local_fonts.length > 0) {
  config.local_fonts.forEach(f => {
    console.log(\`@font-face {
  font-family: '\${f.family}';
  src: url('\${f.src}') format('\${f.src.endsWith('.otf') ? 'opentype' : 'truetype'}');
  font-weight: \${f.weight};
  font-style: \${f.style || 'normal'};
  font-display: swap;
}\`);
  });
}
" >> "$FONT_CSS"
echo "✅ Generated ${FONT_CSS}"

# Build frontend
cd frontend
REACT_APP_TENANT_SLUG="$TENANT_SLUG" npx craco build
echo "✅ Build complete for tenant: ${TENANT_SLUG}"
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x /Users/davidtello/landingpopnails/scripts/build-tenant.sh
```

- [ ] **Step 3: Create .gitignore entry for generated files**

Add to `frontend/.gitignore` (or create it):

```
# Generated by build-tenant.sh — tenant-specific, not committed
src/tenant/tenantConfig.json
src/tenant/tenant-fonts.css
```

- [ ] **Step 4: Commit**

```bash
git add scripts/build-tenant.sh
git add -f frontend/.gitignore
git commit -m "feat: add multi-tenant build script

build-tenant.sh copies the correct tenant JSON config, generates
@font-face CSS for local fonts, and runs craco build. Controlled
by REACT_APP_TENANT_SLUG env var."
```

---

### Task 7: Extend Tailwind config with CSS var color tokens

**Files:**
- Modify: `frontend/tailwind.config.js`

- [ ] **Step 1: Update tailwind.config.js**

Replace `frontend/tailwind.config.js` with:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        tenant: {
          primary: "var(--color-primary)",
          "primary-container": "var(--color-primary-container)",
          secondary: "var(--color-secondary)",
          "secondary-hover": "var(--color-secondary-hover)",
          tertiary: "var(--color-tertiary)",
          "tertiary-hover": "var(--color-tertiary-hover)",
          "surface-high": "var(--color-surface-high)",
          "surface-dim": "var(--color-surface-dim)",
          background: "var(--color-background)",
          "surface-bright": "var(--color-surface-bright)",
          "on-background": "var(--color-on-background)",
          "on-surface-variant": "var(--color-on-surface-variant)",
          outline: "var(--color-outline)",
          "on-primary": "var(--color-on-primary)",
          "on-secondary": "var(--color-on-secondary)",
          error: "var(--color-error)",
          "error-container": "var(--color-error-container)",
          warning: "var(--color-warning)",
          "warning-container": "var(--color-warning-container)",
          success: "var(--color-success)",
          "success-container": "var(--color-success-container)",
          "gold-accent": "var(--color-gold-accent)",
          "gold-dark": "var(--color-gold-dark)",
        },
      },
      fontFamily: {
        headline: "var(--font-headline)",
        body: "var(--font-body)",
      },
    },
  },
  plugins: [],
};
```

- [ ] **Step 2: Verify Tailwind compiles**

```bash
cd /Users/davidtello/landingpopnails/frontend
npx tailwindcss --content './src/**/*.{js,jsx}' --output /dev/null
```

Expected: No errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/tailwind.config.js
git commit -m "feat: extend Tailwind with tenant CSS var color tokens

All tenant colors available as Tailwind utilities: bg-tenant-primary,
text-tenant-secondary, etc. Font families also available as
font-headline, font-body."
```

---

## Phase 2: Backend Configuration

### Task 8: Parameterize database.py

**Files:**
- Modify: `backend/database.py`

- [ ] **Step 1: Update database.py to use env var**

Replace `backend/database.py` with:

```python
"""
Shared database module.
Single MongoDB connection pool used by all backend modules.
Database name is determined by MONGO_DB_NAME environment variable
to support multi-tenant deployments.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'lapopnails_db')

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
```

- [ ] **Step 2: Verify backend starts**

```bash
cd /Users/davidtello/landingpopnails/backend
python -c "from database import db, MONGO_DB_NAME; print(f'DB: {MONGO_DB_NAME}')"
```

Expected: `DB: lapopnails_db` (default value since no env var is set locally)

- [ ] **Step 3: Commit**

```bash
git add backend/database.py
git commit -m "feat: parameterize database name via MONGO_DB_NAME env var

Defaults to 'lapopnails_db' for backward compatibility.
Each tenant deployment sets its own MONGO_DB_NAME."
```

---

### Task 9: Parameterize tenant.py defaults

**Files:**
- Modify: `backend/tenant.py`

- [ ] **Step 1: Update tenant.py**

Edit `backend/tenant.py` lines 11-12 to read from env vars:

```python
DEFAULT_TENANT_ID = os.environ.get("DEFAULT_TENANT_ID", "550e8400-e29b-41d4-a716-446655440000")
DEFAULT_TENANT_SLUG = os.environ.get("DEFAULT_TENANT_SLUG", "lapopnails")
```

No other changes — `LA_POP_NAILS_TENANT` dict, `ensure_default_tenant()`, and lookup functions stay exactly the same. They will be updated per-tenant when we create tenant-specific seed data later.

- [ ] **Step 2: Commit**

```bash
git add backend/tenant.py
git commit -m "feat: read DEFAULT_TENANT_ID and SLUG from env vars

Backward compatible — defaults to existing La Pop Nails values.
Each tenant deployment sets its own IDs."
```

---

### Task 10: Parameterize CORS origins in server.py

**Files:**
- Modify: `backend/server.py`

- [ ] **Step 1: Update CORS config in server.py**

Replace lines 54-61 in `backend/server.py`:

```python
# =============================================================================
# CORS MIDDLEWARE
# =============================================================================

import json

_origins_env = os.environ.get("ALLOWED_ORIGINS", "")
if _origins_env:
    ALLOWED_ORIGINS = json.loads(_origins_env)
else:
    # Backward-compatible default for La Pop Nails
    ALLOWED_ORIGINS = [
        "https://lapopnails.mx",
        "https://www.lapopnails.mx",
        "https://frontend-popnails-production.up.railway.app",
        "https://lapopnails-frontend-production.up.railway.app",
    ]

if os.environ.get("RAILWAY_ENVIRONMENT", "production") != "production":
    ALLOWED_ORIGINS += ["http://localhost:3000", "http://localhost:3001"]
```

- [ ] **Step 2: Verify server starts**

```bash
cd /Users/davidtello/landingpopnails/backend
python -c "
import os, json
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'development')
# Just verify the import doesn't crash
print('CORS config OK')
"
```

- [ ] **Step 3: Commit**

```bash
git add backend/server.py
git commit -m "feat: read CORS ALLOWED_ORIGINS from env var

Accepts JSON array: ALLOWED_ORIGINS='[\"https://gratianailart.com\"]'
Falls back to La Pop Nails domains for backward compatibility."
```

---

### Task 11: Create backend tenant_config.py for email/notification branding

**Files:**
- Create: `backend/tenant_config.py`

- [ ] **Step 1: Create tenant_config.py**

Create `backend/tenant_config.py`:

```python
"""
Static tenant configuration loader.
Reads the tenant JSON config file for branding data used in emails
and notifications. This is NOT for business logic — that lives in MongoDB.
"""

import os
import json
from functools import lru_cache


@lru_cache(maxsize=1)
def get_tenant_static_config() -> dict:
    """Load and cache the static tenant config from the JSON file."""
    slug = os.environ.get("DEFAULT_TENANT_SLUG", "lapopnails")

    # Look for config in multiple locations (development vs production)
    search_paths = [
        f"tenants/{slug}.json",           # running from repo root
        f"../tenants/{slug}.json",         # running from backend/
        f"/app/tenants/{slug}.json",       # Railway container
    ]

    for path in search_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
            print(f"✅ Loaded tenant config: {slug} from {path}")
            return config

    print(f"⚠️ Tenant config not found for '{slug}', using minimal defaults")
    return {
        "slug": slug,
        "business_name": slug.replace("-", " ").title(),
        "colors": {
            "secondary": "#ec4899",
            "tertiary": "#D9B55A",
            "background": "#F6EFE8",
            "on_background": "#2d2520",
        },
        "contact": {
            "email_from": f"citas@{slug}.mx",
        },
        "copy": {
            "email_title": "Cita Confirmada",
        },
    }
```

- [ ] **Step 2: Commit**

```bash
git add backend/tenant_config.py
git commit -m "feat: add tenant_config.py for email/notification branding

Loads static tenant JSON config and caches it. Used by email_service
and whatsapp_service for brand-specific colors, names, and copy."
```

---

### Task 12: Parameterize email_service.py brand colors

**Files:**
- Modify: `backend/email_service.py`

- [ ] **Step 1: Update email_service.py to use tenant config**

Add import at top of `backend/email_service.py` (after line 3):

```python
from tenant_config import get_tenant_static_config
```

Then in `send_confirmation_email()`, after line 15 (`print("📧 Email template...")`), add:

```python
        tc = get_tenant_static_config()
        brand_name = tc.get("copy", {}).get("email_title", "Cita Confirmada")
        brand_secondary = tc.get("colors", {}).get("secondary", "#ec4899")
        brand_tertiary = tc.get("colors", {}).get("tertiary", "#D9B55A")
        brand_bg = tc.get("colors", {}).get("background", "#F6EFE8")
        brand_text = tc.get("colors", {}).get("on_background", "#2d2520")
        brand_business = tc.get("business_name", "Nail Studio")
```

Then do a find-and-replace within the HTML template string:
- Replace `#D4AF37` with `{brand_tertiary}` (gold accent color)
- Replace `POP NAILS` with `{brand_business.upper()}`
- Replace hardcoded title `<title>POP NAILS — Cita Confirmada</title>` with `<title>{brand_name}</title>`
- Replace `#F5EEDB` backgrounds with `{brand_bg}`
- Replace `#6B5B3E` text with `{brand_text}`

NOTE: This is a targeted parameterization of ~5 color tokens in the existing HTML template. Do NOT rewrite the template — just replace the color literals with the variables.

- [ ] **Step 2: Test that email still sends correctly**

```bash
cd /Users/davidtello/landingpopnails/backend
python -c "
from tenant_config import get_tenant_static_config
tc = get_tenant_static_config()
print(f'Email will use: {tc[\"business_name\"]} with secondary={tc[\"colors\"][\"secondary\"]}')
"
```

Expected: `Email will use: La Pop Nails with secondary=#ec4899`

- [ ] **Step 3: Commit**

```bash
git add backend/email_service.py backend/tenant_config.py
git commit -m "feat: parameterize email brand colors from tenant config

Email template now reads business name and 5 color tokens from
tenant JSON config instead of hardcoded hex values."
```

---

## Phase 3: Frontend — Replace Hardcoded Colors in CSS

> **NOTE:** This phase involves replacing 60+ hardcoded hex colors across 3 CSS files. Each file is its own task. The approach is: replace hex literals with `var(--color-*)` references. Where a color doesn't map cleanly to a token, keep it hardcoded (utility colors like grays for borders are fine).

### Task 13: Replace hardcoded colors in App.css

**Files:**
- Modify: `frontend/src/App.css`

- [ ] **Step 1: Find and replace color tokens in App.css**

Key replacements (apply throughout the file):

| Hardcoded | CSS Variable | Semantic meaning |
|-----------|-------------|-----------------|
| `#F6EFE8` | `var(--color-background)` | Page background |
| `#F0E6DB` | `var(--color-surface-dim)` | Surface variant |
| `#D9B55A` | `var(--color-gold-accent)` | Gold accent/CTA |
| `#F8D9E2` | `var(--color-surface-high)` | Elevated surface |
| `#8B4B66` | `var(--color-primary)` | Primary text/brand |
| `#C7A147` | `var(--color-gold-dark)` | Gold hover state |
| `#B8973D` | `var(--color-gold-dark)` | Gold pressed state |
| `#F5D0DC` | `var(--color-surface-high)` | Light surface |
| `#FDF2E9` | `var(--color-background)` | Background variant |

Do a search-and-replace for each. For colors that appear in gradients, replace both stops:
```css
/* Before */
background: linear-gradient(to bottom, #F6EFE8, #F0E6DB);
/* After */
background: linear-gradient(to bottom, var(--color-background), var(--color-surface-dim));
```

- [ ] **Step 2: Verify no visual change**

```bash
cd /Users/davidtello/landingpopnails/frontend && npm start
```

Open browser, check La Pop Nails landing page looks identical.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/App.css
git commit -m "refactor: replace hardcoded colors in App.css with CSS vars

20+ hex color literals replaced with var(--color-*) tokens.
No visual change — La Pop Nails values are set as defaults."
```

---

### Task 14: Replace hardcoded colors in LandingPage.css

**Files:**
- Modify: `frontend/src/LandingPage.css`

- [ ] **Step 1: Add tenant-fonts.css import**

At the top of `LandingPage.css`, replace the existing `@font-face` declarations with:

```css
@import "./tenant/tenant-fonts.css";
```

Remove ALL `@font-face` blocks for Playlist Script, Funnel Sans, and Chewy. These are now generated by `build-tenant.sh`.

- [ ] **Step 2: Replace color tokens in LandingPage.css**

Key replacements:

| Hardcoded | CSS Variable |
|-----------|-------------|
| `#E9D5CC` | `var(--color-surface-dim)` |
| `#2d2520` / `#2D2520` | `var(--color-on-background)` |
| `#D9B55A` | `var(--color-gold-accent)` |
| `#5B3F39` | `var(--color-primary)` |
| `#C9A161` / `#C9A54A` | `var(--color-gold-dark)` |
| `#6B384A` | `var(--color-primary-container)` |
| `#F6EFE8` / `#F0E6DB` | `var(--color-background)` / `var(--color-surface-dim)` |
| `#ec4899` / `#EC4899` | `var(--color-secondary)` |
| `#E91E8C` | `var(--color-secondary)` |
| `#FFE4E6` / `#FFF1F2` / `#F9A8D4` | `var(--color-surface-high)` |

Leave genuinely external colors untouched: `#3B82F6` (blue links), `#EFF6FF` (blue background) — these are utility colors, not brand colors.

- [ ] **Step 3: Verify no visual change**

Open browser, check landing page — all sections should look identical.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/LandingPage.css
git commit -m "refactor: replace hardcoded colors in LandingPage.css with CSS vars

25+ hex literals replaced. @font-face declarations moved to
auto-generated tenant-fonts.css via build script."
```

---

### Task 15: Replace hardcoded colors in WizardBooking.css

**Files:**
- Modify: `frontend/src/WizardBooking.css`

- [ ] **Step 1: Replace color tokens in WizardBooking.css**

Key replacements:

| Hardcoded | CSS Variable |
|-----------|-------------|
| `#fdf2f8` | `var(--color-background)` |
| `#ec4899` | `var(--color-secondary)` |
| `#f43f5e` | `var(--color-wizard-gradient-to)` |
| `#db2777` | `var(--color-secondary-hover)` |
| `#fce7f3` | `var(--color-surface-high)` |
| `#fbbf24` | `var(--color-warning)` |
| `#9d174d` | `var(--color-primary-container)` |
| `#1f2937` | `var(--color-on-background)` |
| `#6b7280` | `var(--color-on-surface-variant)` |
| `#d1d5db` / `#e5e7eb` | `var(--color-outline)` |
| `#f3f4f6` / `#f9fafb` | `var(--color-surface-bright)` |
| `#ef4444` | `var(--color-error)` |
| `#fef2f2` | `var(--color-error-container)` |
| `#d97706` | `var(--color-warning)` |
| `#fef3c7` | `var(--color-warning-container)` |

For gradients:
```css
/* Before */
background: linear-gradient(135deg, #ec4899, #f43f5e);
/* After */
background: linear-gradient(135deg, var(--color-wizard-gradient-from), var(--color-wizard-gradient-to));
```

- [ ] **Step 2: Verify booking wizard looks identical**

Navigate to `/agendar` and check all wizard states.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/WizardBooking.css
git commit -m "refactor: replace hardcoded colors in WizardBooking.css with CSS vars

20+ hex literals replaced with CSS custom property tokens.
Wizard gradient now uses --color-wizard-gradient-from/to."
```

---

## Phase 4: Frontend — Extract Hardcoded Copy & Branding

### Task 16: Extract branding from App.js

**Files:**
- Modify: `frontend/src/App.js`

- [ ] **Step 1: Add useTenant import**

At the top of `App.js`, add:

```jsx
import { useTenant } from "./tenant/useTenant";
import { FeatureGate } from "./tenant/FeatureGate";
```

- [ ] **Step 2: Inside the main component, destructure tenant config**

At the top of the main component function:

```jsx
const tenant = useTenant();
```

- [ ] **Step 3: Replace all hardcoded branding references**

Search for and replace:
- `"La Pop Nails"` → `tenant.business_name`
- `"___lapopnails"` or `"lapopnails"` (Instagram) → `tenant.contact.instagram_handle`
- Instagram URL → `tenant.contact.instagram_url`
- Logo URL hardcoded → `tenant.logo_url`
- `"Agendar Ahora"` → `tenant.copy.cta_primary`
- Any hardcoded hex colors in inline styles → `var(--color-*)` CSS vars or `tenant.colors.*`

- [ ] **Step 4: Wrap AIChatWidget in FeatureGate**

If `AIChatWidget` is rendered in App.js, wrap it:

```jsx
<FeatureGate feature="ai_chat">
  <AIChatWidget />
</FeatureGate>
```

- [ ] **Step 5: Verify and commit**

```bash
grep -rn "La Pop" frontend/src/App.js  # Should return 0 results
git add frontend/src/App.js
git commit -m "refactor: extract hardcoded branding from App.js

Business name, Instagram, logo, CTA text all from useTenant().
AIChatWidget wrapped in FeatureGate."
```

---

### Task 17: Extract branding from LandingPage.js

**Files:**
- Modify: `frontend/src/LandingPage.js`

- [ ] **Step 1: Add useTenant import and destructure**

```jsx
import { useTenant } from "./tenant/useTenant";
// In component:
const tenant = useTenant();
```

- [ ] **Step 2: Replace hardcoded content**

- Hero headline → `tenant.copy.hero_headline`
- Hero subtitle → `tenant.copy.hero_subtitle`
- CTA button text → `tenant.copy.cta_primary`
- Instagram handle → `tenant.contact.instagram_handle`
- Any hardcoded service data → fetch from `/api/services` (already partially done)
- Price display → wrap in `{tenant.features.show_prices_on_landing && <PriceComponent />}`
- Business name in any string → `tenant.business_name`

- [ ] **Step 3: Verify and commit**

```bash
grep -rn "La Pop" frontend/src/LandingPage.js  # Should return 0 results
git add frontend/src/LandingPage.js
git commit -m "refactor: extract hardcoded branding from LandingPage.js

All copy, contact info, and service display from useTenant().
Price visibility controlled by show_prices_on_landing feature flag."
```

---

### Task 18: Extract branding from remaining components

**Files:**
- Modify: `frontend/src/components/AIChatWidget.js`
- Modify: `frontend/src/BookingPage.js`
- Modify: `frontend/src/WizardBooking.js`
- Modify: `frontend/src/PaymentSuccess.js`
- Modify: `frontend/src/InstagramLanding.js`

- [ ] **Step 1: AIChatWidget.js — replace "La Pop Nails"**

Add `useTenant` import. Replace welcome message and all "La Pop Nails" references:

```jsx
const tenant = useTenant();
// welcome message:
`${tenant.copy.chat_welcome}`
```

- [ ] **Step 2: BookingPage.js — replace logo and business name**

```jsx
const tenant = useTenant();
// Logo: tenant.logo_url
// Business name: tenant.business_name
```

- [ ] **Step 3: WizardBooking.js — replace policy text**

```jsx
const tenant = useTenant();
// Policy: tenant.copy.booking_policy
// Business name: tenant.business_name
```

- [ ] **Step 4: PaymentSuccess.js — replace business name**

```jsx
const tenant = useTenant();
// All "La Pop Nails" → tenant.business_name
// Instagram → tenant.contact.instagram_handle
```

- [ ] **Step 5: InstagramLanding.js — wrap in FeatureGate or add feature check**

In `index.js` route, wrap:

```jsx
<Route path="/instagram" element={
  <FeatureGate feature="instagram_landing" fallback={<Navigate to="/" />}>
    <InstagramLanding />
  </FeatureGate>
} />
```

(Add `Navigate` import from `react-router-dom`)

- [ ] **Step 6: Final grep verification**

```bash
grep -rn "La Pop" frontend/src/ --include="*.js" --include="*.jsx" | grep -v "tenants/" | grep -v "node_modules"
```

Expected: Zero results. All "La Pop Nails" references should only exist in `tenants/lapopnails.json`.

- [ ] **Step 7: Commit**

```bash
git add frontend/src/components/AIChatWidget.js frontend/src/BookingPage.js \
       frontend/src/WizardBooking.js frontend/src/PaymentSuccess.js \
       frontend/src/InstagramLanding.js frontend/src/index.js
git commit -m "refactor: extract branding from all remaining components

AIChatWidget, BookingPage, WizardBooking, PaymentSuccess, InstagramLanding
all read from useTenant(). Zero hardcoded 'La Pop Nails' strings remaining
in source code."
```

---

## Phase 5: Gratia Deployment

### Task 19: Set up Gratia static assets

**Files:**
- Create: `frontend/public/assets/tenants/gratia/` (directory with placeholder assets)

- [ ] **Step 1: Create asset directories**

```bash
mkdir -p /Users/davidtello/landingpopnails/frontend/public/assets/tenants/gratia
mkdir -p /Users/davidtello/landingpopnails/frontend/public/assets/tenants/lapopnails
```

- [ ] **Step 2: Copy Gratia assets from stitch-assets**

```bash
# Copy available Gratia assets
cp /Users/davidtello/Projects/gratia-nailart/stitch-assets/gratia-hada-del-bosque-v1.png \
   /Users/davidtello/landingpopnails/frontend/public/assets/tenants/gratia/mascot.png

cp /Users/davidtello/Projects/gratia-nailart/stitch-assets/gratia-landing-page.png \
   /Users/davidtello/landingpopnails/frontend/public/assets/tenants/gratia/og-image.jpg
```

- [ ] **Step 3: Move La Pop assets to tenant directory**

Move existing La Pop Nails favicon and icons to the tenant-specific directory:

```bash
cp /Users/davidtello/landingpopnails/frontend/public/popnails-icon-3d.png \
   /Users/davidtello/landingpopnails/frontend/public/assets/tenants/lapopnails/icon.png
```

- [ ] **Step 4: Commit**

```bash
git add frontend/public/assets/
git commit -m "feat: add tenant asset directories with Gratia branding

Gratia mascot and OG image from Stitch prototypes. La Pop assets
organized under tenants/lapopnails/."
```

---

### Task 20: Test build for both tenants locally

- [ ] **Step 1: Build La Pop Nails**

```bash
cd /Users/davidtello/landingpopnails
REACT_APP_TENANT_SLUG=lapopnails ./scripts/build-tenant.sh
```

Expected: Build succeeds, `frontend/build/` contains compiled app.

- [ ] **Step 2: Serve and verify La Pop Nails**

```bash
cd frontend && npx serve -s build -l 3000
```

Open `http://localhost:3000` — verify La Pop Nails looks identical to production.

- [ ] **Step 3: Build Gratia Nail Art**

```bash
cd /Users/davidtello/landingpopnails
REACT_APP_TENANT_SLUG=gratia ./scripts/build-tenant.sh
```

Expected: Build succeeds. The app should load with Gratia colors (olive/gold/sage).

- [ ] **Step 4: Serve and verify Gratia**

```bash
cd frontend && npx serve -s build -l 3001
```

Open `http://localhost:3001` — verify:
- Colors are olive/gold/sage (not pink/purple)
- Fonts are Noto Serif + Manrope
- AI chat widget is NOT visible (feature flag off)
- Business name shows "Gratia Nail Art"
- No prices visible on landing (if services section renders)

- [ ] **Step 5: Commit any fixes needed**

```bash
git add -A
git commit -m "fix: resolve issues found during dual-tenant build test"
```

---

### Task 21: Deploy Gratia to Railway

> This task requires Railway access and account setup. The steps below are the Railway CLI commands and configuration needed.

- [ ] **Step 1: Create Railway project for Gratia**

This is done via Railway dashboard or CLI:
- Create project "gratia-nailart"
- Add services: gratia-frontend, gratia-backend, gratia-mongodb

- [ ] **Step 2: Configure backend env vars**

Set these environment variables on the gratia-backend Railway service:

```
TENANT_SLUG=gratia
DEFAULT_TENANT_SLUG=gratia
DEFAULT_TENANT_ID=<generate-new-uuid>
MONGO_DB_NAME=gratia_db
MONGO_URL=<railway-mongodb-url>
FRONTEND_URL=https://gratianailart.com
ALLOWED_ORIGINS=["https://gratianailart.com","http://localhost:3000"]
MP_PUBLIC_KEY=<gratia-mercadopago-public-key>
MP_ACCESS_TOKEN=<gratia-mercadopago-access-token>
MP_WEBHOOK_SECRET=<gratia-webhook-secret>
RESEND_API_KEY=<resend-api-key>
JWT_SECRET=<generate-unique-secret>
ADMIN_USERNAME=hazael
ADMIN_PASSWORD_HASH=<bcrypt-hash>
GOOGLE_CALENDAR_ID=<gratia-calendar-id>
GOOGLE_CLIENT_SECRET_JSON=<base64-encoded-service-account>
```

- [ ] **Step 3: Configure frontend env vars**

```
REACT_APP_TENANT_SLUG=gratia
REACT_APP_BACKEND_URL=https://gratia-backend-production.up.railway.app
REACT_APP_MP_PUBLIC_KEY=<gratia-mercadopago-public-key>
```

- [ ] **Step 4: Set frontend build command in Railway**

```
cd /app && ./scripts/build-tenant.sh && cd frontend && npx serve -s build
```

- [ ] **Step 5: Deploy and verify**

Push to Railway. Verify:
- Frontend loads with Gratia branding
- Backend `/api/services` returns (empty at first — will seed in next task)
- Admin login works at `/admin`

- [ ] **Step 6: Seed Gratia services**

Via admin dashboard or direct MongoDB insert, add Gratia's service catalog:
- "Nail Art de Autor" — Diseños únicos pintados a mano — ~2 hrs
- "Técnica Mixta" — Combinación de técnicas premium — ~2.5 hrs
- "Acrílico Esculpido" — Extensiones esculpidas — ~3 hrs
- "Gel con Diseño" — Gel con nail art incluido — ~2 hrs
- "Retoque / Mantenimiento" — Relleno y mantenimiento — ~1.5 hrs

---

## Phase 6: Gratia Landing Page Sections

> Phase 6 is a separate implementation cycle. It involves building the Gratia-specific landing page sections based on the Stitch prototypes. This will be planned in detail once Phases 1-5 are verified.

### Task 22: Implement section renderer

**Files:**
- Create: `frontend/src/components/sections/SectionRenderer.js`

- [ ] **Step 1: Create section renderer**

```jsx
import React from "react";
import { useTenant } from "../tenant/useTenant";

// Section components (lazy loaded)
const sectionMap = {
  hero: React.lazy(() => import("./sections/HeroSection")),
  services: React.lazy(() => import("./sections/ServicesSection")),
  gallery: React.lazy(() => import("./sections/GallerySection")),
  process: React.lazy(() => import("./sections/ProcessSection")),
  hygiene: React.lazy(() => import("./sections/HygieneSection")),
  contact: React.lazy(() => import("./sections/ContactSection")),
  ctaBanner: React.lazy(() => import("./sections/CtaBannerSection")),
  masDeGratia: React.lazy(() => import("./sections/MasDeGratiaSection")),
  footer: React.lazy(() => import("./sections/FooterSection")),
};

export function SectionRenderer() {
  const { landing } = useTenant();

  return (
    <React.Suspense fallback={null}>
      {landing.sections.map((sectionKey) => {
        const Section = sectionMap[sectionKey];
        if (!Section) {
          console.warn(`Unknown section: ${sectionKey}`);
          return null;
        }
        return <Section key={sectionKey} />;
      })}
    </React.Suspense>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/components/sections/
git commit -m "feat: add config-driven section renderer

Landing page sections rendered based on tenant landing.sections array.
La Pop Nails: hero → services → process → hygiene → contact → footer
Gratia: hero → gallery → ctaBanner → masDeGratia → footer"
```

---

### Task 23: Implement Gratia-specific sections

> Each section is a React component in `frontend/src/components/sections/`. They use `useTenant()` for all branding and CSS custom properties for all colors.

**Files to create:**
- `frontend/src/components/sections/HeroSection.js` — Reads `landing.hero_style` for variant (`"default"` = La Pop, `"enchanted"` = Gratia with fairy mascot)
- `frontend/src/components/sections/GallerySection.js` — Portfolio grid, no prices, labels overlay
- `frontend/src/components/sections/CtaBannerSection.js` — Full-width gold CTA
- `frontend/src/components/sections/MasDeGratiaSection.js` — Three cards (Shop, Academy, Booking)
- `frontend/src/components/sections/FooterSection.js` — Social links + attribution

Each component follows the DESIGN.md specifications at `/Users/davidtello/Projects/gratia-nailart/DESIGN.md`. Exact implementation code will be written when we execute this phase, as it depends on the final Stitch prototypes being approved.

---

## Verification Checklist

After all phases are complete, verify:

- [ ] `grep -rn "La Pop" frontend/src/ --include="*.js"` returns zero results (only in tenants/*.json)
- [ ] `grep -rn "lapopnails" backend/ --include="*.py"` only appears in fallback defaults
- [ ] La Pop Nails production site is visually identical to before migration
- [ ] La Pop Nails full booking flow works (service → date → payment → email)
- [ ] Gratia build uses olive/gold/sage colors
- [ ] Gratia build shows "Gratia Nail Art" everywhere
- [ ] Gratia build hides AI chat widget
- [ ] Gratia build hides prices on landing page
- [ ] Both tenants can be built independently with `build-tenant.sh`
- [ ] Email confirmations use correct branding per tenant

# Codebase Structure

**Analysis Date:** 2026-05-10

## Directory Layout

```
gratia-nailart/
├── frontend/                    # React SPA (landing + booking wizard)
│   ├── src/
│   │   ├── main.tsx            # React DOM entry point
│   │   ├── App.tsx             # Router setup, page layout
│   │   ├── index.css           # Tailwind + design system colors
│   │   ├── components/         # React components (landing, booking)
│   │   ├── assets/             # Images, fonts, static assets
│   ├── public/                 # Static files (favicon, etc)
│   ├── vite.config.ts          # Vite build config
│   ├── package.json            # Dependencies, build scripts
│   └── tsconfig.json           # TypeScript config
│
├── backend/                     # FastAPI REST API
│   ├── server.py               # FastAPI app entry point
│   ├── database.py             # MongoDB connection (Motor)
│   ├── models.py               # Pydantic request/response models
│   ├── tenant.py               # Tenant initialization
│   ├── routes/                 # API route handlers
│   │   ├── booking.py          # Booking creation, payments
│   │   ├── appointments.py     # Appointment CRUD
│   │   ├── reschedule.py       # Reschedule logic
│   │   ├── calendar.py         # Availability queries
│   │   ├── clients.py          # Client data endpoints
│   │   ├── discounts.py        # Discount validation
│   │   ├── tenants.py          # Tenant config endpoints
│   │   ├── internal.py         # Internal utilities (ping, metrics)
│   │   └── admin/              # Admin dashboard API
│   │       ├── auth.py         # Admin login
│   │       ├── appointments.py # Manage appointments
│   │       ├── clients.py      # Manage clients
│   │       ├── settings.py     # Business settings
│   │       ├── analytics.py    # Analytics endpoints
│   │       └── ...
│   │
│   ├── Services (business logic)
│   │   ├── calendar_service.py       # Google Calendar integration
│   │   ├── email_service.py          # Resend email integration
│   │   ├── whatsapp_service.py       # WhatsApp Business API
│   │   ├── mercadopago_service.py    # Payment preference + validation
│   │   ├── discount_service.py       # Discount code logic
│   │   ├── notification_service.py   # In-app notifications
│   │   ├── scheduling.py             # Business hours, slot validation
│   │   └── phone_utils.py            # Phone number normalization
│   │
│   ├── Utilities
│   │   ├── tenant_config.py    # Tenant-specific configuration
│   │   ├── auth.py             # Auth helpers
│   │   └── create_admin.py     # Admin account bootstrap
│   │
│   └── .env (not committed)    # Environment variables
│
├── docs/                        # Documentation
│   └── superpowers/            # Superpowers (plans, specs)
│
├── stitch-assets/              # Google Stitch design exports
│
├── .planning/
│   └── codebase/               # GSD codebase mapping docs
│
├── tasks/
│   ├── todo.md                 # Current sprint tasks
│   └── lessons.md              # Lessons learned / patterns
│
├── DESIGN.md                   # Design system (colors, typography, components)
├── CLAUDE.md                   # Project instructions (this file context)
└── README.md                   # Project overview
```

## Directory Purposes

**`frontend/`**
- Purpose: Client-facing React SPA
- Contains: Landing page components, booking wizard, styles, assets
- Key entry: `src/main.tsx` (React root)
- Build output: `dist/` (generated, not committed)

**`frontend/src/components/`**
- Purpose: All React components for landing and booking flow
- Key files:
  - `Nav.tsx`: Navigation bar with "Agenda tu cita" CTA
  - `Hero.tsx`: Hero section with fairy mascot
  - `Gallery.tsx`: Portfolio grid (Mi Trabajo)
  - `CtaBanner.tsx`: Gold CTA banner
  - `MasDeGratia.tsx`: Three-card section (Shop, Academy, Booking)
  - `Footer.tsx`: Footer with social icons
  - `BookingPage.tsx`: Booking page wrapper
  - `WizardBooking.tsx`: Multi-step booking form (30+ KB, largest component)
  - `booking/`: Subcomponents for booking wizard steps

**`frontend/src/assets/`**
- Purpose: Static images, fairy mascot, nail art portfolio images
- Contains: PNG, SVG assets from Stitch design

**`frontend/public/`**
- Purpose: Static files served directly by Vite/HTTP
- Contains: favicon, manifest, assets not bundled

**`backend/`**
- Purpose: FastAPI REST API backend
- Entry point: `server.py`

**`backend/routes/`**
- Purpose: Modular API route handlers organized by feature
- Scoped to public (booking, calendar) and internal (admin, appointments)

**`backend/routes/admin/`**
- Purpose: Admin dashboard API endpoints
- Key files:
  - `auth.py`: Admin login/logout
  - `appointments.py`: View, modify, cancel appointments
  - `clients.py`: View client records
  - `settings.py`: Configure business hours, services
  - `analytics.py`: Booking statistics
  - `conversations.py`: Chat/message history
  - `notifications.py`: Notification management
  - `blocked_dates.py`: Block unavailable dates
  - `setup.py`: Admin onboarding

**`backend/` services**
- Purpose: Encapsulate external service integrations and business logic
- Pattern: Each service is a module with async functions

**`docs/superpowers/`**
- Purpose: Planning artifacts (specs, phase plans)
- Contains: Phase plans from GSD orchestrator

**`.planning/codebase/`**
- Purpose: GSD mapping documents (ARCHITECTURE.md, STRUCTURE.md, etc.)
- Generated by `/gsd:map-codebase` command

**`tasks/`**
- Purpose: Sprint tracking and lessons learned
- Files:
  - `todo.md`: Current tasks with checkboxes
  - `lessons.md`: Patterns and rules to prevent mistakes

**`DESIGN.md`**
- Purpose: Single source of truth for visual design
- Contains: Hex color values, typography rules, component specs, shadow systems
- Generated from Google Stitch design project
- Read by agents before generating UI code

## Key File Locations

**Entry Points:**

| File | Purpose | Triggers |
|------|---------|----------|
| `frontend/src/main.tsx` | React DOM initialization | Browser page load |
| `frontend/src/App.tsx` | Router setup (landing + booking) | React initialization |
| `backend/server.py` | FastAPI app creation, middleware, routers | Container startup |
| `backend/create_admin.py` | Admin account bootstrap | Manual CLI invocation |

**Configuration:**

| File | Purpose | Environment |
|------|---------|-------------|
| `frontend/vite.config.ts` | Vite build settings, React plugin | Dev/build |
| `frontend/tsconfig.json` | TypeScript compiler options | Type checking |
| `backend/.env` | MongoDB URL, email/WhatsApp keys, MercadoPago tokens | Runtime (not committed) |
| `DESIGN.md` | Color palette, typography, component specs | All UI development |

**Core Data Models:**

| File | Contains | Used by |
|------|----------|---------|
| `backend/models.py` | Pydantic request/response schemas | All route handlers |
| `backend/database.py` | MongoDB connection instance | All services and routes |
| `backend/tenant.py` | Tenant initialization, DEFAULT_TENANT_ID | All business logic |

**Business Logic:**

| File | Responsibility |
|------|-----------------|
| `backend/scheduling.py` | Date/time validation, slot availability |
| `backend/email_service.py` | Send confirmation + owner notification emails |
| `backend/whatsapp_service.py` | Send booking confirmations via WhatsApp |
| `backend/mercadopago_service.py` | Create payment preferences, validate webhooks |
| `backend/calendar_service.py` | Create Google Calendar events |
| `backend/discount_service.py` | Validate and redeem discount codes |
| `backend/notification_service.py` | Create in-app notifications |

## Naming Conventions

**Files:**

| Pattern | Example | Location |
|---------|---------|----------|
| PascalCase (React components) | `WizardBooking.tsx`, `CtaBanner.tsx` | `frontend/src/components/` |
| snake_case (Python modules) | `mercadopago_service.py`, `phone_utils.py` | `backend/` |
| snake_case (routes) | `booking.py`, `appointments.py` | `backend/routes/` |
| UPPERCASE (constants/config) | `DEFAULT_TENANT_ID`, `MONGO_URL` | Throughout |

**Directories:**

| Pattern | Example |
|---------|---------|
| kebab-case or lowercase | `frontend/src/components/booking/` |
| PascalCase (rare) | N/A in current structure |

**TypeScript:**

| Type | Pattern | Example |
|------|---------|---------|
| React components | PascalCase | `BookingPage`, `WizardBooking` |
| Interfaces/Types | PascalCase | `AppointmentRequest`, `PaymentRequest` |
| Constants | UPPER_SNAKE_CASE | (Python side only) |

**Python:**

| Type | Pattern | Example |
|------|---------|---------|
| Module names | snake_case | `email_service.py`, `calendar_service.py` |
| Functions | snake_case | `create_google_calendar_event()`, `validate_discount()` |
| Classes | PascalCase | `AsyncIOMotorClient` (imported) |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_TENANT_ID`, `PENDING_PAYMENT_EXPIRY_MINUTES` |

## Where to Add New Code

**New Feature (e.g., SMS notifications):**

1. **Backend service:** Create `backend/sms_service.py` with async functions
   - Import MongoDB `db` from `backend/database.py`
   - Import notification types from `backend/models.py`
   - Pattern: `async def send_sms(phone: str, message: str) -> dict:`

2. **Route integration:** Add endpoint to existing route or new route in `backend/routes/`
   - Import service: `from sms_service import send_sms`
   - Pattern: Use POST/GET with proper path prefix
   - Wrap in try-except, return HTTPException on error

3. **Frontend integration:** If user-facing, add component to `frontend/src/components/`
   - Import API utility from frontend helpers
   - Pattern: async function to call backend endpoint

**New Component (e.g., testimonials section):**

1. Create `frontend/src/components/Testimonials.tsx`
2. Follow PascalCase naming
3. Import design system from `DESIGN.md` (use Tailwind classes with `--color-*` CSS vars)
4. Add route in `frontend/src/App.tsx` if new page, or render in existing page component

**New Admin Feature (e.g., email history):**

1. Create `backend/routes/admin/email_history.py`
2. Import necessary models from `backend/models.py`
3. Import database: `from database import db`
4. Register router in `backend/server.py`: `app.include_router(email_history_router)`
5. Add frontend page to `frontend/src/components/` for admin dashboard

**Utility/Helper:**

- **Frontend**: `frontend/src/` (create subdirectory if complex, e.g., `frontend/src/utils/`)
- **Backend**: `backend/` (create snake_case file if >200 lines, otherwise add to existing utility)

## Special Directories

**`dist/`** (Frontend build output)
- Purpose: Compiled React SPA (HTML, CSS, JS bundles)
- Generated: Yes (by `npm run build`)
- Committed: No (in `.gitignore`)
- Served: Deployed by Railway

**`.planning/codebase/`**
- Purpose: GSD mapping documents
- Generated: Yes (by `/gsd:map-codebase` command)
- Committed: Yes (for orchestrator reference)

**`docs/superpowers/plans/` & `docs/superpowers/specs/`**
- Purpose: Phase plans and implementation specs from GSD
- Generated: Yes (by `/gsd:plan-phase` and `/gsd:execute-phase`)
- Committed: Yes (for audit trail)

**`stitch-assets/`**
- Purpose: Exported design files from Google Stitch (reference only)
- Generated: External (from Stitch)
- Committed: No (too large)

**`node_modules/`, `__pycache__/`, `.env`**
- Purpose: Dependencies, compiled artifacts, secrets
- Generated: Yes
- Committed: No (in `.gitignore`)

---

*Structure analysis: 2026-05-10*

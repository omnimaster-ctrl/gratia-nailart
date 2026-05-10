# Architecture

**Analysis Date:** 2026-05-10

## Pattern Overview

**Overall:** Monorepo with decoupled frontend SPA and backend REST API

**Key Characteristics:**
- Frontend: React 19 SPA with client-side routing (React Router v7)
- Backend: FastAPI async REST API with multi-tenant support
- Database: MongoDB (Motor async driver) for document storage
- Communication: JSON REST API, CORS enabled
- Deployment: Single Railway app with frontend + backend + database

## Layers

**Presentation Layer:**
- Purpose: User-facing UI for landing page and booking wizard
- Location: `frontend/src/`
- Contains: React components (landing, booking wizard, navigation), CSS (Tailwind + custom theme)
- Depends on: Backend REST API, React Router for navigation
- Used by: Client browsers via HTTPS

**Routing & Navigation Layer:**
- Purpose: Client-side routing and page transitions
- Location: `frontend/src/App.tsx`, `frontend/src/components/`
- Contains: React Router setup (landing `/`, booking `/booking`), component-level route guards
- Depends on: React Router DOM v7
- Used by: App.tsx entry point

**API Layer:**
- Purpose: Expose REST endpoints for booking, appointments, calendar, admin operations
- Location: `backend/server.py` (entry point), `backend/routes/`
- Contains: Route modules (booking, appointments, calendar, reschedule, admin, tenants)
- Depends on: Database layer, external services (MercadoPago, email, WhatsApp, Google Calendar)
- Used by: Frontend SPA, admin dashboard

**Business Logic & Services Layer:**
- Purpose: Core domain logic separated from routing
- Location: `backend/*.py` (services and utilities)
- Key modules:
  - `booking.py`: Appointment booking, payment holds, VIP bypass
  - `calendar_service.py`: Google Calendar event creation and sync
  - `notification_service.py`: In-app notification management
  - `email_service.py`: Resend email service integration
  - `whatsapp_service.py`: WhatsApp confirmation messages
  - `mercadopago_service.py`: Payment preference creation and validation
  - `discount_service.py`: Discount code validation and redemption
  - `scheduling.py`: Business hours, date validation, schedule derivation
  - `phone_utils.py`: Phone number normalization
- Depends on: Database, external service clients
- Used by: Route handlers in `backend/routes/`

**Tenant Management Layer:**
- Purpose: Multi-tenant support for future scalability
- Location: `backend/tenant.py`, `backend/tenant_config.py`
- Contains: Tenant initialization, DEFAULT_TENANT_ID constant
- Depends on: Database layer
- Used by: All route handlers to scope data by tenant

**Data Access Layer:**
- Purpose: MongoDB connection management and shared database instance
- Location: `backend/database.py`
- Contains: Motor async client initialization, db instance
- Configuration: `MONGO_URL` (env: `MONGO_URL`), `MONGO_DB_NAME` (env: `MONGO_DB_NAME`)
- Used by: All services and routes

**External Integrations:**
- MercadoPago: Payment preference creation (`mercadopago_service.py`)
- Google Calendar: Event creation and management (`calendar_service.py`)
- Resend: Email delivery (`email_service.py`)
- WhatsApp: Confirmation messages (`whatsapp_service.py`)

## Data Flow

**Booking Submission Flow:**

1. User fills booking form in `WizardBooking.tsx` component
2. Form submission → POST `/api/booking/create` (or `/api/booking/create-vip`)
3. `booking.py` handler validates appointment data against business rules:
   - Valid date (not past, within business hours)
   - Service name and time slot availability
   - Phone/email normalization
4. Creates "pending" appointment in MongoDB (status: "pending_payment")
5. Creates MercadoPago payment preference via `mercadopago_service.py`
6. Returns preference_id to frontend for redirect to MercadoPago checkout
7. User completes payment on MercadoPago
8. Webhook from MercadoPago → `/api/booking/webhook` (in `booking.py`)
9. Validates webhook HMAC signature
10. Updates appointment status to "confirmed" if payment successful
11. Triggers background tasks:
    - `send_confirmation_email()` → via Resend
    - `send_whatsapp_confirmation()` → WhatsApp Business API
    - `create_google_calendar_event()` → syncs to Hazael's calendar
12. Returns confirmation to client

**Reschedule Flow:**

1. Client accesses reschedule page with email + phone (or token-based)
2. POST `/api/reschedule/verify` → verifies identity
3. Retrieves appointment from MongoDB
4. POST `/api/reschedule/update` → validates new date/time, updates document
5. Triggers notification emails and calendar updates

**Calendar Sync:**

1. GET `/api/calendar/availability` → queries MongoDB for booked slots
2. Derives available time slots based on business hours and appointments
3. Returns available date/time combinations to frontend for booking form

**Admin Operations:**

1. Admin endpoints under `/api/admin/*` (separate router in `routes/admin/`)
2. Handles appointments, clients, blocked dates, notifications, analytics
3. All scoped to tenant via `DEFAULT_TENANT_ID`

## Key Abstractions

**Appointment Model:**
- Purpose: Central booking entity
- Representation: MongoDB document with fields: name, phone, service, date, time, status, payment_id, etc.
- Status enum: "pending_payment" → "confirmed" → "completed" / "cancelled"
- Example: `backend/models.py` defines `AppointmentRequest`

**Service Abstractions:**
- Each external integration wrapped in dedicated service module
- Common pattern: async functions, error handling, logging
- Examples: `mercadopago_service.create_preference()`, `email_service.send_confirmation_email()`

**Scheduling Engine:**
- Purpose: Business hours validation, slot availability, schedule derivation
- Location: `backend/scheduling.py`
- Abstractions: `is_valid_appointment_date()`, `is_business_hours()`, `derive_schedule()`
- Handles: Date range validation, time slot allocation (Mañana/Tarde)

## Entry Points

**Frontend:**
- Location: `frontend/src/main.tsx`
- Triggers: Browser load via Vite dev server or built assets
- Responsibilities: React DOM initialization, root component render

**Backend:**
- Location: `backend/server.py`
- Triggers: Python process startup (Railway container)
- Responsibilities:
  - FastAPI app creation
  - Middleware setup (CORS)
  - Router registration (8 routers)
  - Background task initialization (expiration monitor)
  - Google Calendar credential loading from env

**Admin Setup:**
- Location: `backend/create_admin.py`
- Triggers: Manual invocation
- Responsibilities: Bootstrap initial admin account

## Error Handling

**Strategy:** Async exception handling with HTTP status codes + detailed error messages

**Patterns:**

Frontend:
- Try-catch in async booking submission
- User-facing error toasts for network failures
- Form validation before submission

Backend:
- FastAPI HTTPException for validation errors (400, 422)
- Custom error handling for business logic (e.g., appointment already exists)
- Webhook signature validation prevents unauthorized payment updates
- MongoDB duplicate key errors caught and handled gracefully
- Background task exception logging (expiration monitor continues despite errors)

**Example from `booking.py`:**
```python
try:
    validate_discount(...)
except DiscountValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))
```

## Cross-Cutting Concerns

**Logging:** 
- Print statements to stdout (Railway logs captured)
- Background tasks log status (✅ success, ⚠️ warning)
- Webhook processing logs payment events

**Validation:**
- Pydantic models enforce request shape (`models.py`)
- Business logic validation in handlers (date ranges, phone format)
- Discount code validation with atomic MongoDB operations

**Authentication:**
- Admin routes protected by auth tokens (stored in headers)
- Public routes (booking, landing) have no authentication
- Webhook HMAC signature validation (MercadoPago)
- Reschedule via email/phone verification or token

**Tenant Isolation:**
- All queries implicitly scoped to `DEFAULT_TENANT_ID`
- Tenant info in booking confirmation emails
- Multi-tenant architecture ready for future expansion

---

*Architecture analysis: 2026-05-10*

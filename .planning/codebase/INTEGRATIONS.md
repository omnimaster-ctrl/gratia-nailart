# External Integrations

**Analysis Date:** 2026-05-10

## APIs & External Services

**Payment Processing:**
- MercadoPago - Booking deposit payment ($250 MXN per appointment)
  - SDK: mercadopago 2.2.1
  - Auth: `MP_ACCESS_TOKEN` (env var)
  - Implementation: `backend/mercadopago_service.py` - Creates checkout preferences, processes webhooks
  - Features: Preference creation, payment info retrieval, merchant order lookup
  - Webhook endpoint: `/api/webhooks/mercadopago`

**Email Notifications:**
- Resend - Transactional email service
  - SDK: resend 2.0.0
  - Auth: `RESEND_API_KEY` (env var)
  - Implementation: `backend/email_service.py`
  - Features: Appointment confirmations, cancellations, reschedule notifications, owner notifications
  - Email templates: HTML-formatted emails with appointment details
  - From address: "La Pop Nails <hola@lapopnails.mx>" (configured in code)

**WhatsApp/SMS:**
- Twilio - WhatsApp API for notifications
  - SDK: twilio 8.10.0
  - Auth: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` (env vars)
  - Implementation: `backend/whatsapp_service.py`
  - Features: Appointment confirmations (via approved template), reminders, cancellations, owner notifications
  - WhatsApp template: `HX1782e8fd5d82f07a33ff2ada0f4a0a70` (confirmacion_cita_utility_v4, approved Feb 5 2026)
  - From number: `TWILIO_WHATSAPP_FROM` (Twilio sandbox number)
  - Recipient format: +521 + 10 digits (Mexico mobile standard)

**Calendar Integration:**
- Google Calendar - Syncs appointments to nail artist's calendar
  - SDK: google-api-python-client 2.108.0, google-auth-oauthlib 1.1.0, google-auth-httplib2 0.2.0
  - Auth: Service account (via `GOOGLE_SERVICE_ACCOUNT_JSON` env var, base64 encoded) OR OAuth token (stored in MongoDB)
  - Implementation: `backend/calendar_service.py`
  - Features: Event creation, event deletion, token refresh for OAuth flow
  - Database: OAuth tokens stored in `system_config` collection (MongoDB)
  - Scopes: `https://www.googleapis.com/auth/calendar`

**AI/LLM (Experimental - Future Pro Tier):**
- Groq - LLM inference for booking agent
  - SDK: groq >=0.4.1,<1 and langchain-groq >=0.2.0
  - Auth: Environment variable (not yet fully integrated)

- OpenAI - Fallback LLM provider
  - SDK: openai >=1.0.0
  - Auth: Environment variable (not yet fully integrated)

- Langfuse - LLM observability and monitoring
  - SDK: langfuse >=3.0.0
  - Purpose: Track AI agent interactions and performance metrics

## Data Storage

**Databases:**
- MongoDB (async via Motor)
  - Connection: `MONGO_URL` env var (default: mongodb://localhost:27017)
  - Database name: `MONGO_DB_NAME` env var (default: gratia_nailart_db)
  - Client: motor 3.3.1 (async wrapper around pymongo)
  - Implementation: `backend/database.py` - Single connection pool `db` exported to all modules
  - Collections (inferred):
    - `system_config` - Google Calendar OAuth tokens and system settings
    - Tenant/business data (multi-tenant support)
    - Appointments, clients, bookings
    - Discounts, blocked dates

**File Storage:**
- AWS S3 (future)
  - SDK: boto3 >=1.34.129
  - Purpose: Portfolio images, design uploads
  - Status: Dependency present but not yet wired in code

**Caching:**
- None detected - In-memory session state only

## Authentication & Identity

**Auth Provider:**
- Custom JWT-based authentication
  - Implementation: `backend/auth.py`
  - Token library: pyjwt >=2.10.1, python-jose >=3.3.0
  - Password hashing: passlib >=1.7.4
  - Multi-tenant: Tenants isolated by subdomain/header

**Google OAuth (for Calendar sync):**
- google-auth-oauthlib 1.1.0 - OAuth 2.0 flow
- Tokens refreshed via `google-auth-httplib2`
- Service account option for non-interactive calendar access

## Monitoring & Observability

**Error Tracking:**
- None detected (no Sentry/Rollbar integration)

**Logs:**
- Print statements to stdout
- Uvicorn logs (FastAPI)
- No structured logging framework

**AI Observability (Experimental):**
- Langfuse - Integrated for future AI bot, tracks LLM calls and performance

## CI/CD & Deployment

**Hosting:**
- Railway.app
  - Frontend: Node.js + Vite build + preview server
  - Backend: Python + FastAPI + Uvicorn
  - MongoDB: Railway-hosted MongoDB instance
  - Auto-deploy from `main` branch on GitHub (may not always trigger)
  - Manual redeploy: `railway redeploy --yes`
  - CLI installed: `/opt/homebrew/bin/railway` (logged in as David Tello)

**Production URLs:**
- Frontend: https://gratia-nailart-production.up.railway.app/
- Backend: https://gratia-nailart-backend-production.up.railway.app/ (inferred from code)

**Domain:**
- Pending - Waiting for client to choose (suggested: gratianailart.com)

**CI Pipeline:**
- None detected (no GitHub Actions, Travis, CircleCI)

## Environment Configuration

**Required env vars:**

| Var | Purpose | Example |
|-----|---------|---------|
| `MONGO_URL` | MongoDB connection | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `MONGO_DB_NAME` | Database name | `gratia_nailart_db` |
| `MP_ACCESS_TOKEN` | MercadoPago | `TEST-1234567890...` |
| `RESEND_API_KEY` | Resend email | `re_...` |
| `TWILIO_ACCOUNT_SID` | Twilio account | `ACxxxxxxxxxxxxxxx` |
| `TWILIO_AUTH_TOKEN` | Twilio auth | `xxxxxxxxxxxxxxxx` |
| `TWILIO_WHATSAPP_FROM` | WhatsApp sender | `whatsapp:+1234567890` |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Google Calendar (base64) | base64-encoded service account JSON |
| `GOOGLE_CLIENT_SECRET_JSON` | Google OAuth (base64) | base64-encoded OAuth credentials JSON |
| `POP_NOTIFICATION_EMAIL` | Owner email | `pop@gratianailart.com` |
| `POP_WHATSAPP_PHONE` | Owner WhatsApp | `+5214434910277` |
| `FRONTEND_URL` | Frontend URL | `https://gratia-nailart-production.up.railway.app` |
| `BACKEND_URL` | Backend URL for webhooks | `https://gratia-nailart-backend-production.up.railway.app` |
| `ALLOWED_ORIGINS` | CORS origins (JSON) | `["https://gratianailart.com", "http://localhost:3000"]` |
| `RAILWAY_ENVIRONMENT` | Deployment env | `production` or `development` |

**Secrets location:**
- Railway dashboard (environment variables)
- Not committed to git (`.gitignore` includes `.env*`, `secrets/`)

## Webhooks & Callbacks

**Incoming (Backend webhooks):**
- `/api/webhooks/mercadopago` - MercadoPago payment webhook
  - Triggers: Payment approval, cancellation, pending status updates
  - Implementation: Handled in booking routes or separate webhook handler

**Outgoing (Frontend callbacks):**
- MercadoPago redirect URLs (configured in `backend/mercadopago_service.py`):
  - Success: `{FRONTEND_URL}/payment-success`
  - Failure: `{FRONTEND_URL}/payment-failure`
  - Pending: `{FRONTEND_URL}/payment-pending`

**Google Calendar webhooks:**
- None detected (polling/push notifications not implemented)

## API Documentation

**Frontend API calls:**
- Booking wizard posts to backend via `fetch()` or similar
- No OpenAPI/Swagger UI enabled in code

**Backend API structure:**
- FastAPI auto-generates OpenAPI schema at `/openapi.json` (standard)
- Routes: Admin, tenants, clients, discounts, appointments, booking, reschedule, calendar, internal

---

*Integration audit: 2026-05-10*

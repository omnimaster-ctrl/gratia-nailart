# Technology Stack

**Analysis Date:** 2026-05-10

## Languages

**Primary:**
- TypeScript ~5.9.3 - Frontend (React + React Router)
- Python 3.x - Backend (FastAPI)

**Secondary:**
- JavaScript/JSX - React components in frontend

## Runtime

**Environment:**
- Node.js (frontend)
- Python 3.x (backend)

**Package Manager:**
- npm - Frontend (no lockfile specified, uses standard package.json)
- pip - Backend (requirements.txt)

## Frameworks

**Core:**
- React ^19.2.4 - UI library for booking + landing page
- FastAPI 0.110.1 - Backend API server
- Uvicorn 0.25.0 - ASGI server for FastAPI

**Routing:**
- react-router-dom ^7.14.0 - Client-side routing for landing + booking wizard

**Build/Dev:**
- Vite 8.0.1 - Frontend bundler and dev server
- Tailwind CSS 4.2.2 - Utility-first CSS framework for styling
- @tailwindcss/vite 4.2.2 - Vite plugin for Tailwind
- TypeScript + @vitejs/plugin-react 6.0.1 - React + TS support in Vite

## Key Dependencies

**Critical:**
- motor 3.3.1 - Async MongoDB driver (PyMongo async wrapper)
- pymongo 4.5.0 - MongoDB client library (used by Motor)
- pydantic >=2.6.4 - Data validation and settings management
- luxon ^3.7.2 - Date/time library for JavaScript (frontend)
- pytz / tzdata - Timezone support (backend)

**Infrastructure & Async:**
- python-multipart 0.0.9 - Parse multipart/form-data in FastAPI

**Validation & Security:**
- email-validator >=2.2.0 - Email validation
- cryptography >=42.0.8 - Cryptographic operations
- passlib >=1.7.4 - Password hashing
- pyjwt >=2.10.1 - JWT token generation/validation
- python-jose >=3.3.0 - JOSE (JSON Object Signing/Encryption) implementation

**Environment & Config:**
- python-dotenv >=1.0.1 - Load .env files

**Testing & Code Quality:**
- pytest >=8.0.0 - Testing framework (backend)
- black >=24.1.1 - Code formatter
- isort >=5.13.2 - Import sorter
- flake8 >=7.0.0 - Linter
- mypy >=1.8.0 - Static type checker
- ESLint ^9.39.4 - Frontend linting (@eslint/js, typescript-eslint, eslint-plugin-react-hooks)

**CLI & Utilities:**
- typer >=0.9.0 - CLI framework for Python
- requests >=2.31.0 - HTTP client
- requests-oauthlib >=2.0.0 - OAuth support for Google Calendar integration

## Integration SDKs

**Payment Processing:**
- mercadopago 2.2.1 - MercadoPago payment SDK

**Communications:**
- twilio 8.10.0 - WhatsApp messages (Twilio API)
- resend 2.0.0 - Email service (Resend API)

**Calendar & Auth:**
- google-api-python-client 2.108.0 - Google Calendar API
- google-auth-httplib2 0.2.0 - HTTP authentication for Google APIs
- google-auth-oauthlib 1.1.0 - OAuth 2.0 flow for Google

**Cloud Storage:**
- boto3 >=1.34.129 - AWS SDK (S3 for file uploads, future use)

**Web Push (Experimental):**
- pywebpush >=2.0.0 - Web push notifications

**AI & LLM (Experimental):**
- langchain-core >=0.3.0 - LangChain core framework
- langgraph >=0.2.0 - LangGraph for agent workflows
- langchain-groq >=0.2.0 - Groq LLM integration
- groq >=0.4.1,<1 - Groq API client
- openai >=1.0.0 - OpenAI API (for future AI bot tier)
- langfuse >=3.0.0 - LLM observability/monitoring

## Configuration

**Environment:**
- `.env` file (local development) - Contains API keys and database credentials
- Environment variables on Railway - Secrets managed via Railway dashboard
- `MONGO_URL` - MongoDB connection string (default: mongodb://localhost:27017)
- `MONGO_DB_NAME` - Database name (default: gratia_nailart_db)
- `MP_ACCESS_TOKEN` - MercadoPago API token
- `RESEND_API_KEY` - Resend email service key
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` - Twilio WhatsApp credentials
- `TWILIO_WHATSAPP_FROM` - WhatsApp sender number (Twilio sandbox)
- `GOOGLE_SERVICE_ACCOUNT_JSON` - Google Calendar service account (base64 encoded)
- `GOOGLE_CLIENT_SECRET_JSON` - Google OAuth credentials (base64 encoded)
- `POP_NOTIFICATION_EMAIL` - Owner email for appointment notifications
- `POP_WHATSAPP_PHONE` - Owner WhatsApp number for notifications
- `ALLOWED_ORIGINS` - CORS origins (JSON array, includes localhost in dev)
- `FRONTEND_URL` - Frontend URL for email links
- `BACKEND_URL` - Backend URL for webhooks
- `RAILWAY_ENVIRONMENT` - Environment flag (production/staging)

**Build:**
- Frontend: `frontend/vite.config.ts` - Vite configuration (React + Tailwind)
- Frontend: `frontend/tsconfig.json` & `frontend/tsconfig.app.json` - TypeScript configuration
- Frontend: `frontend/eslint.config.js` - ESLint rules
- Backend: No explicit build config (FastAPI runs directly)

**Development:**
- Frontend: Vite dev server (hot reload)
- Backend: Uvicorn dev server with FastAPI auto-reload

## Database

**MongoDB (via Motor async driver):**
- Collections (inferred from code):
  - `system_config` - System-level configuration (e.g., Google Calendar tokens)
  - Appointments, clients, bookings (multi-tenant design)
- Connection pool: `motor.motor_asyncio.AsyncIOMotorClient`
- Async-first design with Motor for non-blocking I/O

## Platform Requirements

**Development:**
- Node.js 18+ (for npm)
- Python 3.8+ (for FastAPI)
- MongoDB instance (local or remote)

**Production:**
- Deployment: Railway.app
- Frontend: Node.js runtime on Railway (Vite build + preview server)
- Backend: Python runtime on Railway (FastAPI + Uvicorn)
- Database: MongoDB (Railway-hosted or external)
- Domain: Pending (suggested: gratianailart.com)

**Infra Costs (~$15-20 USD/month):**
- Railway frontend: ~$5
- Railway backend (FastAPI): ~$5-10
- Railway MongoDB: ~$5
- Resend email: Free tier
- Domain: ~$1 (amortized)

---

*Stack analysis: 2026-05-10*

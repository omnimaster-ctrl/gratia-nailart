# Codebase Concerns

**Analysis Date:** 2026-05-10

## Security Vulnerabilities

**Previous Secrets Leak (RESOLVED):**
- Issue: Client secret and OAuth token pickle file were committed to repo
- Files affected: `backend/client_secret.json`, `backend/token.pickle`
- Impact: Exposed Google Calendar OAuth credentials publicly
- Current status: Removed in commits 1b84666 and 94abf5a; `.gitignore` now prevents re-occurrence
- Resolution: Secrets now stored as environment variables (base64-encoded in Railway)
- **Remaining Risk:** Ensure no additional credential files remain in git history

**Placeholder Tokens in Environment:**
- Issue: Multiple service integrations have placeholder/dummy tokens in code examples and docs
- Files: `backend/mercadopago_service.py`, `backend/whatsapp_service.py`, `backend/calendar_service.py`
- Impact: If anyone uses these placeholders without real credentials, services will silently fail
- Recommendation: Create `.env.example` file with clearly marked placeholder values and documentation

**Google Credentials Handling:**
- Issue: Base64-encoded credentials decoded at startup and written to filesystem (`/app/backend/client_secret.json`)
- Location: `backend/server.py` lines 17-26
- Risk: File created in container filesystem; if service account JSON is too long or decoding fails, silent failure occurs
- Mitigation: Error handling in place but minimal logging
- Better approach: Use the base64 directly without writing to disk, or validate before write

**Hardcoded Email/Phone in Notifications:**
- Files: `backend/calendar_service.py` (lines 159, 259), `backend/whatsapp_service.py` (line 309)
- Issue: Fallback email `lapopnails.28@gmail.com` hardcoded; Pop's personal phone hardcoded
- Impact: Multi-tenant system hardcodes single email/phone address for one business
- Fix approach: Move to `tenant_config.py` or environment variables

---

## Technical Debt

**Returning Client Lookup Not Wired in Frontend:**
- Issue: Backend endpoint exists (`GET /api/client/lookup/{phone}`) but frontend never calls it
- Files: `backend/routes/clients.py` (implemented), `frontend/src/components/WizardBooking.tsx` (missing call)
- Impact: Step 1 can detect returning client but doesn't auto-populate; only works if user manually checks "soy cliente"
- Priority: High — impacts UX for ~10% of bookings
- Fix: Add fetch call in `WizardBooking.tsx` after phone input blur

**Placeholder Gallery Images:**
- Issue: Gallery uses placeholder filenames instead of real Gratia nail art photos
- Files: `frontend/src/components/Gallery.tsx` lines 3-12 (pink-gems.png, quilted-stars.png, etc.)
- Impact: Landing page shows generic placeholder images; needs Hazael's actual portfolio photos
- Blocker: Awaiting real images from client
- Tasks: `tasks/todo.md` line 31 — marked incomplete

**Railway Auto-Deploy Unreliable:**
- Issue: Auto-deploy from GitHub `main` branch frequently fails to trigger
- Impact: Manual fallback required: `railway up` from frontend/backend directories
- Cause: Root directory config may not be properly propagated in Railway dashboard
- Workaround documented in `tasks/todo.md` line 23
- Fix approach: Verify Railway project settings via dashboard or use Railway CLI to set root directories explicitly

**Missing .env.example in Backend:**
- Issue: No example environment file to guide new developers
- Files: `backend/.env` exists but is .gitignored; no .example version
- Impact: Unclear which env vars are required vs optional
- Recommendation: Create `backend/.env.example` with all keys and helpful comments

---

## Integration Status — Blockers for Launch

**MercadoPago OAuth:**
- Status: Not authorized by client
- Issue: Need Hazael to authorize Omnifractal's MercadoPago app
- Impact: Deposit payments will fail; booking can't complete
- Files: `backend/mercadopago_service.py`, `frontend/src/components/WizardBooking.tsx` line 71
- Required action: Send OAuth authorization link to Hazael, wait for callback

**Google Calendar Sync:**
- Status: Service account method configured; OAuth fallback in place
- Issue: Requires either:
  - Service account JSON (provided via `GOOGLE_SERVICE_ACCOUNT_JSON` env var), OR
  - OAuth token (stored in MongoDB after client authorizes)
- Files: `backend/calendar_service.py` lines 21-70 (token loading logic)
- Current behavior: If no credentials, event details are stored in DB pending OAuth (lines 187-196)
- Risk: Events won't sync to calendar until credentials available
- Workaround: Service account approach bypasses OAuth entirely if set up

**WhatsApp Notifications:**
- Status: Twilio SDK integrated; templates approved (Feb 5 2026)
- Blocking issue: Need Twilio account setup and Gratia's WhatsApp Business number enrolled
- Files: `backend/whatsapp_service.py` (fully implemented)
- Current: If `TWILIO_ACCOUNT_SID` not set, silently skips sending (line 56-57)
- Impact: Booking confirmations won't be sent; users won't know appointments succeeded
- Required action: Set up Twilio Business account, configure env vars, test with production number

**Custom Domain:**
- Status: Pending — awaiting Hazael to choose and register
- Suggested: gratianailart.com, gratianails.mx
- Impact: No SSL/HTTPS until domain connected and configured in Railway
- Tasks: `tasks/todo.md` line 38 — incomplete

---

## Known Bugs & Fragile Areas

**Date/Time Picker Timezone Logic:**
- Issue: Calendar operations assume Mexico City timezone (America/Mexico_City)
- Files: `backend/calendar_service.py` lines 146, 151, 233, 235; `backend/scheduling.py`
- Risk: If deployment moves to different timezone or client location changes, dates will be off
- Safe modification: All timezone references should use tenant config, not hardcoded

**Email Service Legacy Code:**
- Files: `backend/email_service.py` (40KB — largest file in project)
- Issue: Ported from La Pop Nails; contains old references to Pop Nails and legacy logic
- Risk: Email templates mention "La Pop Nails" instead of "Gratia Nail Art"
- Action needed: Search-and-replace email content to match Gratia brand
- Search patterns: "La Pop Nails", "La Pop", "PopNails", "@___lapopnails", "Pop" (business owner name)

**Hardcoded Business Names in Multiple Places:**
- Files affected:
  - `backend/whatsapp_service.py` line 295: "La Pop Nails" message
  - `backend/mercadopago_service.py` line 83: "LA POP NAILS" statement descriptor
  - `backend/calendar_service.py` lines 122, 209: "La Pop Nails" event title
  - `backend/email_service.py`: Multiple references throughout
- Impact: Notifications and confirmations show wrong business name
- Priority: High — affects customer experience
- Fix approach: Move to tenant config or environment variables

**Phone Normalization Edge Cases:**
- Files: `backend/phone_utils.py`, `backend/whatsapp_service.py` lines 62-104
- Issue: Complex regex logic for Mexico +521 format; multiple fallback branches
- Risk: Border cases (alternate area codes, international numbers) may format incorrectly
- Coverage: Limited test coverage for edge cases
- Recommendation: Add unit tests for phone formatting

---

## Missing Critical Features

**No Admin Dashboard Implemented:**
- Issue: Booking backend routes exist but no admin UI to view/manage appointments
- Files: `backend/routes/admin/` directory exists but sparse
- Impact: Business owner (Hazael) can't view appointments, reschedule, or mark completions
- Priority: High — needed for launch
- Scope: Requires admin login flow, appointment list, calendar view, rescheduling UI

**No Availability Management UI:**
- Issue: Availability is hardcoded in `backend/scheduling.py` (fixed hours: 10AM-7PM, blocks per day)
- Files: `backend/scheduling.py` (AM_BLOCK, PM_BLOCK, SAT_BLOCK constants)
- Impact: If Hazael wants to change hours or take vacation, code must be updated
- Required: Admin interface to set working hours, blocked dates, per-day capacity
- Blocker: Can't launch without this

**No Payment Webhook Verification:**
- Issue: MercadoPago webhook endpoint exists but signature verification may be incomplete
- Files: `backend/routes/booking.py` (webhook handling)
- Risk: Malformed webhooks could create duplicate appointments or miss confirmations
- Recommendation: Add HMAC signature verification for all webhooks

---

## Performance & Scaling Concerns

**In-Memory Calendar Event Details Storage:**
- Issue: Calendar events pending OAuth are stored in MongoDB but queried on every booking
- Files: `backend/calendar_service.py` lines 187-195
- Risk: Not a bottleneck now but could accumulate if OAuth authorization is delayed
- Recommendation: Add TTL index or periodic cleanup

**No Caching on Availability Queries:**
- Issue: `GET /api/available-dates` and `GET /api/available-times/{date}` query database every time
- Files: Frontend calls at lines 27-30, 37-39 in `frontend/src/components/WizardBooking.tsx`
- Impact: 2 network requests per form interaction; no client-side caching
- Fix: Add HTTP caching headers or implement client-side SWR/React Query

**Gallery Auto-Scroll Performance:**
- Files: `frontend/src/components/Gallery.tsx` lines 27-57
- Issue: Uses `requestAnimationFrame` for infinite scroll with duplicate items
- Risk: Minor — desktop/tablet only concern, works fine on modern browsers
- No action required — performant enough for current scope

---

## Testing Gaps

**No Automated Tests:**
- Issue: Zero test files in `src/` or `backend/` directories (zod tests in node_modules don't count)
- Impact: Booking flow, payment integration, calendar sync untested
- Priority: High — especially for payment workflows and availability logic
- Recommendation: Start with Jest/Vitest for frontend, pytest for backend

**Manually Tested Features:**
- Google Calendar: Needs to be tested end-to-end after service account setup
- WhatsApp: Manual testing only; template approval process is slow
- MercadoPago: Sandbox mode testing not documented
- Phone lookup: Backend implemented but frontend integration not verified

---

## Accessibility & Mobile Concerns

**Form Accessibility:**
- Files: `frontend/src/components/WizardBooking.tsx`
- Issue: Heavy use of `className` with conditional styling; limited semantic HTML
- Gap: No ARIA labels for complex form sections (clinical form, dates, times)
- Recommendation: Add `aria-label`, `aria-describedby` to inputs

**Mobile Date Picker:**
- Issue: Custom date picker in booking wizard may not work well on older iOS
- Files: `frontend/src/components/WizardBooking.tsx` (custom input, not `<input type="date">`)
- Recommendation: Use native date input on mobile, custom picker on desktop

**Responsive Images in Gallery:**
- Files: `frontend/src/components/Gallery.tsx`
- Issue: Images are 220px-270px width; no `srcset` or lazy loading
- Impact: Mobile users load full-res images unnecessarily
- Fix: Add `loading="lazy"` and `srcset` for different breakpoints

---

## Deployment & Operations

**No Health Check Endpoint:**
- Issue: No way to verify backend is alive without calling an API route
- Recommendation: Add `GET /health` endpoint for monitoring

**No Structured Logging:**
- Issue: All logs are `print()` statements; no structured logging (JSON, log levels, timestamps)
- Files: Throughout backend (calendar_service.py, whatsapp_service.py, etc.)
- Impact: Hard to search logs in Railway dashboard, difficult to debug
- Recommendation: Use Python `logging` module with JSON formatter

**Missing Railway Configuration Documentation:**
- Issue: Root directory config, environment variables not explicitly documented
- Files: Railway setup described only in `tasks/todo.md`
- Recommendation: Create `DEPLOYMENT.md` with Railway-specific setup steps

---

## Deployment Blocking Issues Summary

| Issue | Priority | Status | Blocker? |
|-------|----------|--------|----------|
| MercadoPago OAuth | HIGH | Awaiting client | **YES** |
| Twilio/WhatsApp setup | HIGH | Awaiting account | **YES** |
| Custom domain registration | MEDIUM | Awaiting client | Optional but needed for SSL |
| Admin dashboard | HIGH | Not implemented | **YES** — no way to manage bookings |
| Gallery placeholder images | MEDIUM | Awaiting client | Cosmetic but important |
| Returning client lookup wiring | MEDIUM | Incomplete | Minor UX gap |
| Availability management UI | HIGH | Not implemented | **YES** — can't adjust hours |
| .env.example | LOW | Missing | Documentation only |

---

*Concerns audit: 2026-05-10*

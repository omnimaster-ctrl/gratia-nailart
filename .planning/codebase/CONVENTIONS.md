# Coding Conventions

**Analysis Date:** 2026-05-10

## Naming Patterns

**Files:**
- React components: PascalCase (e.g., `Nav.tsx`, `WizardBooking.tsx`, `Gallery.tsx`)
- Utility/service files: camelCase (e.g., `bookingLogic.ts`, `email_service.py`, `calendar_service.py`)
- Type/model files: camelCase or descriptive (e.g., `models.py` for Pydantic schemas)
- Python modules follow snake_case (e.g., `mercadopago_service.py`, `phone_utils.py`, `discount_service.py`)

**Functions:**
- React components: PascalCase (exported as default: `export default function Nav() {}`)
- TypeScript/JavaScript functions: camelCase (e.g., `validateStep()`, `buildTimeSlots()`, `minSelectableDateMX()`)
- Python functions: snake_case (e.g., `create_booking_hold()`, `validate_discount()`, `send_whatsapp_confirmation()`)
- Async functions: same naming, async keyword precedes: `async def validate_discount(...)`

**Variables:**
- TypeScript: camelCase (e.g., `form`, `errors`, `bookedTimes`, `fullyCashedDates`)
- Python: snake_case (e.g., `discount_doc`, `existing_hold`, `hold_expired`)
- Constants: UPPER_SNAKE_CASE (e.g., `DEPOSIT_MXN`, `HOLD_DURATION_MINUTES`, `AM_BLOCK`, `TZ`)
- React state: camelCase with `set` prefix for setState (e.g., `const [step, setStep] = useState(1)`)

**Types:**
- TypeScript interfaces/types: PascalCase (e.g., `FormData`, `PaymentRequest`, `AppointmentRequest`)
- Python Pydantic models: PascalCase (e.g., `AppointmentRequest`, `DiscountConstraint`, `LoginResponse`)
- Enum-like objects: camelCase keys (e.g., `services = { 'Técnica Mixta': {...} }`)

**Spanish in Code:**
- User-facing strings (labels, messages, placeholders, error messages): Spanish only (e.g., "Tus datos", "Agenda tu cita", "Email *")
- Component names and function names: English only (e.g., `WizardBooking`, `validateStep()`)
- Variable/field names in form objects: camelCase English (e.g., `appointmentDate`, `serviceType`, `retiroMaterial`)
- Database field names: snake_case English (e.g., `appointment_date`, `service_type`, `retiro_material`)

## Code Style

**Formatting:**
- TypeScript: 2-space indentation (Vite default)
- Python: 4-space indentation (PEP 8)
- No trailing semicolons in TypeScript (modern JS/TS convention)
- Line breaks organized by feature blocks with `// ── Comment ──` style separators

**Linting:**
- ESLint v9 with TypeScript support (`@eslint/js`, `typescript-eslint`)
- React Hooks rules enforced (`eslint-plugin-react-hooks`)
- React Refresh rules enforced (`eslint-plugin-react-refresh`)
- No custom Prettier config; uses ESLint for formatting
- Python: No linting config detected; follows PEP 8 implicitly

**Tailwind CSS:**
- CSS-in-class model via Tailwind utility classes in JSX
- No CSS modules or styled-components
- Design tokens defined in `index.css` as Tailwind theme variables (e.g., `--color-gold: #cda255`)
- Custom keyframes for animations (`float`, `float-slow`, `sparkle`) in `index.css`
- Responsive design with `md:` breakpoints (mobile-first)

## Import Organization

**Order (TypeScript/React):**
1. React/Next/Framework imports (`import { useState } from 'react'`)
2. Router/Navigation imports (`import { BrowserRouter } from 'react-router-dom'`)
3. Type imports (`import { type FormData }`)
4. Local component imports (relative paths)
5. Utility/service imports (`import { validateStep, services } from './booking/bookingLogic'`)
6. Environment variables (`const API = import.meta.env.VITE_BACKEND_URL || ...`)

Example from `WizardBooking.tsx`:
```typescript
import { useState, useEffect, useCallback } from 'react'
import { type FormData, initialFormData, validateStep, services, ... } from './booking/bookingLogic'

const API = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
```

**Order (Python):**
1. Standard library imports
2. Third-party imports (FastAPI, Motor, Pydantic, etc.)
3. Local imports (database, models, services)

Example from `routes/booking.py`:
```python
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks

from database import db
from models import PaymentRequest
```

**Path Aliases:**
- No path aliases configured in `tsconfig.json` or `vite.config.ts`
- All imports use relative paths (e.g., `'./booking/bookingLogic'`, `'./components/Nav'`)

## Error Handling

**TypeScript/React:**
- Async operations wrapped in `try/catch` blocks
- Errors collected in state object (`errors: Record<string, string>`)
- UI displays errors via conditional rendering: `{errors.name && <span className={errMsg}>{errors.name}</span>}`
- Failed API calls show user-friendly alerts: `alert('Error de conexión.')`
- Network failures caught silently with `.catch(() => {})` for non-critical endpoints

Pattern from `WizardBooking.tsx`:
```typescript
const handlePayment = async () => {
  const e = validateStep(5, form)
  setErrors(e)
  if (Object.keys(e).length > 0) return
  try {
    const res = await fetch(...)
    if (res.ok && data.checkout_url) { ... }
    else { alert(`Error: ${data.detail || 'Intenta de nuevo'}`) }
  } catch { alert('Error de conexión.') }
}
```

**Python/FastAPI:**
- Validation via Pydantic models (automatic 422 responses on failure)
- Business logic errors raised as `HTTPException` with appropriate status codes
- Database queries wrapped in try/except for `DuplicateKeyError`, etc.
- Background task errors logged to console with emoji prefixes (e.g., `❌`, `⚠️`, `✅`)
- Async context managers for database connections

Pattern from `routes/booking.py`:
```python
try:
    data = await request.json()
    date = data.get("date")
    if not date:
        raise HTTPException(status_code=400, detail="Date required")
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
```

## Logging

**Framework:** Console logging (no dedicated logging library)

**Patterns:**
- TypeScript: Conditional logs for debugging, no production logging framework
- Python: `print()` statements with emoji prefixes for status indication:
  - `✅` = Success
  - `⚠️` = Warning
  - `❌` = Error
  - `🛡️` = System processes (background tasks)

Examples from `server.py`:
```python
print("✅ Google Calendar credentials configured from environment")
print(f"⚠️ Failed to configure Google Calendar credentials: {e}")
print("🛡️ Starting Expiration Monitor background task...")
```

## Comments

**When to Comment:**
- Function docstrings: Used for async functions explaining purpose and parameters
- Inline comments: Minimal; code is self-documenting
- Section separators: `// ── Label ──` for organizing large components
- MDN-style docstrings in Python modules (e.g., `"""Pydantic models for API requests."""`)

**JSDoc/TSDoc:**
- TypeScript: Not widely used; types are inferred from Pydantic models
- Python: Module-level docstrings present (e.g., `"""Booking creation, holds, payments..."""`)
- No formal type hints in docstrings; Pydantic models serve as documentation

## Function Design

**Size:**
- React components: Typically 50–300 lines (large wizard components exceed this)
- TypeScript functions: Short utility functions (10–30 lines); complex logic in separate service files
- Python functions: 20–60 lines; longer functions include internal comments

**Parameters:**
- React: Props passed as single object (destructured in component signature)
- TypeScript: Explicit parameter lists; no heavy destructuring in function signatures
- Python: Type hints required via Pydantic models or Python type annotations

**Return Values:**
- React components: JSX elements (implicit return or explicit `return (...)`)
- TypeScript utilities: Typed return values (e.g., `Record<string, string>` for error objects)
- Python async functions: JSON-serializable Pydantic models or FastAPI responses

Example from `bookingLogic.ts`:
```typescript
export const validateAppointmentDate = (date: string) => {
  if (!date || !isBusinessDayMX(date)) return false
  const sel = DateTime.fromISO(date, { zone: TZ }).startOf('day')
  const min = DateTime.fromISO(minSelectableDateMX(), { zone: TZ }).startOf('day')
  // ... validation logic
  return true
}
```

## Module Design

**Exports:**
- React components: Default export (`export default function Component() {}`)
- Utility modules: Named exports for individual functions/constants
- Barrel files: Not used; imports are direct from individual modules

**Barrel Files:**
- `src/components/` has no `index.ts`; imports are explicit (e.g., `import Nav from './components/Nav'`)
- `routes/` directory has no barrel; each route imports its dependencies directly

**State Management:**
- React: Local component state via `useState()` and `useEffect()`
- Persistence: `localStorage` for form data (e.g., `localStorage.setItem('gratia_wizard', JSON.stringify(form))`)
- Backend state: MongoDB via Motor async driver
- No Redux, Context API, or Zustand; state is co-located with UI

## API Communication

**Base URL:**
- Environment variable: `VITE_BACKEND_URL` (TypeScript)
- Default fallback: `'http://localhost:8000'`
- Production: `'https://gratia-nailart-production.up.railway.app'`

**Request/Response:**
- HTTP method: explicit (e.g., `fetch(..., { method: 'POST' })`)
- Content-Type: `'application/json'` for POST/PUT requests
- Error handling: Check `res.ok` before parsing JSON

Pattern from `WizardBooking.tsx`:
```typescript
const res = await fetch(`${API}/api/create-mercadopago-preference`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ appointment_data: {...}, customer_email: form.email }),
})
const data = await res.json()
if (res.ok && data.checkout_url) { ... }
```

---

*Convention analysis: 2026-05-10*

# Testing Patterns

**Analysis Date:** 2026-05-10

## Test Framework

**Status:** No tests detected. Repository contains zero test files.

**Runner:**
- Not applicable (no test framework installed)
- `package.json` does not include Jest, Vitest, Mocha, or similar
- Backend `requirements.txt` does not include pytest or unittest

**Assertion Library:**
- Not applicable

**Run Commands:**
- No test command in `package.json` scripts
- No test infrastructure present

## Test File Organization

**Current State:**
```
gratia-nailart/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json (no test scripts)
└── backend/
    ├── routes/
    ├── models.py
    ├── server.py
    └── requirements.txt (no pytest)
```

**No test directories present:**
- No `__tests__/` directory
- No `tests/` directory
- No `spec/` directory
- No `*.test.ts`, `*.test.tsx`, `*.spec.ts`, or `*.spec.tsx` files
- No Python test files

## Test Structure

**What would belong tested:**
- API endpoints (FastAPI routes): `routes/booking.py`, `routes/admin.py`, `routes/appointments.py`
- Business logic (utilities): `bookingLogic.ts`, `discount_service.py`, `calendar_service.py`
- React components: `WizardBooking.tsx`, `Nav.tsx`, `Gallery.tsx`
- Form validation: `validateStep()` in `bookingLogic.ts`
- Payment integration: `mercadopago_service.py`

**Recommended structure if testing were added:**

TypeScript (Frontend):
```
frontend/
├── src/
│   ├── components/
│   │   ├── Nav.tsx
│   │   ├── Nav.test.tsx          ← Colocated with component
│   │   ├── WizardBooking.tsx
│   │   └── WizardBooking.test.tsx
│   ├── components/booking/
│   │   ├── bookingLogic.ts
│   │   └── bookingLogic.test.ts  ← Colocated with logic
│   └── __tests__/                ← Integration tests
│       ├── booking.integration.test.ts
│       └── api.integration.test.ts
└── vitest.config.ts              ← Would be needed
```

Python (Backend):
```
backend/
├── routes/
│   ├── booking.py
│   └── tests/
│       └── test_booking.py       ← Separate test directory
├── discount_service.py
├── tests/
│   ├── test_discount_service.py
│   ├── test_calendar_service.py
│   └── conftest.py               ← Shared fixtures
└── pytest.ini                      ← Would be needed
```

## Mocking

**Current Practice:**
- No mocking framework detected (no `jest.mock`, `unittest.mock`, `pytest-mock`)
- Actual network calls made in components (e.g., `fetch()` calls to `${API}/api/...`)
- No test doubles or stubs in production code

**External Dependencies Not Mocked:**
- API calls: Real HTTP requests to backend (e.g., `/api/available-dates`, `/api/create-mercadopago-preference`)
- Google Calendar: Actual credentials loaded from environment (`client_secret.json`)
- MercadoPago: Real preference creation (not intercepted)
- WhatsApp/Email: Actual messages sent (no mock service)
- MongoDB: Real database queries (no test database isolation)

## Fixtures and Factories

**Status:** No test fixtures or data factories present.

**What would be needed:**

TypeScript fixtures (if testing were added):
```typescript
// frontend/src/__tests__/fixtures/formData.ts
export const mockFormData: FormData = {
  name: 'Test User',
  email: 'test@example.com',
  phone: '5551234567',
  serviceType: 'Técnica Mixta',
  appointmentDate: '2026-05-20',
  appointmentTime: '09:30',
  // ... other fields
}

export const mockServices = {
  'Técnica Mixta': {
    name: 'Técnica Mixta',
    price: 500,
    duration: 180,
    duration_range: '3h',
    description: '...'
  }
}
```

Python fixtures (if testing were added):
```python
# backend/tests/conftest.py
import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

@pytest.fixture
async def db():
    """Provide test database connection."""
    # Connect to test MongoDB
    # Yield for test
    # Cleanup after test

@pytest.fixture
def appointment_data():
    """Sample appointment request."""
    return {
        'name': 'Test Client',
        'phone': '+5215551234567',
        'service': 'Técnica Mixta',
        'date': '2026-05-20',
        'time': '09:30',
        'appointmentDate': '2026-05-20'
    }
```

## Coverage

**Requirements:** None enforced (no CI/CD test stage detected)

**View Coverage:** N/A (no coverage tools installed)

## Test Types

### Unit Tests (Not Implemented)

**Scope:** Individual functions and components

TypeScript unit test targets:
- `bookingLogic.ts`: `validateStep()`, `buildTimeSlots()`, `minSelectableDateMX()`, `isWeekendMX()`, etc.
- Form validation functions
- Date/time utilities

Python unit test targets:
- `discount_service.py`: `validate_discount()`, `redeem_discount_atomic()`
- `phone_utils.py`: `normalize_phone()`
- `scheduling.py`: `is_valid_appointment_date()`, `derive_schedule()`

### Integration Tests (Not Implemented)

**Scope:** API endpoints, database interactions, external service calls

Python integration test targets:
- `POST /api/booking/hold`: Create booking hold, validate date/time
- `POST /api/create-mercadopago-preference`: Payment flow
- `GET /api/available-dates`: Fetch available dates from calendar
- `POST /api/validate-coupon`: Discount validation with database

TypeScript integration test targets:
- Booking wizard form submission flow
- API communication with backend
- Form persistence via localStorage

### E2E Tests (Not Implemented)

**Framework:** Not used (no Playwright, Cypress, or WebDriver)

**Would test:**
- Complete booking flow: Fill form → Validate → Pay
- Admin dashboard workflows
- Authentication flows

## Common Patterns (If Tests Were Added)

### Async Testing Pattern (TypeScript)

```typescript
// Using Vitest (recommended for Vite projects)
import { describe, it, expect } from 'vitest'
import { validateStep, buildTimeSlots, minSelectableDateMX } from './bookingLogic'

describe('bookingLogic', () => {
  it('should calculate next selectable date (24h minimum)', () => {
    const min = minSelectableDateMX()
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    expect(new Date(min) >= tomorrow).toBe(true)
  })

  it('should validate appointment date', () => {
    // Returns false for weekends, past dates
    expect(validateAppointmentDate('2026-05-10')).toBe(false) // Today (insufficient advance)
    expect(validateAppointmentDate('2026-05-18')).toBe(true)  // Sunday (weekend)
  })

  it('should build time slots for a given date', () => {
    const slots = buildTimeSlots('2026-05-20')
    expect(slots.morning.length).toBeGreaterThan(0)
    expect(slots.morning[0]).toHaveProperty('value', 'display')
  })
})
```

### Async Testing Pattern (Python)

```python
# Using pytest-asyncio
import pytest
from httpx import AsyncClient
from app import app

@pytest.mark.asyncio
async def test_create_booking_hold():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/booking/hold",
            json={
                "date": "2026-05-20",
                "phone": "5551234567",
                "time": "09:30"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "hold_id" in data
        assert "expires_at" in data

@pytest.mark.asyncio
async def test_validate_coupon_invalid_code(db):
    response = await client.post(
        "/api/validate-coupon",
        json={
            "coupon_code": "INVALID",
            "service_type": "Técnica Mixta",
            "service_price": 500
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert "invalid" in data.get("message", "").lower()
```

### Mocking Pattern (If Implemented)

TypeScript (would use Vitest mocking):
```typescript
import { vi } from 'vitest'

vi.stubGlobal('fetch', vi.fn((url) => {
  if (url.includes('available-dates')) {
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve({
        available_dates: [
          { date: '2026-05-20', is_available: true }
        ]
      })
    })
  }
  return Promise.reject(new Error('Not mocked'))
}))
```

Python (would use pytest-mock or unittest.mock):
```python
@pytest.mark.asyncio
async def test_booking_with_mocked_email(mocker):
    mock_send = mocker.patch(
        'email_service.send_confirmation_email',
        return_value=True
    )
    # Create booking
    await create_appointment(...)
    # Assert email was called
    mock_send.assert_called_once()
```

## Test Coverage Gaps

**Critical untested areas:**
- Payment integration (MercadoPago preference creation)
- Calendar service (Google Calendar events)
- Email/WhatsApp notifications
- Booking hold expiration logic
- Discount code validation and redemption
- Authentication flows (admin login)
- Database constraints (duplicate bookings, date/time conflicts)

**Risk:** Bugs in payment, calendar, or notification flows can break production bookings without detection.

---

*Testing analysis: 2026-05-10*

"""
Canonical phone normalization for La Pop Nails.

All modules must use this function to normalize phone numbers.
The canonical format is raw 10-digit Mexican mobile (e.g., "5512345678").
"""


def normalize_phone(raw: str) -> str:
    """
    Normalize a phone string to its canonical 10-digit Mexican format.

    Handles inputs like:
      "+52 55 1234 5678" → "5512345678"
      "15512345678"      → "5512345678"  (strips leading US '1')
      "525512345678"     → "5512345678"
      "5512345678"       → "5512345678"
      ""                 → ""

    Returns empty string if input has fewer than 10 digits.
    """
    if not raw:
        return ""

    digits = "".join(filter(str.isdigit, str(raw)))

    if len(digits) < 10:
        return ""

    return digits[-10:]

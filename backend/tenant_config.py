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
    slug = os.environ.get("DEFAULT_TENANT_SLUG", "gratianailart")

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

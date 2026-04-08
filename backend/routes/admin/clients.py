"""
Admin client directory — list, update, delete clients with phone/name deduplication.
"""

from datetime import datetime, date, timezone
from typing import Optional
from collections import Counter
from fastapi import APIRouter, Depends, HTTPException, status

from database import db
from auth import get_current_admin
from tenant import DEFAULT_TENANT_ID
from models import UpdateClientRequest
from phone_utils import normalize_phone

router = APIRouter(tags=["admin-clients"])


# =============================================================================
# HELPERS (only used by this module)
# =============================================================================


def normalize_name(name: str) -> str:
    """Normalize name for better comparison."""
    if not name:
        return ""
    normalized = name.strip().title()
    normalized = ' '.join(normalized.split())
    return normalized


def calculate_name_similarity(name1: str, name2: str) -> float:
    """Calculate similarity between two names using Levenshtein distance."""
    if not name1 or not name2:
        return 0.0

    n1 = normalize_name(name1).lower()
    n2 = normalize_name(name2).lower()

    if n1 == n2:
        return 1.0

    if n1 in n2 or n2 in n1:
        return 0.85

    def levenshtein(s1, s2):
        if len(s1) < len(s2):
            return levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    distance = levenshtein(n1, n2)
    max_len = max(len(n1), len(n2))

    if max_len == 0:
        return 1.0

    similarity = 1.0 - (distance / max_len)
    return max(0.0, similarity)


def select_best_name(names: list) -> str:
    """Select the best quality name from a list of name variations."""
    if not names:
        return "Cliente"

    valid_names = [n.strip() for n in names if n and n.strip()]
    if not valid_names:
        return "Cliente"

    normalized_counts = Counter()
    name_examples = {}

    for name in valid_names:
        normalized_key = normalize_name(name).lower()
        normalized_counts[normalized_key] += 1
        if normalized_key not in name_examples:
            name_examples[normalized_key] = name
        else:
            existing = name_examples[normalized_key]
            if name == name.title() and existing != existing.title():
                name_examples[normalized_key] = name

    if not normalized_counts:
        return "Cliente"

    max_frequency = max(normalized_counts.values())
    most_frequent = [name_examples[k] for k, v in normalized_counts.items() if v == max_frequency]

    if len(most_frequent) == 1:
        return most_frequent[0]

    def score_name(name):
        score = 0
        normalized = name.strip()

        if ' ' in normalized:
            score += 100
        if normalized and normalized[0].isupper():
            score += 50
        if normalized == normalized.title():
            score += 25
        score += len(normalized)
        if normalized.isupper():
            score -= 20
        if normalized.islower():
            score -= 10

        return score

    scored_names = [(score_name(n), n) for n in most_frequent]
    scored_names.sort(reverse=True, key=lambda x: x[0])

    return scored_names[0][1]


# =============================================================================
# ROUTES
# =============================================================================

@router.get("/clients")
async def get_clients(
    search: Optional[str] = None,
    admin: dict = Depends(get_current_admin)
):
    """Get all clients with stats for the client directory."""
    try:
        all_appointments = await db.appointments.find({
            "tenant_id": DEFAULT_TENANT_ID
        }).sort("created_at", 1).to_list(length=10000)

        clients_map = {}
        client_counter = 0

        for apt in all_appointments:
            raw_phone = apt.get("phone", "")
            email = apt.get("customer_email", "")
            name = apt.get("name", "Cliente")

            normalized_phone = normalize_phone(raw_phone)

            if not normalized_phone and not email and not name:
                continue

            best_match_key = None
            best_confidence = 0.0

            for existing_key, existing_client in clients_map.items():
                confidence = 0.0

                if normalized_phone and existing_client["phone"] == normalized_phone:
                    confidence = 100.0
                elif email and existing_client["email"] == email:
                    confidence = 100.0
                else:
                    name_similarity = calculate_name_similarity(name, existing_client["names"][0])

                    if normalized_phone and existing_client["phone"] == normalized_phone and name_similarity >= 0.8:
                        confidence = 90.0
                    elif name_similarity >= 0.9:
                        confidence = 70.0

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match_key = existing_key

            if best_match_key and best_confidence >= 70.0:
                client_key = best_match_key
                existing = clients_map[client_key]

                if name not in existing["names"]:
                    existing["names"].append(name)

                if email and not existing["email"]:
                    existing["email"] = email

                if normalized_phone and not existing["phone"].startswith("+"):
                    existing["phone"] = normalized_phone

            else:
                client_key = normalized_phone or email or f"client_{client_counter}"
                client_counter += 1

                client_record = None
                if normalized_phone or raw_phone or email:
                    or_conditions = []
                    if normalized_phone:
                        or_conditions.append({"phone": normalized_phone, "tenant_id": DEFAULT_TENANT_ID})
                    if raw_phone and raw_phone != normalized_phone:
                        or_conditions.append({"phone": raw_phone, "tenant_id": DEFAULT_TENANT_ID})
                    if email:
                        or_conditions.append({"email": email, "tenant_id": DEFAULT_TENANT_ID})

                    if or_conditions:
                        client_record = await db.clients.find_one({"$or": or_conditions})

                clients_map[client_key] = {
                    "phone": normalized_phone or raw_phone,
                    "names": [name],
                    "first_name": name,
                    "email": email,
                    "appointments": [],
                    "notes": client_record.get("notes", "") if client_record else "",
                    "is_vip": client_record.get("is_vip", False) if client_record else False,
                    "profile_photo": client_record.get("profile_photo") if client_record else None,
                    "birthday": client_record.get("birthday") if client_record else None,
                    "created_at": apt.get("created_at"),
                    "preferences": {}
                }

                if client_record:
                    clients_map[client_key]["preferences"] = {
                        "favoriteSnacks": client_record.get("favoriteSnacks"),
                        "favoriteDrinks": client_record.get("favoriteDrinks"),
                        "favoriteMovie": client_record.get("favoriteMovie"),
                        "favoriteSeries": client_record.get("favoriteSeries"),
                        "favoriteMusic": client_record.get("favoriteMusic")
                    }

            clients_map[client_key]["appointments"].append(apt)

        enriched_clients = []

        for client_key, client_data in clients_map.items():
            appointments = client_data["appointments"]

            confirmed_appointments = [apt for apt in appointments if apt.get("status") == "confirmed"]
            total_appointments = len(confirmed_appointments)
            total_revenue = len(confirmed_appointments) * 250

            last_appointment = None
            next_appointment = None
            today_date = date.today()

            future_dates = []
            past_dates = []

            for apt in appointments:
                if apt.get("status") == "confirmed":
                    apt_date = apt.get("date")
                    if apt_date:
                        try:
                            apt_date_obj = datetime.strptime(apt_date, "%Y-%m-%d").date()

                            if apt_date_obj >= today_date:
                                future_dates.append(apt_date)
                            else:
                                past_dates.append(apt_date)
                        except:
                            pass

            if future_dates:
                next_appointment = min(future_dates)

            if past_dates:
                last_appointment = max(past_dates)

            is_returning = len(confirmed_appointments) > 1

            if search:
                search_lower = search.lower()

                name_match = False
                for name_var in client_data.get("names", []):
                    if search_lower in name_var.lower():
                        name_match = True
                        break

                phone_digits = ''.join(c for c in search if c.isdigit())
                phone_match = search in client_data["phone"] or (phone_digits and phone_digits in client_data["phone"])
                email_match = client_data["email"] and search_lower in client_data["email"].lower()

                if not (name_match or phone_match or email_match):
                    continue

            first_name = client_data.get("first_name")
            if first_name:
                best_name = normalize_name(first_name)
            else:
                best_name = select_best_name(client_data.get("names", ["Cliente"]))

            enriched_clients.append({
                "phone": client_data["phone"],
                "name": best_name,
                "name_variations": client_data.get("names", []),
                "email": client_data["email"],
                "birthday": client_data["birthday"],
                "created_at": client_data["created_at"],
                "notes": client_data["notes"],
                "is_vip": client_data["is_vip"],
                "is_returning": is_returning,
                "profile_photo": client_data["profile_photo"],
                "preferences": client_data["preferences"],
                "total_appointments": total_appointments,
                "total_revenue": total_revenue,
                "last_appointment": last_appointment,
                "next_appointment": next_appointment
            })

        enriched_clients.sort(key=lambda x: x["name"].lower())

        return {
            "success": True,
            "clients": enriched_clients,
            "total": len(enriched_clients)
        }

    except Exception as e:
        print(f"❌ Clients endpoint error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching clients: {str(e)}")


@router.put("/clients/{phone}")
async def update_client(
    phone: str,
    update_data: UpdateClientRequest,
    admin: dict = Depends(get_current_admin)
):
    """Update client information (notes, VIP status, etc.)."""
    try:
        normalized_phone = normalize_phone(phone)
        if not normalized_phone:
            normalized_phone = phone

        client = await db.clients.find_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "$or": [
                {"phone": normalized_phone},
                {"phone": phone}
            ]
        })

        update_doc = {"$set": {}}

        if update_data.notes is not None:
            update_doc["$set"]["notes"] = update_data.notes

        if update_data.is_vip is not None:
            update_doc["$set"]["is_vip"] = update_data.is_vip

        update_doc["$set"]["updated_at"] = datetime.now(timezone.utc).isoformat()
        update_doc["$set"]["updated_by"] = admin["email"]

        if client:
            await db.clients.update_one(
                {"_id": client["_id"]},
                update_doc
            )
        else:
            apt = await db.appointments.find_one({
                "tenant_id": DEFAULT_TENANT_ID,
                "$or": [
                    {"phone": normalized_phone},
                    {"phone": phone}
                ]
            })

            if not apt:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Client not found in appointments"
                )

            client_doc = {
                "tenant_id": DEFAULT_TENANT_ID,
                "phone": normalized_phone,
                "name": apt.get("name", "Cliente"),
                "email": apt.get("customer_email"),
                "notes": update_data.notes or "",
                "is_vip": update_data.is_vip or False,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "updated_by": admin["email"]
            }

            await db.clients.insert_one(client_doc)

        return {
            "success": True,
            "message": "Client updated successfully",
            "phone": phone
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Update client error: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating client: {str(e)}")


@router.delete("/clients/{phone}")
async def delete_client(
    phone: str,
    admin: dict = Depends(get_current_admin)
):
    """Delete a client and all their appointments."""
    try:
        normalized_phone = normalize_phone(phone)
        if not normalized_phone:
            normalized_phone = phone

        client_result = await db.clients.delete_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "$or": [
                {"phone": normalized_phone},
                {"phone": phone}
            ]
        })

        appointments_result = await db.appointments.delete_many({
            "tenant_id": DEFAULT_TENANT_ID,
            "$or": [
                {"phone": normalized_phone},
                {"phone": phone}
            ]
        })

        await db.client_memories.delete_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "phone": normalized_phone[-10:] if len(normalized_phone) >= 10 else normalized_phone
        })

        print(f"🗑️ Client deleted by {admin['email']}: {phone}")
        print(f"   - Client records deleted: {client_result.deleted_count}")
        print(f"   - Appointments deleted: {appointments_result.deleted_count}")

        return {
            "success": True,
            "message": "Cliente eliminado correctamente",
            "deleted": {
                "client_records": client_result.deleted_count,
                "appointments": appointments_result.deleted_count
            }
        }

    except Exception as e:
        print(f"❌ Delete client error: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting client: {str(e)}")

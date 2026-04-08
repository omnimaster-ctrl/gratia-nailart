"""
MercadoPago Payment Service for La Pop Nails
Handles payment processing using MercadoPago Checkout Pro
"""

import mercadopago
import os
from typing import Dict, Any


def get_sdk():
    """Get MercadoPago SDK instance with access token"""
    access_token = os.environ.get('MP_ACCESS_TOKEN')
    if not access_token:
        raise Exception("MP_ACCESS_TOKEN not configured")
    return mercadopago.SDK(access_token)


def create_preference(
    appointment_id: str,
    customer_name: str,
    customer_email: str,
    customer_phone: str,
    service_name: str,
    amount: float = 250.00,
    frontend_url: str = "https://lapopnails.mx"
) -> Dict[str, Any]:
    """
    Create a MercadoPago Checkout Pro preference.

    Args:
        appointment_id: Unique appointment ID
        customer_name: Customer's full name
        customer_email: Customer's email
        customer_phone: Customer's phone number
        service_name: Service name
        amount: Payment amount in MXN (default 250.00)
        frontend_url: Frontend URL for redirects

    Returns:
        Dict with preference_id and init_point (checkout URL)
    """
    try:
        sdk = get_sdk()

        # Build preference data
        name_parts = customer_name.split() if customer_name else ["Cliente"]
        preference_data = {
            "items": [
                {
                    "id": appointment_id,
                    "title": f"Anticipo - {service_name}",
                    "description": f"Anticipo para cita en La Pop Nails - {service_name}",
                    "quantity": 1,
                    "currency_id": "MXN",
                    "unit_price": float(amount)
                }
            ],
            "payer": {
                "name": name_parts[0],
                "surname": " ".join(name_parts[1:]) if len(name_parts) > 1 else name_parts[0],
                "email": customer_email,
                "phone": {
                    "area_code": "52",
                    "number": customer_phone[-10:] if len(customer_phone) >= 10 else customer_phone
                }
            },
            "payment_methods": {
                "installments": 1,
                "excluded_payment_types": []
            },
            "back_urls": {
                "success": f"{frontend_url}/payment-success",
                "failure": f"{frontend_url}/payment-failure",
                "pending": f"{frontend_url}/payment-pending"
            },
            "auto_return": "approved",
            "external_reference": appointment_id,
            "notification_url": os.environ.get(
                'BACKEND_URL',
                'https://lapopnails-backend-production.up.railway.app'
            ) + "/api/webhooks/mercadopago",
            "statement_descriptor": "LA POP NAILS",
        }

        # Create preference
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})

        if preference_response.get("status") in [200, 201]:
            return {
                "preference_id": preference.get("id"),
                "init_point": preference.get("init_point"),
                "sandbox_init_point": preference.get("sandbox_init_point"),
                "status": "created"
            }
        else:
            error_msg = preference.get("message", "Unknown error")
            raise Exception(f"MercadoPago API error: {error_msg}")

    except Exception as e:
        print(f"MercadoPago error: {e}")
        raise Exception(f"Error creating MercadoPago preference: {str(e)}")


def get_payment_info(payment_id: str) -> Dict[str, Any]:
    """
    Get payment information from MercadoPago.

    Args:
        payment_id: MercadoPago payment ID

    Returns:
        Payment details including status
    """
    try:
        sdk = get_sdk()
        payment_response = sdk.payment().get(payment_id)

        if payment_response.get("status") == 200:
            return payment_response.get("response", {})
        else:
            raise Exception(f"Could not fetch payment {payment_id}")

    except Exception as e:
        print(f"MercadoPago get payment error: {e}")
        raise


def get_merchant_order(order_id: str) -> Dict[str, Any]:
    """
    Get merchant order information from MercadoPago.

    Args:
        order_id: MercadoPago merchant order ID

    Returns:
        Order details
    """
    try:
        sdk = get_sdk()
        order_response = sdk.merchant_order().get(order_id)

        if order_response.get("status") == 200:
            return order_response.get("response", {})
        else:
            raise Exception(f"Could not fetch order {order_id}")

    except Exception as e:
        print(f"MercadoPago get order error: {e}")
        raise

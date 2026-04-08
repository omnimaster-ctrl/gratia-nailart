"""
WhatsApp Notification Service for La Pop Nails
Uses Twilio WhatsApp API for sending booking confirmations and reminders.
"""

from twilio.rest import Client
from datetime import datetime
import os

# Spanish day names
DIAS_SEMANA = {
    'Monday': 'lunes',
    'Tuesday': 'martes',
    'Wednesday': 'miércoles',
    'Thursday': 'jueves',
    'Friday': 'viernes',
    'Saturday': 'sábado',
    'Sunday': 'domingo'
}

def get_spanish_day_name(date_str: str) -> str:
    """Convert date string to Spanish day name."""
    try:
        # Try parsing different date formats
        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                english_day = date_obj.strftime('%A')
                return DIAS_SEMANA.get(english_day, english_day)
            except ValueError:
                continue
        return ""
    except Exception:
        return ""


def format_date_latam(date_str: str) -> str:
    """Convert YYYY-MM-DD to DD-MM-YYYY."""
    try:
        if not date_str:
            return ""
        # Parse standard ISO format
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d-%m-%Y')
    except Exception:
        # Return original if parsing fails
        return date_str


def get_twilio_client():
    """Initialize Twilio client with credentials from environment."""
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    if not account_sid or not auth_token:
        print("⚠️ Twilio credentials not configured")
        return None

    return Client(account_sid, auth_token)


def format_phone_for_whatsapp(phone: str) -> str:
    """Format phone number for WhatsApp (must include country code).

    For Mexico (Twilio Sandbox): WhatsApp uses +521 + 10 digits
    Example: 443 491 0277 -> whatsapp:+5214434910277
    """
    # Remove any non-digit characters
    digits_only = ''.join(filter(str.isdigit, phone))

    # If starts with +521 (Mexico mobile), use as-is
    if phone.startswith('+521'):
        return f"whatsapp:{phone}"

    # If starts with +52 but missing the 1, add it
    if phone.startswith('+52') and not phone.startswith('+521'):
        return f"whatsapp:+521{phone[3:]}"

    # If starts with other country code, use as-is
    if phone.startswith('+'):
        return f"whatsapp:{phone}"

    # Mexico: If has 521 prefix (13 digits) - use as-is
    if len(digits_only) == 13 and digits_only.startswith('521'):
        return f"whatsapp:+{digits_only}"

    # Mexico: If has 52 prefix (12 digits) - add the "1"
    if len(digits_only) == 12 and digits_only.startswith('52'):
        return f"whatsapp:+521{digits_only[2:]}"

    # Mexico: If has 52 prefix (11 digits) - add the "1"
    if len(digits_only) == 11 and digits_only.startswith('52'):
        return f"whatsapp:+521{digits_only[2:]}"

    # Mexico 10-digit number: add +521 (country code + mobile prefix)
    if len(digits_only) == 10:
        return f"whatsapp:+521{digits_only}"

    # If already has country code without +
    if len(digits_only) > 10:
        return f"whatsapp:+{digits_only}"

    # Default: Mexico 10-digit with +521
    return f"whatsapp:+521{digits_only}"


async def send_whatsapp_confirmation(phone: str, appointment_data: dict) -> bool:
    """
    Send booking confirmation via WhatsApp using approved template.

    Template: appointment_confirmation
    Variables:
      {{1}} = First name
      {{2}} = Date (e.g., "lunes 20 de enero")
      {{3}} = Time (e.g., "10:00 AM")

    Args:
        phone: Customer phone number
        appointment_data: Dict containing name, date, time, service

    Returns:
        bool: True if message sent successfully
    """
    import json
    
    client = get_twilio_client()
    if not client:
        print("❌ Twilio not configured - skipping WhatsApp confirmation")
        return False

    whatsapp_to = format_phone_for_whatsapp(phone)
    whatsapp_from = os.environ.get('TWILIO_WHATSAPP_FROM')
    if not whatsapp_from:
        print("TWILIO_WHATSAPP_FROM not configured - cannot send WhatsApp")
        return False

    # Template SID for confirmacion_cita_utility_v4 (Approved Feb 5 2026)
    # UTILITY category - high deliverability, no Meta throttling
    # Fallback: v2 (HXe3d47c5d4df401f3351ce127bf2cbb3c) if issues arise
    template_sid = os.environ.get(
        'WHATSAPP_CONFIRMATION_TEMPLATE_SID',
        'HX1782e8fd5d82f07a33ff2ada0f4a0a70'
    )

    # Get client's first name and capitalize it
    full_name = appointment_data.get('name', 'hermosa')
    first_name = full_name.split()[0].capitalize() if full_name else 'hermosa'

    # Format date with Latam format (DD-MM-YYYY)
    date_str = appointment_data.get('date', '')
    latam_date = format_date_latam(date_str)
    full_date_str = latam_date  # Just the date in DD-MM-YYYY format

    # Get time - format it nicely
    raw_time = appointment_data.get('time', '')
    schedule = appointment_data.get('schedule', '')

    # Format time to be human readable (e.g., "10:00" -> "10:00 AM")
    def format_time_display(time_val):
        if not time_val:
            return schedule  # Fallback to schedule
        try:
            # If it's already formatted (contains AM/PM), use as is
            if 'AM' in time_val.upper() or 'PM' in time_val.upper():
                return time_val
            # Parse HH:MM format
            hour, minute = time_val.split(':')
            hour_int = int(hour)
            if hour_int < 12:
                return f"{hour_int}:{minute} AM"
            elif hour_int == 12:
                return f"12:{minute} PM"
            else:
                return f"{hour_int - 12}:{minute} PM"
        except:
            return time_val or schedule

    time_str = format_time_display(raw_time)

    # Build content variables for template
    # Variables: {{1}}=name, {{2}}=date, {{3}}=time
    content_variables = json.dumps({
        "1": first_name,
        "2": full_date_str,
        "3": time_str
    })

    try:
        message = client.messages.create(
            content_sid=template_sid,
            content_variables=content_variables,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        print(f"✅ WhatsApp confirmation sent to {whatsapp_to}: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ WhatsApp confirmation error: {e}")
        return False


async def send_owner_new_appointment_notification(appointment_data: dict) -> bool:
    """
    Notify Pop (business owner) via WhatsApp when a new appointment is confirmed.

    Uses the same approved template as client confirmations, but addresses Pop
    and packs client info into the time variable. This works immediately without
    needing a separate Meta-approved template.

    Returns:
        bool: True if message sent successfully
    """
    import json

    owner_phone = os.environ.get('POP_WHATSAPP_PHONE')
    if not owner_phone:
        print("⚠️ POP_WHATSAPP_PHONE not configured - skipping owner notification")
        return False

    client = get_twilio_client()
    if not client:
        return False

    whatsapp_to = format_phone_for_whatsapp(owner_phone)
    whatsapp_from = os.environ.get('TWILIO_WHATSAPP_FROM')
    if not whatsapp_from:
        print("TWILIO_WHATSAPP_FROM not configured - cannot send WhatsApp")
        return False
    template_sid = os.environ.get(
        'WHATSAPP_CONFIRMATION_TEMPLATE_SID',
        'HX1782e8fd5d82f07a33ff2ada0f4a0a70'
    )

    client_name = appointment_data.get('name', 'Cliente')
    service = appointment_data.get('service', '')
    date_str = format_date_latam(appointment_data.get('date', ''))

    raw_time = appointment_data.get('time', '')
    try:
        hour, minute = raw_time.split(':')
        hour_int = int(hour)
        if hour_int < 12:
            time_str = f"{hour_int}:{minute} AM"
        elif hour_int == 12:
            time_str = f"12:{minute} PM"
        else:
            time_str = f"{hour_int - 12}:{minute} PM"
    except:
        time_str = raw_time

    # Pack client info into template variables:
    # {{1}}=Pop, {{2}}=date, {{3}}="10:00 AM — Cliente: David Tello (Extensión Híbrida)"
    content_variables = json.dumps({
        "1": "Pop",
        "2": date_str,
        "3": f"{time_str} — {client_name} ({service})"
    })

    try:
        message = client.messages.create(
            content_sid=template_sid,
            content_variables=content_variables,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        print(f"✅ Owner WhatsApp notification sent to {whatsapp_to}: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ Owner WhatsApp notification error: {e}")
        return False


async def send_whatsapp_reminder(phone: str, appointment_data: dict) -> bool:
    """
    Send appointment reminder 24h before via WhatsApp.
    
    Args:
        phone: Customer phone number
        appointment_data: Dict containing name, date, time, service
    
    Returns:
        bool: True if message sent successfully
    """
    client = get_twilio_client()
    if not client:
        print("❌ Twilio not configured - skipping WhatsApp reminder")
        return False

    whatsapp_to = format_phone_for_whatsapp(phone)
    whatsapp_from = os.environ.get('TWILIO_WHATSAPP_FROM')
    if not whatsapp_from:
        print("TWILIO_WHATSAPP_FROM not configured - cannot send WhatsApp")
        return False

    message_body = f"""*La Pop Nails - Recordatorio*

Hola {appointment_data.get('name', 'Cliente')}, tu cita es MANANA:

*Fecha:* {format_date_latam(appointment_data.get('date', 'N/A'))}
*Hora:* {appointment_data.get('time', 'N/A')}
*Servicio:* {appointment_data.get('service', 'N/A')}

Recuerda llegar puntual. Tolerancia: 15 min.
Resto a pagar en el salon.

Te esperamos!
212: 
213: ✨ Ojo hermosa: este es un chat automático y no puedo leer respuestas por aquí 🥺.
Si necesitas hacer cambios o tienes dudas, mándame mensajito a mi número personal: *+52 443 6287997* 📲"""

    try:
        message = client.messages.create(
            body=message_body,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        print(f"✅ WhatsApp reminder sent to {whatsapp_to}: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ WhatsApp reminder error: {e}")
        return False


async def send_whatsapp_cancellation(phone: str, appointment_data: dict) -> bool:
    """
    Send cancellation notification via WhatsApp.
    
    Args:
        phone: Customer phone number
        appointment_data: Dict containing name, date, time, service, reason
    
    Returns:
        bool: True if message sent successfully
    """
    client = get_twilio_client()
    if not client:
        print("❌ Twilio not configured - skipping WhatsApp cancellation")
        return False

    whatsapp_to = format_phone_for_whatsapp(phone)
    whatsapp_from = os.environ.get('TWILIO_WHATSAPP_FROM')
    if not whatsapp_from:
        print("TWILIO_WHATSAPP_FROM not configured - cannot send WhatsApp")
        return False

    # Get client's first name and capitalize it
    full_name = appointment_data.get('name', 'hermosa')
    first_name = full_name.split()[0].capitalize() if full_name else 'hermosa'

    # Format date robustly
    date_str = appointment_data.get('date', '')
    full_date_str = format_date_latam(date_str)

    # Get time
    raw_time = appointment_data.get('time', '')

    # Format time to be human readable
    def format_time_display(time_val):
        if not time_val:
            return ""
        try:
            if 'AM' in time_val.upper() or 'PM' in time_val.upper():
                return time_val
            hour, minute = time_val.split(':')
            hour_int = int(hour)
            if hour_int < 12:
                return f"{hour_int}:{minute} AM"
            elif hour_int == 12:
                return f"12:{minute} PM"
            else:
                return f"{hour_int - 12}:{minute} PM"
        except:
            return time_val

    time_str = format_time_display(raw_time)

    # Build reason section if provided
    reason_section = ""
    if appointment_data.get('reason'):
        reason_section = f"\n💬 Motivo: {appointment_data['reason']}\n"

    message_body = f"""Hola {first_name}, 😔

Lamento informarte que tu cita ha sido cancelada.

📅 Detalles de la cita:
• Servicio: {appointment_data.get('service', 'N/A')}
• Fecha: {full_date_str}
• Hora: {time_str}
{reason_section}
Si deseas agendar una nueva cita, estaré encantada de atenderte. Puedes:

🌐 Visitar: https://lapopnails.mx

✨ Ojo hermosa: este es un chat automático y no puedo leer respuestas por aquí 🥺.
Si necesitas hacer cambios o tienes dudas, mándame mensajito a mi número personal: *+52 443 6287997* 📲

Con cariño,
Paloma – PopNails 💖"""

    try:
        message = client.messages.create(
            body=message_body,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        print(f"✅ WhatsApp cancellation sent to {whatsapp_to}: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ WhatsApp cancellation error: {e}")
        return False


async def send_whatsapp_test(phone: str) -> bool:
    """
    Send a test WhatsApp message using the Confirmed Template structure.
    This ensures compatibility with Production numbers.
    """
    print(f"🔍 DEBUG - Testing with Template-Compatible format...")
    
    # Use dummy data to simulate a real appointment
    # This verifies if the Template Message logic works
    dummy_data = {
        "name": "David (Test)",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "12:00",
        "service": "Test Service",
        "schedule": "12:00 - 14:00"
    }
    
    # Reuse the confirmation logic which sends the exact template text
    return await send_whatsapp_confirmation(phone, dummy_data)

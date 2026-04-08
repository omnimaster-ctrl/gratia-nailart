"""
Email service for La Pop Nails.
Sends confirmation, cancellation, and reschedule notification emails via Resend.
"""

import os
from datetime import datetime
import resend

resend.api_key = os.environ.get('RESEND_API_KEY', '')


async def send_confirmation_email(customer_email: str, appointment_data: dict):
    """Send confirmation email using Resend API - v2.1 GOLD TEXT"""
    try:
        print("📧 Email template version: 2.1 - GOLD TEXT #D4AF37")
        if not resend.api_key:
            print("❌ Resend API key not configured")
            return False

        current_year = datetime.now().year

        notes_row = ""
        if appointment_data.get('notes'):
            notes_row = f'''
                        <tr>
                          <td style="padding:10px 10px;background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">✎</span>&nbsp; Notas:
                            </span>
                          </td>
                          <td style="padding:10px 10px;background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data['notes']}
                            </span>
                          </td>
                        </tr>'''

        html_content = f'''<!doctype html>
<html lang="es" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="x-apple-disable-message-reformatting" />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <title>POP NAILS — Cita Confirmada</title>
    <!--[if mso]>
      <xml>
        <o:OfficeDocumentSettings>
          <o:PixelsPerInch>96</o:PixelsPerInch>
          <o:AllowPNG/>
        </o:OfficeDocumentSettings>
      </xml>
      <style type="text/css">
        .title-text {{ font-family: Georgia, 'Times New Roman', serif !important; }}
      </style>
    <![endif]-->
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&display=swap');
    </style>
  </head>
  <body style="margin:0;padding:0;background-color:#F3BCC7;">
    <div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">
      Tu anticipo ha sido procesado exitosamente. Tu cita está confirmada.
    </div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;background-color:#F3BCC7;">
      <tr>
        <td align="center" style="padding:22px 12px;">
          <table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0"
            style="border-collapse:separate;width:640px;max-width:640px;background-color:#FCE4E8;border-radius:22px;">
            <tr>
              <td align="center" style="padding:28px 18px 18px 18px;">
                <div style="font-family:'Montserrat',Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;letter-spacing:8px;color:#D4AF37;text-align:center;text-transform:uppercase;font-weight:600;">
                  <font color="#D4AF37" style="color:#D4AF37;">POP NAILS</font>
                </div>
                <div style="height:24px;line-height:24px;font-size:24px;">&nbsp;</div>
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin:0 auto;">
                  <tr>
                    <td valign="middle" style="padding-right:12px;">
                      <span style="font-size:16px;color:#D4AF37;"><font color="#D4AF37">✦</font></span>
                    </td>
                    <td valign="middle">
                      <div style="font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif;font-size:48px;line-height:54px;font-weight:600;font-style:italic;text-align:center;color:#D4AF37;"><font color="#D4AF37" style="color:#D4AF37;">¡Cita Confirmada!</font></div>
                    </td>
                    <td valign="top" style="padding-left:10px;position:relative;">
                      <span style="font-size:14px;color:#D4AF37;"><font color="#D4AF37">✦</font></span>
                      <br/>
                      <span style="font-size:10px;color:#D4AF37;padding-left:8px;"><font color="#D4AF37">✧</font></span>
                    </td>
                  </tr>
                </table>
                <div style="height:12px;line-height:12px;font-size:12px;">&nbsp;</div>
                <div style="font-family:'Montserrat',Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#6B6B6B;text-align:center;font-weight:400;letter-spacing:0.5px;">
                  Tu anticipo ha sido procesado exitosamente
                </div>
                <div style="height:24px;line-height:24px;font-size:24px;">&nbsp;</div>
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                  style="border-collapse:separate;background:radial-gradient(ellipse at center,#FFFDF8 0%,#FBF6E8 50%,#F5EED9 100%);border:3px solid #C9A962;border-radius:18px;box-shadow:0 0 15px rgba(201,169,98,0.4);">
                  <tr>
                    <td style="padding:18px 18px 0 18px;">
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:24px;color:#2A2A2A;font-weight:700;">
                        Hola {appointment_data['name']}!
                      </div>
                      <div style="height:8px;line-height:8px;font-size:8px;">&nbsp;</div>
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:22px;color:#2A2A2A;">
                        Tu anticipo ha sido procesado exitosamente. Tu cita ya está asegurada.
                      </div>
                      <div style="height:14px;line-height:14px;font-size:14px;">&nbsp;</div>
                      <div style="text-align:center;">
                        <div style="display:inline-block;background-color:#203828;border-radius:50px;padding:12px 20px;border:3px solid #C9A962;">
                          <span style="display:inline-block;vertical-align:middle;width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background-color:#C9A962;color:#203828;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:700;">✓</span>
                          <span style="display:inline-block;vertical-align:middle;width:8px;">&nbsp;</span>
                          <span style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:20px;color:#F5EED9;font-weight:700;vertical-align:middle;">Anticipo Pagado - Cita Asegurada</span>
                        </div>
                      </div>
                      <div style="height:16px;line-height:16px;font-size:16px;">&nbsp;</div>
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;color:#2A2A2A;font-weight:800;">
                        Detalles de tu Cita:
                      </div>
                      <div style="height:10px;line-height:10px;font-size:10px;">&nbsp;</div>
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                        style="border-collapse:collapse;border:1px solid #D7C8A6;">
                        <tr>
                          <td width="42%" style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">▦</span>&nbsp; Fecha:
                            </span>
                          </td>
                          <td width="58%" style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data['date']}
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">◔</span>&nbsp; Horario:
                            </span>
                          </td>
                          <td style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data.get('schedule', appointment_data['time'])}
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">✂</span>&nbsp; Servicio:
                            </span>
                          </td>
                          <td style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data['service']}
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">✆</span>&nbsp; Teléfono:
                            </span>
                          </td>
                          <td style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data['phone']}
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td style="padding:10px 10px;{"border-bottom:1px solid #D7C8A6;" if appointment_data.get('notes') else ""}background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">⊡</span>&nbsp; Anticipo:
                            </span>
                          </td>
                          <td style="padding:10px 10px;{"border-bottom:1px solid #D7C8A6;" if appointment_data.get('notes') else ""}background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              $250 MXN
                            </span>
                          </td>
                        </tr>{notes_row}
                      </table>
                      <div style="height:18px;line-height:18px;font-size:18px;">&nbsp;</div>
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;color:#2A2A2A;font-weight:800;">
                        ¿Qué sigue?
                      </div>
                      <div style="height:8px;line-height:8px;font-size:8px;">&nbsp;</div>
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin-bottom:14px;">
                        <tr>
                          <td width="18" valign="top" style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:20px;color:#2A2A2A;">•</td>
                          <td valign="top" style="padding:6px 0;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2A2A2A;">
                              📅 Tu cita ya está en nuestro calendario.
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td width="18" valign="top" style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:20px;color:#2A2A2A;">•</td>
                          <td valign="top" style="padding:6px 0;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2A2A2A;">
                              📱 Te contactaremos por WhatsApp si necesitamos algo.
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td width="18" valign="top" style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:20px;color:#2A2A2A;">•</td>
                          <td valign="top" style="padding:6px 0;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2A2A2A;">
                              🏷️ Llega 5–10 min antes para confirmar el servicio y el diseño.
                            </span>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:12px 18px 18px 18px;">
                      <div style="background-color:#EDE5D4;border:2px solid #C9A962;border-radius:12px;padding:16px 20px;">
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;font-weight:800;text-align:center;">
                          Recordatorio:
                        </div>
                        <div style="height:6px;"></div>
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#2A2A2A;text-align:center;">
                          El anticipo es no reembolsable si cancelas con menos de <b>24 horas</b> de anticipación.
                          Gracias por elegir <b>POP NAILS</b>.
                        </div>
                      </div>
                    </td>
                  </tr>
                </table>
                <div style="height:20px;line-height:20px;font-size:20px;">&nbsp;</div>
                <!-- Reschedule Button -->
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                  <tr>
                    <td align="center" style="background-color:#D4AF37;border-radius:8px;">
                      <a href="{os.environ.get('FRONTEND_URL', 'https://frontend-popnails-production.up.railway.app')}/reagendar/{appointment_data.get('reschedule_token', '')}"
                         target="_blank"
                         style="display:inline-block;padding:12px 24px;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:600;color:#FFFFFF;text-decoration:none;">
                        📅 ¿Necesitas reagendar? Haz clic aquí
                      </a>
                    </td>
                  </tr>
                </table>
                <div style="height:8px;line-height:8px;font-size:8px;">&nbsp;</div>
                <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;line-height:16px;color:#888888;text-align:center;">
                  Solo puedes reagendar una vez y con al menos 24 horas de anticipación.
                </div>
                <div style="height:14px;line-height:14px;font-size:14px;">&nbsp;</div>
                <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#6B5B3E;text-align:center;">
                  © {current_year} POP NAILS.
                </div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>'''

        params = {
            "from": "La Pop Nails <hola@lapopnails.mx>",
            "to": [customer_email],
            "subject": "✨ ¡Tu cita en La Pop Nails está confirmada!",
            "html": html_content
        }

        response = resend.Emails.send(params)
        print(f"✅ Confirmation email sent successfully to {customer_email} - ID: {response.get('id', 'unknown')}")
        return True

    except Exception as e:
        print(f"❌ Failed to send confirmation email: {str(e)}")
        raise e


async def send_cancellation_email(customer_email: str, appointment_data: dict):
    """Send cancellation notification email using Resend API - Elegant format matching confirmation"""
    try:
        print("📧 Sending cancellation email...")
        if not resend.api_key:
            print("❌ Resend API key not configured")
            return False

        current_year = datetime.now().year

        reason_row = ""
        if appointment_data.get('reason'):
            reason_row = f'''
                        <tr>
                          <td style="padding:10px 10px;background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">✎</span>&nbsp; Motivo:
                            </span>
                          </td>
                          <td style="padding:10px 10px;background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data['reason']}
                            </span>
                          </td>
                        </tr>'''

        html_content = f'''<!doctype html>
<html lang="es" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="x-apple-disable-message-reformatting" />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <title>POP NAILS — Cita Cancelada</title>
    <!--[if mso]>
      <xml>
        <o:OfficeDocumentSettings>
          <o:PixelsPerInch>96</o:PixelsPerInch>
          <o:AllowPNG/>
        </o:OfficeDocumentSettings>
      </xml>
      <style type="text/css">
        .title-text {{ font-family: Georgia, 'Times New Roman', serif !important; }}
      </style>
    <![endif]-->
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&display=swap');
    </style>
  </head>
  <body style="margin:0;padding:0;background-color:#F3BCC7;">
    <div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">
      Tu cita ha sido cancelada. Lamentamos el inconveniente.
    </div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;background-color:#F3BCC7;">
      <tr>
        <td align="center" style="padding:22px 12px;">
          <table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0"
            style="border-collapse:separate;width:640px;max-width:640px;background-color:#FCE4E8;border-radius:22px;">
            <tr>
              <td align="center" style="padding:28px 18px 18px 18px;">
                <div style="font-family:'Montserrat',Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;letter-spacing:8px;color:#D4AF37;text-align:center;text-transform:uppercase;font-weight:600;">
                  <font color="#D4AF37" style="color:#D4AF37;">POP NAILS</font>
                </div>
                <div style="height:24px;line-height:24px;font-size:24px;">&nbsp;</div>
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin:0 auto;">
                  <tr>
                    <td valign="middle" style="padding-right:12px;">
                      <span style="font-size:16px;color:#D4AF37;"><font color="#D4AF37">✦</font></span>
                    </td>
                    <td valign="middle">
                      <div style="font-family:'Cormorant Garamond',Georgia,'Times New Roman',serif;font-size:48px;line-height:54px;font-weight:600;font-style:italic;text-align:center;color:#D4AF37;"><font color="#D4AF37" style="color:#D4AF37;">Cita Cancelada</font></div>
                    </td>
                    <td valign="top" style="padding-left:10px;position:relative;">
                      <span style="font-size:14px;color:#D4AF37;"><font color="#D4AF37">✦</font></span>
                      <br/>
                      <span style="font-size:10px;color:#D4AF37;padding-left:8px;"><font color="#D4AF37">✧</font></span>
                    </td>
                  </tr>
                </table>
                <div style="height:12px;line-height:12px;font-size:12px;">&nbsp;</div>
                <div style="font-family:'Montserrat',Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#6B6B6B;text-align:center;font-weight:400;letter-spacing:0.5px;">
                  Lamentamos informarte sobre la cancelación
                </div>
                <div style="height:24px;line-height:24px;font-size:24px;">&nbsp;</div>
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                  style="border-collapse:separate;background:radial-gradient(ellipse at center,#FFFDF8 0%,#FBF6E8 50%,#F5EED9 100%);border:3px solid #C9A962;border-radius:18px;box-shadow:0 0 15px rgba(201,169,98,0.4);">
                  <tr>
                    <td style="padding:18px 18px 0 18px;">
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:24px;color:#2A2A2A;font-weight:700;">
                        Hola {appointment_data.get('name', 'Cliente')}!
                      </div>
                      <div style="height:8px;line-height:8px;font-size:8px;">&nbsp;</div>
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:22px;color:#2A2A2A;">
                        Lamento mucho informarte que ha sido necesario cancelar tu cita. Entiendo lo frustrante que puede ser y te pido una disculpa sincera por cualquier inconveniente que esto te cause.
                      </div>
                      <div style="height:16px;line-height:16px;font-size:16px;">&nbsp;</div>
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:20px;line-height:24px;color:#2A2A2A;font-weight:800;">
                        Detalles de la Cita Cancelada:
                      </div>
                      <div style="height:10px;line-height:10px;font-size:10px;">&nbsp;</div>
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                        style="border-collapse:collapse;border:1px solid #D7C8A6;">
                        <tr>
                          <td width="42%" style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">▦</span>&nbsp; Fecha:
                            </span>
                          </td>
                          <td width="58%" style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data.get('date', 'N/A')}
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">◔</span>&nbsp; Horario:
                            </span>
                          </td>
                          <td style="padding:10px 10px;border-bottom:1px solid #D7C8A6;background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data.get('time', 'N/A')}
                            </span>
                          </td>
                        </tr>
                        <tr>
                          <td style="padding:10px 10px;{"border-bottom:1px solid #D7C8A6;" if appointment_data.get('reason') else ""}background-color:#F5EEDB;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#6B5B3E;font-weight:800;">
                              <span style="color:#B8976C;font-size:20px;">✂</span>&nbsp; Servicio:
                            </span>
                          </td>
                          <td style="padding:10px 10px;{"border-bottom:1px solid #D7C8A6;" if appointment_data.get('reason') else ""}background-color:#FFF9EA;">
                            <span style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:18px;color:#2A2A2A;">
                              {appointment_data.get('service', 'N/A')}
                            </span>
                          </td>
                        </tr>{reason_row}
                      </table>
                      <div style="height:18px;line-height:18px;font-size:18px;">&nbsp;</div>
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:17px;line-height:24px;color:#2A2A2A;font-weight:700;text-align:center;">
                        💕 Me encantaría atenderte en otra fecha
                      </div>
                      <div style="height:8px;line-height:8px;font-size:8px;">&nbsp;</div>
                      <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#2A2A2A;text-align:center;">
                        Si quieres reagendar, te invito a visitar nuestra página web donde podrás ver todas las fechas disponibles y elegir la que mejor te convenga.
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:12px 18px 18px 18px;">
                      <div style="background-color:#EDE5D4;border:2px solid #C9A962;border-radius:12px;padding:12px 20px;text-align:center;">
                        <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#6B5B3E;">
                          También puedes escribirme por WhatsApp si tienes dudas: <b>+52 443 243 6676</b>
                        </div>
                      </div>
                    </td>
                  </tr>
                </table>
                <div style="height:20px;line-height:20px;font-size:20px;">&nbsp;</div>
                <!-- Reagendar Button -->
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                  <tr>
                    <td align="center" style="background-color:#D4AF37;border-radius:8px;">
                      <a href="https://lapopnails.mx"
                         target="_blank"
                         style="display:inline-block;padding:12px 24px;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:600;color:#FFFFFF;text-decoration:none;">
                        💅 Reagendar Mi Cita
                      </a>
                    </td>
                  </tr>
                </table>
                <div style="height:14px;line-height:14px;font-size:14px;">&nbsp;</div>
                <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#6B5B3E;text-align:center;">
                  Gracias por tu comprensión. Espero verte pronto para consentir tus manos 💅✨
                </div>
                <div style="height:14px;line-height:14px;font-size:14px;">&nbsp;</div>
                <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#6B5B3E;text-align:center;">
                  © {current_year} POP NAILS.
                </div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>'''

        params = {
            "from": "La Pop Nails <hola@lapopnails.mx>",
            "to": [customer_email],
            "subject": "❌ Cita Cancelada - La Pop Nails",
            "html": html_content
        }

        response = resend.Emails.send(params)
        print(f"✅ Cancellation email sent successfully to {customer_email} - ID: {response.get('id', 'unknown')}")
        return True

    except Exception as e:
        print(f"❌ Failed to send cancellation email: {str(e)}")
        return False


async def send_reschedule_blocked_notification(customer_email: str, customer_name: str, appointment_date: str, appointment_schedule: str):
    """Send informative email when reschedule is blocked"""
    try:
        if not resend.api_key:
            print("❌ Resend API key not configured")
            return False

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #fdf2f8 0%, #ffffff 50%, #fef7f7 100%); }}
                .header {{ background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .info-box {{ background: #fef3c7; padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #f59e0b; }}
                .new-appointment-box {{ background: #ecfdf5; padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #10b981; }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; color: #6b7280; }}
                .button {{ background: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>¿Necesitas cambiar tu fecha? 💅</h1>
                    <p>Te ayudamos con las opciones disponibles</p>
                </div>

                <div class="content">
                    <h2>¡Hola {customer_name}!</h2>
                    <p>Entendemos que a veces necesitas cambiar tu fecha de cita. Te escribimos para informarte sobre tus opciones disponibles.</p>

                    <div class="info-box">
                        <h3 style="color: #92400e; margin-top: 0;">📅 Tu cita actual:</h3>
                        <p><strong>Fecha:</strong> {appointment_date}</p>
                        <p><strong>Horario:</strong> {appointment_schedule}</p>
                        <p><strong>Estado:</strong> Ya reagendada anteriormente</p>
                    </div>

                    <h3 style="color: #be185d;">✨ ¿Necesitas cambiar tu fecha nuevamente?</h3>
                    <p>Como ya reagendaste esta cita una vez, tienes estas opciones:</p>

                    <div class="new-appointment-box">
                        <h4 style="color: #065f46; margin-top: 0;">🆕 Opción 1: Nueva Cita</h4>
                        <p>Puedes agendar una <strong>NUEVA CITA</strong> con un nuevo anticipo de <strong>$250 MXN</strong>.</p>
                        <p>• Tendrás total flexibilidad de fechas</p>
                        <p>• Proceso rápido y automático</p>
                        <p>• Confirmación inmediata</p>
                    </div>

                    <div class="info-box">
                        <h4 style="color: #92400e; margin-top: 0;">📞 Opción 2: Contacto Directo</h4>
                        <p>Contáctanos por Instagram <strong>@___lapopnails</strong> para explorar más opciones.</p>
                        <p>• Nuestro equipo te ayudará personalmente</p>
                        <p>• Podemos buscar soluciones especiales</p>
                        <p>• Respuesta rápida por DM</p>
                    </div>

                    <p style="text-align: center; margin: 30px 0;">
                        <strong>¡Te esperamos para crear magia en tus uñas! 💅✨</strong>
                    </p>
                </div>

                <div class="footer">
                    <p><strong>La Pop Nails</strong></p>
                    <p>📱 Instagram: @___lapopnails</p>
                    <p style="font-size: 12px; margin-top: 20px;">
                        Estamos aquí para ayudarte. ¡Contáctanos cuando gustes!
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        params = {
            "from": "La Pop Nails <hola@lapopnails.mx>",
            "to": [customer_email],
            "subject": "💅 ¿Necesitas cambiar tu cita? - La Pop Nails",
            "html": html_content
        }

        response = resend.Emails.send(params)
        print(f"✅ Reschedule blocked notification sent successfully to {customer_email} - ID: {response.get('id', 'unknown')}")
        return True

    except Exception as e:
        print(f"❌ Failed to send reschedule blocked notification: {str(e)}")
        return False


async def send_owner_appointment_email(appointment_data: dict):
    """
    Notify the business owner (Pop) via email when a new appointment is confirmed.
    Clean, minimal design — just the facts Pop needs at a glance.
    """
    try:
        owner_email = os.environ.get('POP_NOTIFICATION_EMAIL')
        if not owner_email:
            print("⚠️ POP_NOTIFICATION_EMAIL not configured - skipping owner email")
            return False

        if not resend.api_key:
            print("❌ Resend API key not configured")
            return False

        client_name = appointment_data.get('name', 'Cliente')
        service = appointment_data.get('service', '')
        date_str = appointment_data.get('date', '')
        time_str = appointment_data.get('time', '')
        phone = appointment_data.get('phone', '')
        email = appointment_data.get('customer_email', '')
        source = appointment_data.get('source', 'web')

        # Format time for display
        try:
            hour, minute = time_str.split(':')
            hour_int = int(hour)
            if hour_int < 12:
                display_time = f"{hour_int}:{minute} AM"
            elif hour_int == 12:
                display_time = f"12:{minute} PM"
            else:
                display_time = f"{hour_int - 12}:{minute} PM"
        except:
            display_time = time_str

        # Format date for display
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            dias = {'Monday':'Lunes','Tuesday':'Martes','Wednesday':'Miércoles',
                    'Thursday':'Jueves','Friday':'Viernes','Saturday':'Sábado','Sunday':'Domingo'}
            day_name = dias.get(date_obj.strftime('%A'), '')
            display_date = f"{day_name} {date_obj.day}/{date_obj.month}/{date_obj.year}"
        except:
            display_date = date_str

        source_label = "🤖 Bot" if source == "agent" else "🌐 Web"

        html_content = f'''<!doctype html>
<html lang="es">
<head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/></head>
<body style="margin:0;padding:0;background:#FDF8F0;font-family:Arial,Helvetica,sans-serif;">
  <div style="max-width:480px;margin:20px auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
    <div style="background:#D4AF37;padding:16px 24px;text-align:center;">
      <h1 style="margin:0;color:#fff;font-size:18px;letter-spacing:1px;">💅 NUEVA CITA CONFIRMADA</h1>
    </div>
    <div style="padding:24px;">
      <table style="width:100%;border-collapse:collapse;">
        <tr>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#8B7355;font-size:13px;width:90px;">Cliente</td>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#2A2A2A;font-size:15px;font-weight:600;">{client_name}</td>
        </tr>
        <tr>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#8B7355;font-size:13px;">Servicio</td>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#2A2A2A;font-size:15px;">{service}</td>
        </tr>
        <tr>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#8B7355;font-size:13px;">Fecha</td>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#2A2A2A;font-size:15px;font-weight:600;">{display_date}</td>
        </tr>
        <tr>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#8B7355;font-size:13px;">Hora</td>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#2A2A2A;font-size:15px;font-weight:600;">{display_time}</td>
        </tr>
        <tr>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#8B7355;font-size:13px;">Teléfono</td>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#2A2A2A;font-size:15px;">{phone}</td>
        </tr>
        <tr>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#8B7355;font-size:13px;">Email</td>
          <td style="padding:10px 8px;border-bottom:1px solid #f0e8d8;color:#2A2A2A;font-size:14px;">{email}</td>
        </tr>
        <tr>
          <td style="padding:10px 8px;color:#8B7355;font-size:13px;">Origen</td>
          <td style="padding:10px 8px;color:#2A2A2A;font-size:14px;">{source_label}</td>
        </tr>
      </table>
      <div style="margin-top:20px;padding:12px;background:#F0FFF4;border-radius:8px;text-align:center;">
        <span style="color:#059669;font-size:14px;font-weight:600;">✅ Anticipo pagado — $250 MXN</span>
      </div>
    </div>
    <div style="padding:12px 24px;background:#FDF8F0;text-align:center;">
      <span style="color:#8B7355;font-size:12px;">La Pop Nails — Notificación automática</span>
    </div>
  </div>
</body>
</html>'''

        params = {
            "from": "La Pop Nails <hola@lapopnails.mx>",
            "to": [owner_email],
            "subject": f"💅 Nueva cita: {client_name} — {display_date} {display_time}",
            "html": html_content
        }

        response = resend.Emails.send(params)
        print(f"✅ Owner email notification sent to {owner_email} - ID: {response.get('id', 'unknown')}")
        return True

    except Exception as e:
        print(f"❌ Failed to send owner email notification: {str(e)}")
        return False

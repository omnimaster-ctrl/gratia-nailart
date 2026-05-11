# Launch Prep — Integration Questions & Cost Analysis

Reference doc for what to ask Hazael, expected costs for notifications, and domain pricing.
Created: 2026-05-10

---

## 1. Questions for Hazael

### Google Calendar

- ¿Qué cuenta de Google quieres usar? (probablemente la asociada a @gratia.nailart)
- ¿Calendario dedicado "Gratia Bookings" o tu calendario principal? *(Recomendado: dedicado — más limpio, fácil de compartir/dejar de compartir)*
- En cada cita en el calendario, ¿quieres que aparezca el nombre del cliente y el servicio, o solo "Cita reservada"?
- ¿Cuál es tu horario de trabajo típico? (días, horas) — esto es lo que se bloquea como "disponible"
- ¿Cuántos minutos de buffer entre citas? (limpieza, setup)
- ¿Cuántos días de anticipación máxima quieres permitir reservar? (¿1 mes? ¿3 meses?)

**Lo que necesita hacer:**
- Autorizar la app vía OAuth (un click cuando esté lista) — necesita acceso de escritura al calendario
- Si el dominio no está verificado en Google, OAuth aparecerá como "app sin verificar" hasta que lo verifiquemos

### MercadoPago

- ¿Ya tienes cuenta de MercadoPago Vendedor (México)? Si no, hay que crear una en mercadopago.com.mx
- ¿Cuenta bancaria vinculada para recibir los pagos?
- ¿RFC para facturación electrónica? (necesario para emitir facturas si lo pide el cliente)
- **Decisión clave: ¿Cuánto cobrar de anticipo por cita?**
  - Opción A: monto fijo (ej. $200 MXN)
  - Opción B: % del servicio (ej. 30%)
  - Opción C: 100% por adelantado
- **Política de cancelación/reembolso:** ¿reembolsa si cancela con 24h? ¿48h? ¿no reembolsa?
- ¿Qué métodos de pago habilitar? (tarjeta, OXXO, SPEI, MercadoCrédito)

**Lo que necesita darnos:**
- **Access Token de Producción** (Dashboard MP → Tus integraciones → Credenciales de producción)
- **Public Key de Producción**
- *(También Test Token + Test Public Key si queremos staging separado)*
- Un email para webhooks de pago

> ⚠️ Estos son secretos — debe pegarlos en el chat directo, no en email/Slack/screenshots.

---

## 2. Notification Cost Analysis

### WhatsApp (Twilio — ya está en el código)

**Pricing model (Twilio WhatsApp Business API, México):**
- Mensajes de **utilidad** (confirmaciones, recordatorios) — categoría más barata
- Conversación de 24h: **~$0.014–$0.020 USD** por conversación
- Tarifa de plataforma Twilio: **+$0.005 USD** por mensaje
- Renta de número WhatsApp Business: **~$1 USD/mo**

**Estimate for Gratia (100 citas/mes):**

| Concepto | Cálculo | Costo |
|---|---|---|
| Confirmación + recordatorio | 100 citas × 2 msgs × ~$0.025 | ~$5 USD/mo |
| Renta del número | fijo | ~$1 USD/mo |
| **Total WhatsApp** | | **~$6 USD/mo (~$120 MXN)** |

**Setup requirements:**
- Número de teléfono dedicado (Twilio compra)
- Aprobación de "Display Name" de WhatsApp Business (1–3 días, gratis)
- Aprobación de templates de utilidad (1–2 días por template, gratis)

**Alternativa más barata a futuro:** WhatsApp Business Platform directo de Meta (~$0.005/conversación) — pero más complejo de integrar. Para 100 citas/mes, los $6 de Twilio no justifican la migración.

### Email (Resend — ya está en el stack)

**Pricing:**
- **Free tier:** 3,000 emails/mes, 100/día
- **Pro:** $20 USD/mo (50,000 emails) — overkill para Gratia

**Estimate for Gratia:**
- 100 citas × 2 emails (confirmación + recordatorio) = **400 emails/mes**
- Bien dentro del free tier → **$0 USD/mo**

**Setup requirements:**
- Dominio verificado (SPF + DKIM) — depende de tener `gratianailart.com` en Cloudflare primero

### Combined notifications

| Canal | Setup | Mensual (100 citas) |
|---|---|---|
| WhatsApp (Twilio) | ~3–5 días aprobaciones | ~$120 MXN |
| Email (Resend) | ~10 min config DNS | $0 |
| **Total** | | **~$120 MXN/mo** |

---

## 3. Domain — Cloudflare Registrar

Cloudflare vende dominios al costo, sin markup.

| TLD | Precio/año | Notas |
|---|---|---|
| **gratianailart.com** | **~$10.44 USD** (~$210 MXN) | Recomendado — más barato y universal |
| gratianailart.mx | ~$30–35 USD | Solo via NIC.mx — Cloudflare no vende `.mx` directo |
| gratianailart.com.mx | ~$15–18 USD | Cloudflare a veces lo soporta — verificar |
| gratianails.com | ~$10.44 USD | Backup si `.com` está tomado |

**Incluido gratis con Cloudflare:**
- DNS hosting (global, rápido)
- SSL/TLS automático
- WHOIS privacy
- DDoS protection
- Sin upselling

**Pasos:**
1. Verificar disponibilidad en cloudflare.com → Domain Registration
2. Comprar (~5 min)
3. Apuntar DNS a Railway (CNAME del frontend)
4. Configurar SPF/DKIM/DMARC para Resend (registros TXT en Cloudflare)

**Disclaimers:**
- Precios verificados con info pública reciente — confirma en cloudflare.com antes de comprar
- Twilio WhatsApp pricing varía por país y categoría — confirma en twilio.com/whatsapp/pricing/mx

---

## 4. Total Monthly Cost — Operating Picture

Basado en 100 citas/mes:

| Item | USD/mo | MXN/mo |
|---|---|---|
| Railway (frontend + backend + Mongo) | ~$15 | ~$300 |
| WhatsApp (Twilio) | ~$6 | ~$120 |
| Email (Resend) | $0 | $0 |
| Domain (.com amortizado) | ~$0.87 | ~$17 |
| **Total infra/notifications** | **~$22 USD/mo** | **~$440 MXN/mo** |

**Cobro mensual a Hazael (Basic tier):** $1,000 MXN
**Margen estimado:** ~$560 MXN/mo (~56%)

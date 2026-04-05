# Gratia Nail Art — Google Stitch Prompts

> Prompts for generating the remaining screens in the Gratia Nail Art website.
> All screens share the same design system from the landing page (Hada del Bosque theme).
> Reference: La Pop Nails (lapopnails.mx) format — clean booking flow, service cards, mobile-first.

---

## Design System Reference (for all prompts)

- **Colors:** Dark Olive #515942 (primary), Mustard Gold #cda255 (CTAs/accents), Warm Beige #d6c9b0 (cards), Sage Green #b7bba2 (section backgrounds), Light Cream #e5e4d0 (background), Warm Brown #a18b63 (tertiary accents)
- **Typography:** Noto Serif for headlines, Manrope for body/labels
- **Style:** Enchanted forest fairy aesthetic, soft ambient shadows, no hard borders, gold accents on CTAs, dark backgrounds for hero areas, warm golden lighting feel
- **Language:** Spanish (Mexico)
- **Layout:** Mobile-first, 390px width

---

## Screen 1: Servicios (Services Page)

```
Design a mobile services page (390px wide) for "Gratia Nail Art", a nail art studio with an enchanted forest fairy aesthetic.

Color palette: Dark Olive #515942 (primary/headers), Mustard Gold #cda255 (CTAs/highlights), Warm Beige #d6c9b0 (cards), Sage Green #b7bba2 (section backgrounds), Light Cream #e5e4d0 (page background), Warm Brown #a18b63 (tertiary accents).
Typography: Noto Serif for headlines, Manrope for body text.

Page structure:
1. **Sticky nav** — Same as landing page: "Gratia Nail Art" logo left, nav links (Home, Servicios, Enseñamos, Contacto), gold "Agenda tu cita" CTA button right.

2. **Page header** — Dark olive #515942 background with subtle golden sparkle particles. Large Noto Serif headline: "Nuestros Servicios". Subtitle in Manrope: "Técnicas mixtas y nail art de autor". Soft ambient glow effect.

3. **Service category tabs** — Horizontal scrollable pill-shaped tabs: "Todo", "Nail Art", "Técnica Mixta", "Acrílico", "Gel". Active tab has gold #cda255 background with dark text, inactive tabs have beige #d6c9b0 background.

4. **Service cards grid** — 2-column grid of service cards on warm beige #d6c9b0 backgrounds with rounded corners (12px). Each card has:
   - A square thumbnail image placeholder (nail art photo) with rounded top corners
   - Service name in Manrope semibold (e.g., "Uñas Acrílicas con Nail Art")
   - Brief description in small Manrope text, 2 lines max
   - Duration indicator with clock icon: "~2 hrs"
   - Gold #cda255 "Agendar" button at the bottom
   - Soft shadow, no hard borders

   Example services:
   - "Nail Art de Autor" — Diseños únicos pintados a mano
   - "Técnica Mixta" — Combinación de técnicas para un acabado premium
   - "Acrílico Esculpido" — Extensiones de uñas esculpidas
   - "Gel con Diseño" — Acabado gel con nail art incluido
   - "Manantial Encantado" — Colección especial Hada del Bosque
   - "Retoque / Mantenimiento" — Relleno y mantenimiento de uñas

5. **CTA banner** — Full-width gold #cda255 banner: "¿Lista para transformar tus uñas?" with a "Reserva tu cita" button in dark olive #515942.

6. **Footer** — Same as landing page: Instagram + Facebook icons, @gratia.nailart, SOFTWARE BY OMNIFRACTAL, © 2026 Gratia Nail Art.

Style: Soft ambient shadows, no hard 1px borders, enchanted fairy garden mood. NO prices or costs shown anywhere on this page.
```

---

## Screen 2: Reserva — Paso 1 (Select Service)

```
Design a mobile booking step 1 page (390px wide) for "Gratia Nail Art", a nail art studio with an enchanted forest fairy aesthetic.

Color palette: Dark Olive #515942, Mustard Gold #cda255, Warm Beige #d6c9b0, Sage Green #b7bba2, Light Cream #e5e4d0, Warm Brown #a18b63.
Typography: Noto Serif for headlines, Manrope for body.

Page structure:
1. **Simplified nav** — "Gratia Nail Art" logo left, small "X" close button right that returns to home.

2. **Progress stepper** — Horizontal 4-step progress indicator at the top:
   - Step 1: "Servicio" (ACTIVE — gold #cda255 circle with number, bold text)
   - Step 2: "Fecha y Hora" (inactive — grey outline circle)
   - Step 3: "Tus Datos" (inactive)
   - Step 4: "Confirmar" (inactive)
   Connected by a thin line, gold for completed, grey for remaining.

3. **Section title** — Noto Serif headline: "Elige tu servicio". Subtitle: "Selecciona el servicio que deseas agendar."

4. **Service selection list** — Vertical list of service cards on white/cream backgrounds. Each card has:
   - Left: Small square thumbnail (nail art image)
   - Right side content:
     - Service name in Manrope semibold
     - Short description in small grey text
     - Duration with clock icon: "~2 hrs"
   - Right edge: Radio button / selection indicator
   - Selected card gets a gold #cda255 left border (3px) and subtle gold background tint

   Services listed:
   - "Nail Art de Autor" — Diseños únicos pintados a mano — ~2 hrs
   - "Técnica Mixta" — Combinación de técnicas premium — ~2.5 hrs
   - "Acrílico Esculpido" — Extensiones esculpidas — ~3 hrs
   - "Gel con Diseño" — Gel con nail art incluido — ~2 hrs
   - "Retoque / Mantenimiento" — Relleno y mantenimiento — ~1.5 hrs

5. **Bottom fixed bar** — Fixed to bottom of screen. White background with top shadow. Gold #cda255 "Siguiente" button full-width. Below it: "Paso 1 de 4" in small grey text.

Style: Clean, focused, minimal distractions. Soft shadows, no hard borders. The fairy aesthetic is present but subtle — this is a functional booking flow.
```

---

## Screen 3: Reserva — Paso 2 (Select Date & Time)

```
Design a mobile booking step 2 page (390px wide) for "Gratia Nail Art", a nail art studio with an enchanted forest fairy aesthetic.

Color palette: Dark Olive #515942, Mustard Gold #cda255, Warm Beige #d6c9b0, Sage Green #b7bba2, Light Cream #e5e4d0, Warm Brown #a18b63.
Typography: Noto Serif for headlines, Manrope for body.

Page structure:
1. **Simplified nav** — Same as step 1.

2. **Progress stepper** — Step 1 "Servicio" completed (gold filled circle with checkmark), Step 2 "Fecha y Hora" ACTIVE (gold circle), Steps 3-4 inactive.

3. **Selected service summary** — Small collapsible card at top showing: "Nail Art de Autor — ~2 hrs" with a pencil/edit icon to go back. Warm beige background.

4. **Section title** — Noto Serif headline: "Elige fecha y hora". Subtitle: "Selecciona el día y horario que prefieras."

5. **Calendar** — Monthly calendar widget for "Abril 2026".
   - Header: Left arrow, "Abril 2026" in Manrope semibold, right arrow
   - Day headers: L M M J V S D (short Spanish days)
   - Day cells: Numbers in a grid. Available days in dark text, unavailable/past days in light grey. Selected day has gold #cda255 circular background. Today has a subtle olive outline.
   - The calendar sits on a cream/white card with rounded corners and soft shadow.

6. **Time slots** — Below the calendar, horizontal scrollable row of time slot pills:
   - "10:00", "11:00", "12:00", "13:00", "15:00", "16:00", "17:00"
   - Available slots: beige #d6c9b0 background
   - Selected slot: gold #cda255 background with white text
   - Unavailable slots: light grey, slightly transparent
   - Label above: "Horarios disponibles" in small Manrope text

7. **Bottom fixed bar** — Gold "Siguiente" button, "Paso 2 de 4" text. Also a "← Anterior" text link on the left side of the bar.

Style: Clean calendar UI, fairy aesthetic through color palette only, functional and easy to read.
```

---

## Screen 4: Reserva — Paso 3 (Client Information)

```
Design a mobile booking step 3 page (390px wide) for "Gratia Nail Art", a nail art studio with an enchanted forest fairy aesthetic.

Color palette: Dark Olive #515942, Mustard Gold #cda255, Warm Beige #d6c9b0, Sage Green #b7bba2, Light Cream #e5e4d0, Warm Brown #a18b63.
Typography: Noto Serif for headlines, Manrope for body.

Page structure:
1. **Simplified nav** — Same as previous steps.

2. **Progress stepper** — Steps 1-2 completed (gold checkmarks), Step 3 "Tus Datos" ACTIVE, Step 4 inactive.

3. **Booking summary card** — Compact card showing: "Nail Art de Autor — Sáb 11 Abr, 15:00 — ~2 hrs" with edit icon. Warm beige background, rounded corners.

4. **Section title** — Noto Serif headline: "Tus datos". Subtitle: "Completa tu información para confirmar la cita."

5. **Form fields** — Clean form with floating labels, each field on a cream/white card-like container:
   - "Nombre completo" — text input
   - "Teléfono (WhatsApp)" — phone input with Mexican flag +52 prefix
   - "Instagram (opcional)" — text input with @ prefix icon
   - "Notas o referencias" — textarea, 3 lines, placeholder: "Describe el diseño que te gustaría, comparte fotos de referencia, etc."

   Input styling: Light cream #e5e4d0 background, olive #515942 text, gold #cda255 focus border/underline, Manrope font, rounded corners (8px), no harsh borders — just subtle bottom line that turns gold on focus.

6. **Reference photos upload** — A dashed-border upload area: "Sube fotos de referencia (opcional)". Icon of an image/camera. "Máximo 3 fotos" in small text. Dashed border in sage green #b7bba2.

7. **Bottom fixed bar** — Gold "Siguiente" button, "← Anterior" link, "Paso 3 de 4".

Style: Clean form design, generous spacing between fields, accessible and easy to fill on mobile.
```

---

## Screen 5: Reserva — Paso 4 (Confirmation & Payment)

```
Design a mobile booking step 4 confirmation page (390px wide) for "Gratia Nail Art", a nail art studio with an enchanted forest fairy aesthetic.

Color palette: Dark Olive #515942, Mustard Gold #cda255, Warm Beige #d6c9b0, Sage Green #b7bba2, Light Cream #e5e4d0, Warm Brown #a18b63.
Typography: Noto Serif for headlines, Manrope for body.

Page structure:
1. **Simplified nav** — Same as previous steps.

2. **Progress stepper** — Steps 1-3 completed (gold checkmarks), Step 4 "Confirmar" ACTIVE.

3. **Section title** — Noto Serif headline: "Confirma tu cita". Subtitle: "Revisa los detalles antes de confirmar."

4. **Booking summary card** — Large card on warm beige #d6c9b0 with rounded corners and soft shadow:
   - **Servicio:** "Nail Art de Autor"
   - **Fecha:** "Sábado 11 de Abril, 2026"
   - **Hora:** "3:00 PM"
   - **Duración:** "~2 horas"
   - **Nombre:** "María García"
   - **WhatsApp:** "+52 443 123 4567"
   - Each item as a row with label in small grey text and value in dark olive semibold.
   - Small "Editar" gold text link at top-right of the card.

5. **Deposit section** — Card below the summary:
   - Headline: "Apartado de cita"
   - Explanation text: "Para confirmar tu cita, se requiere un apartado que se descuenta del costo total del servicio."
   - Deposit amount shown prominently: "$200 MXN" in large gold #cda255 text
   - Small text: "Se descuenta del total de tu servicio"
   - MercadoPago logo/badge for trust

6. **Terms checkbox** — Small checkbox with text: "Acepto las políticas de cancelación y reagendamiento" with an underlined link to terms.

7. **Bottom fixed bar** — Large gold #cda255 button: "Confirmar y Pagar $200 MXN". "← Anterior" link. Secure payment icon (lock) next to button text.

Style: Clean confirmation layout, trustworthy and professional, clear hierarchy of information.
```

---

## Screen 6: Reserva Exitosa (Booking Confirmation)

```
Design a mobile booking success page (390px wide) for "Gratia Nail Art", a nail art studio with an enchanted forest fairy aesthetic.

Color palette: Dark Olive #515942, Mustard Gold #cda255, Warm Beige #d6c9b0, Sage Green #b7bba2, Light Cream #e5e4d0, Warm Brown #a18b63.
Typography: Noto Serif for headlines, Manrope for body.

Page structure:
1. **Simplified nav** — "Gratia Nail Art" logo centered.

2. **Success animation area** — Large centered section:
   - Animated gold #cda255 checkmark inside a gold circle
   - Subtle sparkle/fairy dust particles floating around it
   - Below: Noto Serif headline "¡Cita Confirmada!" in dark olive
   - Subtitle: "Tu cita ha sido agendada exitosamente" in Manrope

3. **Booking details card** — Warm beige card with all appointment details:
   - "Nail Art de Autor"
   - "Sábado 11 de Abril, 2026 — 3:00 PM"
   - "Duración: ~2 horas"
   - A small fairy mascot illustration in the corner of the card
   - "Apartado pagado: $200 MXN ✓" in green text

4. **Next steps** — Ordered list with icons:
   - 📱 "Te enviaremos confirmación por WhatsApp"
   - 📍 "Recibirás la ubicación del estudio 24 hrs antes"
   - 💅 "¡Prepárate para uñas mágicas!"

5. **Action buttons** — Two buttons stacked:
   - "Agregar a mi calendario" — Outlined button in olive green
   - "Volver al inicio" — Gold #cda255 filled button

6. **Footer** — Minimal: @gratia.nailart, SOFTWARE BY OMNIFRACTAL

Style: Celebratory but elegant, the fairy sparkle particles add magic to the success moment. Warm and inviting.
```

---

## Screen 7: Enseñamos / Jardín de las Hadas (Academy Page)

```
Design a mobile academy page (390px wide) for "Gratia Nail Art", a nail art studio with an enchanted forest fairy aesthetic. The academy is called "Jardín de las Hadas" (Garden of the Fairies).

Color palette: Dark Olive #515942, Mustard Gold #cda255, Warm Beige #d6c9b0, Sage Green #b7bba2, Light Cream #e5e4d0, Warm Brown #a18b63.
Typography: Noto Serif for headlines, Manrope for body.

Page structure:
1. **Sticky nav** — Same as landing page.

2. **Hero section** — Dark olive #515942 background with enchanted forest atmosphere. Large fairy mascot character visible. Noto Serif headline: "Jardín de las Hadas". Subtitle: "Aprende nail art con técnicas de autor". Decorative golden sparkles and leaf elements. A "Próximamente" badge in gold if not yet launched.

3. **About section** — Light cream background. Headline: "Tu camino en el nail art comienza aquí". Paragraph text about Hazael's teaching philosophy — learning nail art as an art form, not just a trade. Two-column stat boxes: "X+ Alumnas graduadas", "X Años de experiencia".

4. **Course cards** — Section title: "Nuestros Cursos". Vertical stack of course cards on warm beige backgrounds:
   - "Curso Básico — Nail Art desde Cero" — Para principiantes, aprende las bases — Icon of a paintbrush
   - "Técnica Mixta Avanzada" — Domina la combinación de técnicas — Icon of a palette
   - "Nail Art de Autor" — Crea tus propios diseños únicos — Icon of a star/wand

   Each card has: title in Manrope semibold, description, a relevant icon, and a gold "Más información" button. No prices shown.

5. **Testimonials** — Section title: "Lo que dicen nuestras alumnas". Horizontal scrollable carousel of testimonial cards with: quote text in italic Noto Serif, student name, small profile photo placeholder, star rating (5 gold stars).

6. **CTA section** — Dark olive background: "¿Quieres aprender nail art?" with a "Contáctanos por WhatsApp" gold button and a "Ver próximos cursos" outlined button.

7. **Footer** — Same as landing page.

Style: Magical and inspiring, the fairy theme is strongest on this page. It should feel like entering an enchanted garden academy.
```

---

## Screen 8: Contacto (Contact Page)

```
Design a mobile contact page (390px wide) for "Gratia Nail Art", a nail art studio with an enchanted forest fairy aesthetic.

Color palette: Dark Olive #515942, Mustard Gold #cda255, Warm Beige #d6c9b0, Sage Green #b7bba2, Light Cream #e5e4d0, Warm Brown #a18b63.
Typography: Noto Serif for headlines, Manrope for body.

Page structure:
1. **Sticky nav** — Same as landing page.

2. **Page header** — Dark olive #515942 background with subtle golden accents. Noto Serif headline: "Contacto". Subtitle: "¿Tienes preguntas? Estamos para ayudarte."

3. **Contact methods** — Three horizontal cards in a row (or stacked on narrow mobile):
   - **WhatsApp** — Green WhatsApp icon, "Escríbenos", phone number. Gold "Abrir WhatsApp" button.
   - **Instagram** — Instagram gradient icon, "@gratia.nailart", "Síguenos y escríbenos por DM". Gold "Ir a Instagram" button.
   - **Facebook** — Facebook blue icon, "Gratia Nail Art", "Visita nuestra página". Gold "Ir a Facebook" button.

4. **Contact form** — Section title: "Envíanos un mensaje". Simple form on a warm beige card:
   - "Nombre" — text input
   - "WhatsApp o Email" — text input
   - "Mensaje" — textarea, 4 lines
   - Gold "Enviar mensaje" button
   - Input styling: cream backgrounds, gold focus borders, Manrope font.

5. **Location section** — Section title: "Ubicación".
   - "Morelia, Michoacán, México" in text
   - A decorative map placeholder (illustrated/stylized, not a Google Map embed — for the prototype)
   - Note: "La dirección exacta se comparte al confirmar tu cita" in small italic text.

6. **Business hours** — Simple list on sage green #b7bba2 background card:
   - "Horario de Atención"
   - Lunes a Viernes: 10:00 — 19:00
   - Sábado: 10:00 — 15:00
   - Domingo: Cerrado

7. **Footer** — Same as landing page.

Style: Warm, approachable, easy to find contact info at a glance. Professional but personal.
```

---

## Screen 9: Gratia Nail Shop (Product Store — Future)

```
Design a mobile nail shop page (390px wide) for "Gratia Nail Shop", the e-commerce sub-brand of Gratia Nail Art, with an enchanted forest fairy aesthetic.

Color palette: Dark Olive #515942, Mustard Gold #cda255, Warm Beige #d6c9b0, Sage Green #b7bba2, Light Cream #e5e4d0, Warm Brown #a18b63.
Typography: Noto Serif for headlines, Manrope for body.

Page structure:
1. **Sticky nav** — Same as main site but with "Gratia Nail Shop" sub-brand indicator.

2. **Hero banner** — Warm beige #d6c9b0 background. Noto Serif headline: "Gratia Nail Shop". Subtitle: "Productos con diseños mágicos de Gratia" in Manrope. A "Próximamente" badge overlay in gold since this is a future feature.

3. **Category filters** — Horizontal scrollable pills: "Todo", "Prensa-On", "Accesorios", "Kits", "Colecciones". Same styling as service tabs.

4. **Product grid** — 2-column grid of product cards:
   - Square product image placeholder with rounded corners
   - Product name: "Press-On Manantial Encantado"
   - Small description: "Set de 10 uñas prensa-on"
   - Price: "$350 MXN" in gold #cda255 text
   - "Comprar" gold button
   - Soft shadow cards on cream background

   Example products:
   - "Press-On Manantial Encantado" — Set de 10 uñas
   - "Press-On Ópalo Místico" — Set de 10 uñas
   - "Kit Hada del Bosque" — Kit completo de decoración
   - "Accesorios Mágicos" — Charms y decoraciones

5. **Footer** — Same as main site.

Style: E-commerce layout but maintaining the fairy enchanted aesthetic. Products feel magical, not generic. This is a preview/coming soon page.
```

---

## Notes for Stitch

- All screens should use the **same design system** created for the landing page
- Maintain the **Stitch project ID:** `1318442603202433328`
- The fairy mascot character should appear subtly across pages (not just landing)
- Test all screens at **390px** (mobile-first) — desktop can be adapted later
- Keep consistent nav and footer across all pages

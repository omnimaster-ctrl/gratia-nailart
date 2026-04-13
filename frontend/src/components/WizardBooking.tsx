import { useState, useEffect, useCallback } from 'react'
import { type FormData, initialFormData, validateStep, services, buildTimeSlots, minSelectableDateMX, AM_BLOCK, PM_BLOCK, SAT_BLOCK } from './booking/bookingLogic'

const API = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
const DEPOSIT_MXN = 250

export default function WizardBooking() {
  const [step, setStep] = useState(1)
  const [form, setForm] = useState<FormData>(initialFormData)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [bookedTimes, setBookedTimes] = useState<string[]>([])
  const [fullyBookedDates, setFullyBookedDates] = useState<string[]>([])
  const [isLoadingAvail, setIsLoadingAvail] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [showPolicies, setShowPolicies] = useState(false)
  const [couponStatus, setCouponStatus] = useState({ loading: false, error: '', success: '' })

  // Persist form data
  useEffect(() => { localStorage.setItem('gratia_wizard', JSON.stringify(form)) }, [form])
  useEffect(() => {
    const saved = localStorage.getItem('gratia_wizard')
    if (saved) { try { setForm(prev => ({ ...prev, ...JSON.parse(saved) })) } catch {} }
  }, [])

  // Fetch available dates on mount
  useEffect(() => {
    fetch(`${API}/api/available-dates`).then(r => r.ok ? r.json() : null).then(d => {
      if (d?.available_dates) setFullyBookedDates(d.available_dates.filter((x: any) => !x.is_available).map((x: any) => x.date))
    }).catch(() => {})
  }, [])

  // Fetch availability when date changes
  useEffect(() => {
    if (!form.appointmentDate) return
    setIsLoadingAvail(true)
    setForm(p => ({ ...p, appointmentTime: '' }))
    fetch(`${API}/api/available-times/${form.appointmentDate}`).then(r => r.ok ? r.json() : null).then(d => {
      setBookedTimes(d?.booked_times || [])
    }).catch(() => {}).finally(() => setIsLoadingAvail(false))
  }, [form.appointmentDate])

  const set = useCallback((field: string, value: any) => {
    if (field === 'appointmentDate' && fullyBookedDates.includes(value)) {
      setErrors(p => ({ ...p, appointmentDate: 'Fecha completamente reservada.' }))
      return
    }
    setForm(p => ({ ...p, [field]: value }))
    if (errors[field]) setErrors(p => ({ ...p, [field]: '' }))

    if ((field === 'serviceType' && value) || field === 'retiroMaterial') {
      const svc = field === 'serviceType' ? value : form.serviceType
      const retiro = field === 'retiroMaterial' ? value : form.retiroMaterial
      if (svc) {
        const sub = (services[svc]?.price || 0) + (retiro ? 150 : 0)
        setForm(p => ({ ...p, [field]: value, anticipoAmount: DEPOSIT_MXN, subtotal: sub, total: sub, remainingAmount: Math.max(0, sub - DEPOSIT_MXN), discount: 0, appliedCoupon: null, couponCode: '' }))
        setCouponStatus({ loading: false, error: '', success: '' })
      }
    }
  }, [form.serviceType, form.retiroMaterial, errors, fullyBookedDates])

  const next = () => { const e = validateStep(step, form); setErrors(e); if (Object.keys(e).length === 0) { let n = step + 1; if (form.isReturningClient && n === 2) n = 3; if (form.isReturningClient && n === 4) n = 5; setStep(Math.min(n, 6)) } }
  const prev = () => { let n = step - 1; if (form.isReturningClient && n === 4) n = 3; if (form.isReturningClient && n === 2) n = 1; setStep(Math.max(n, 1)) }

  const handlePayment = async () => {
    const e = validateStep(5, form); setErrors(e); if (Object.keys(e).length > 0) return
    setIsProcessing(true)
    try {
      const digits = form.phone.replace(/\D/g, '').slice(0, 10)
      const phone = `+521${digits}`
      const schedule = `${form.appointmentTime} - ${parseInt(form.appointmentTime.split(':')[0]) + 2}:${form.appointmentTime.split(':')[1]}`
      const res = await fetch(`${API}/api/create-mercadopago-preference`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ appointment_data: { name: form.name, phone, service: form.serviceType, date: form.appointmentDate, schedule, time: form.appointmentTime, aceptaPoliticas: true, currentNailsImages: form.currentNailImages, retiro: form.retiroMaterial, tieneIdeas: form.hasDesignIdeas, imagenes: form.designImages, libertadArtistica: form.freeDesign, notes: form.favoriteSnacks ? `Snacks: ${form.favoriteSnacks}, Bebidas: ${form.favoriteDrinks}` : null, favoriteSnacks: form.favoriteSnacks || null, favoriteDrinks: form.favoriteDrinks || null, favoriteMovie: form.favoriteMovie || null, favoriteSeries: form.favoriteSeries || null, favoriteMusic: form.favoriteMusic || null, birthday: form.birthday || null }, customer_email: form.email }),
      })
      const data = await res.json()
      if (res.ok && data.checkout_url) { localStorage.removeItem('gratia_wizard'); window.location.href = data.checkout_url }
      else { alert(`Error: ${data.detail || 'Intenta de nuevo'}`); setIsProcessing(false) }
    } catch { alert('Error de conexión.'); setIsProcessing(false) }
  }

  const applyCoupon = async () => {
    if (!form.couponCode.trim()) { setCouponStatus({ loading: false, error: 'Ingresa un código', success: '' }); return }
    setCouponStatus({ loading: true, error: '', success: '' })
    try {
      const r = await fetch(`${API}/api/validate-coupon`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ coupon_code: form.couponCode, service_type: form.serviceType, service_price: form.subtotal }) })
      const d = await r.json()
      if (r.ok && d.valid) {
        const disc = d.discount_amount; const tot = Math.max(0, form.subtotal - disc); const dep = d.waive_deposit ? 0 : DEPOSIT_MXN
        setForm(p => ({ ...p, appliedCoupon: d, discount: disc, total: tot, anticipoAmount: dep, remainingAmount: Math.max(0, tot - dep), waiveDeposit: d.waive_deposit }))
        setCouponStatus({ loading: false, error: '', success: d.waive_deposit ? '¡Código VIP aplicado!' : `¡Cupón aplicado! -$${disc} MXN` })
      } else { setCouponStatus({ loading: false, error: d.message || 'Código inválido', success: '' }) }
    } catch { setCouponStatus({ loading: false, error: 'Error al validar.', success: '' }) }
  }

  const timeSlots = form.serviceType && form.appointmentDate ? buildTimeSlots(form.appointmentDate) : null
  const stepLabels = ['Tus datos', 'Ficha clínica', 'Fecha y Servicio', 'Tus preferencias', 'Anticipo', 'Confirmación']
  const totalSteps = form.isReturningClient ? 4 : 6
  const displayStep = form.isReturningClient ? [0, 1, 1, 2, 2, 3, 4][step] : step

  // ── Shared styles ──
  const inp = 'w-full px-4 py-3 rounded-xl border-2 border-outline/40 bg-surface-bright font-body text-on-background focus:border-gold focus:ring-2 focus:ring-gold/20 focus:outline-none transition-all'
  const errCls = 'border-red-400 bg-red-50'
  const label = 'block font-label font-semibold text-on-background mb-1.5 text-sm'
  const errMsg = 'text-red-500 text-xs mt-1'

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Header */}
      <div className="bg-dark-deepest rounded-t-3xl p-6 text-center shadow-lg">
        <h1 className="font-headline text-3xl md:text-4xl text-gold italic">Agenda tu Cita</h1>
        <div className="mt-4">
          <div className="h-1.5 bg-dark-muted/30 rounded-full overflow-hidden"><div className="h-full bg-gradient-to-r from-gold-dim to-gold rounded-full transition-all duration-500" style={{ width: `${(displayStep / totalSteps) * 100}%` }} /></div>
          <p className="text-dark-muted font-body text-sm mt-2">Paso {displayStep} de {totalSteps} — {stepLabels[step - 1]}</p>
        </div>
      </div>

      {/* Content */}
      <div className="bg-light-cream rounded-b-3xl shadow-xl p-6 md:p-8 border border-gold/10">

        {/* ── STEP 1: Personal Data ── */}
        {step === 1 && (
          <div className="space-y-5">
            <div><h2 className="font-headline text-2xl text-dark-deepest italic">Tus Datos</h2><p className="text-on-surface-variant font-body text-sm mt-1">Cuéntanos quién eres para personalizar tu experiencia</p></div>
            {form.isReturningClient && <div className="flex items-center gap-3 p-4 bg-green-50 rounded-xl border border-green-200"><span className="text-2xl">🎉</span><div><h3 className="font-semibold text-green-800 text-sm">¡Bienvenido de vuelta!</h3><p className="text-green-600 text-xs">Autocompletamos tus datos</p></div></div>}
            <div><label className={label}>Nombre completo *</label><input className={`${inp} ${errors.name ? errCls : ''}`} value={form.name} onChange={e => set('name', e.target.value)} placeholder="Tu nombre completo" />{errors.name && <span className={errMsg}>{errors.name}</span>}</div>
            <div><label className={label}>Email *</label><input type="email" className={`${inp} ${errors.email ? errCls : ''}`} value={form.email} onChange={e => set('email', e.target.value)} placeholder="tu@email.com" />{errors.email && <span className={errMsg}>{errors.email}</span>}</div>
            <div><label className={label}>Teléfono *</label><div className="flex gap-2"><select className="w-24 px-2 py-3 rounded-xl border-2 border-outline/40 bg-surface-bright font-body text-sm" value={form.countryCode} onChange={e => set('countryCode', e.target.value)}><option value="+52">🇲🇽 +52</option><option value="+1">🇺🇸 +1</option></select><input type="tel" className={`${inp} flex-1 ${errors.phone ? errCls : ''}`} value={form.phone} onChange={e => set('phone', e.target.value.replace(/\D/g, ''))} placeholder="10 dígitos" maxLength={10} /></div>{errors.phone && <span className={errMsg}>{errors.phone}</span>}</div>
          </div>
        )}

        {/* ── STEP 2: Clinical Form ── */}
        {step === 2 && (
          <div className="space-y-5">
            <div><h2 className="font-headline text-2xl text-dark-deepest italic">Ficha Clínica</h2><p className="text-on-surface-variant font-body text-sm mt-1">Para brindarte un servicio seguro</p></div>
            {[{ key: 'hasAllergies', detail: 'allergiesDetails', label: 'Tengo alergias a productos para uñas', ph: 'Describe tus alergias...' }, { key: 'hasSkinConditions', detail: 'skinConditionsDetails', label: 'Tengo condiciones de piel en manos/uñas', ph: 'Describe la condición...' }, { key: 'hasMedicalConditions', detail: 'medicalConditionsDetails', label: 'Tengo condiciones médicas relevantes', ph: 'Describe la condición médica...' }, { key: 'takingMedications', detail: 'medicationsDetails', label: 'Estoy tomando medicamentos actualmente', ph: 'Menciona los medicamentos...' }].map(({ key, detail, label: lbl, ph }) => (
              <div key={key} className="p-4 bg-warm-beige/50 rounded-xl">
                <label className="flex items-start gap-3 cursor-pointer"><input type="checkbox" className="mt-1 accent-gold w-4 h-4" checked={(form as any)[key]} onChange={e => set(key, e.target.checked)} /><span className="font-body text-sm text-dark-deeper">{lbl}</span></label>
                {(form as any)[key] && <textarea className={`${inp} mt-3 ${(errors as any)[detail] ? errCls : ''}`} rows={2} placeholder={ph} value={(form as any)[detail]} onChange={e => set(detail, e.target.value)} />}
                {(errors as any)[detail] && <span className={errMsg}>{(errors as any)[detail]}</span>}
              </div>
            ))}
            <div className="p-3 bg-gold/10 rounded-lg text-sm text-dark-deeper font-body"><span className="mr-1">💅</span>Esta información es confidencial y nos ayuda a cuidar tu salud.</div>
          </div>
        )}

        {/* ── STEP 3: Service & Date/Time ── */}
        {step === 3 && (
          <div className="space-y-5">
            <div><h2 className="font-headline text-2xl text-dark-deepest italic">Fecha y Servicio</h2><p className="text-on-surface-variant font-body text-sm mt-1">Selecciona tu servicio y programa tu cita</p></div>
            <div><label className={label}>Tipo de servicio *</label><div className="grid gap-3">{Object.entries(services).map(([k, s]) => (<div key={k} onClick={() => set('serviceType', k)} className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${form.serviceType === k ? 'border-gold bg-gold/10 shadow-md' : 'border-outline/30 bg-surface-bright hover:border-gold/50 hover:-translate-y-0.5'}`}><h3 className="font-headline text-base text-dark-deepest font-bold">{s.name}</h3><p className="text-on-surface-variant text-xs font-body mt-1">{s.description}</p><div className="flex justify-between mt-2 text-sm"><span className="font-bold text-gold">${s.price} MXN</span><span className="text-on-surface-variant">{s.duration_range}</span></div></div>))}</div>{errors.serviceType && <span className={errMsg}>{errors.serviceType}</span>}</div>

            {form.serviceType && (<>
              <div className="flex items-center justify-between p-3 bg-warm-beige/60 rounded-xl"><span className="font-body text-sm font-semibold text-dark-deeper">¿Retiro de material?</span><div className="flex gap-2">{[false, true].map(v => (<button key={String(v)} onClick={() => set('retiroMaterial', v)} className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${form.retiroMaterial === v ? 'bg-gold text-dark-deepest' : 'bg-white border border-outline/30 text-on-surface-variant hover:border-gold'}`}>{v ? 'Sí' : 'No'}</button>))}</div></div>
              {form.retiroMaterial && <div className="p-2 bg-amber-50 border-l-3 border-amber-400 rounded text-xs text-amber-800"><strong>Nota:</strong> El retiro tiene un costo de $150 MXN.</div>}
            </>)}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div><label className={label}>Fecha *</label><input type="date" className={`${inp} ${errors.appointmentDate ? errCls : ''}`} value={form.appointmentDate} onChange={e => set('appointmentDate', e.target.value)} min={minSelectableDateMX()} />{errors.appointmentDate && <span className={errMsg}>{errors.appointmentDate}</span>}<p className="text-xs text-on-surface-variant mt-1">📅 Agenda con <strong>2 días de anticipación</strong>. Lun-Sáb.</p></div>
              <div><label className={label}>Hora *</label>
                {isLoadingAvail ? <p className="text-sm text-on-surface-variant py-3">Verificando disponibilidad...</p> : timeSlots && timeSlots.available ? (
                  <div className="space-y-3">
                    {timeSlots.morning.length > 0 && <div><h4 className="text-xs font-bold text-on-surface-variant mb-1">{AM_BLOCK.label}</h4><div className="flex flex-wrap gap-1.5">{timeSlots.morning.map(s => { const booked = bookedTimes.includes(s.value); return <button key={s.value} disabled={booked} onClick={() => set('appointmentTime', s.value)} className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${form.appointmentTime === s.value ? 'bg-gold text-dark-deepest shadow' : booked ? 'bg-gray-100 text-gray-400 line-through cursor-not-allowed' : 'bg-white border border-outline/30 hover:border-gold text-dark-deeper'}`}>{s.display}</button> })}</div></div>}
                    {timeSlots.afternoon.length > 0 && <div><h4 className="text-xs font-bold text-on-surface-variant mb-1">{PM_BLOCK.label}</h4><div className="flex flex-wrap gap-1.5">{timeSlots.afternoon.map(s => { const booked = bookedTimes.includes(s.value); return <button key={s.value} disabled={booked} onClick={() => set('appointmentTime', s.value)} className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${form.appointmentTime === s.value ? 'bg-gold text-dark-deepest shadow' : booked ? 'bg-gray-100 text-gray-400 line-through cursor-not-allowed' : 'bg-white border border-outline/30 hover:border-gold text-dark-deeper'}`}>{s.display}</button> })}</div></div>}
                    {timeSlots.saturday.length > 0 && <div><h4 className="text-xs font-bold text-on-surface-variant mb-1">{SAT_BLOCK.label}</h4><div className="flex flex-wrap gap-1.5">{timeSlots.saturday.map(s => { const booked = bookedTimes.includes(s.value); return <button key={s.value} disabled={booked} onClick={() => set('appointmentTime', s.value)} className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${form.appointmentTime === s.value ? 'bg-gold text-dark-deepest shadow' : booked ? 'bg-gray-100 text-gray-400 line-through cursor-not-allowed' : 'bg-white border border-outline/30 hover:border-gold text-dark-deeper'}`}>{s.display}</button> })}</div></div>}
                  </div>
                ) : form.appointmentDate ? <p className="text-sm text-red-500 py-2">No hay disponibilidad para esta fecha.</p> : <p className="text-sm text-on-surface-variant py-2">Selecciona una fecha primero.</p>}
                {errors.appointmentTime && <span className={errMsg}>{errors.appointmentTime}</span>}
              </div>
            </div>

            <div className="space-y-3">
              <label className="flex items-center gap-3 cursor-pointer"><input type="checkbox" className="accent-gold w-4 h-4" checked={form.hasDesignIdeas} onChange={e => set('hasDesignIdeas', e.target.checked)} /><span className="font-body text-sm">¿Tienes ideas de diseño?</span></label>
              <label className="flex items-center gap-3 cursor-pointer"><input type="checkbox" className="accent-gold w-4 h-4" checked={form.freeDesign} onChange={e => set('freeDesign', e.target.checked)} /><span className="font-body text-sm">Diseño libre por el nail artist</span></label>
            </div>
          </div>
        )}

        {/* ── STEP 4: Preferences ── */}
        {step === 4 && (
          <div className="space-y-5">
            <div><h2 className="font-headline text-2xl text-dark-deepest italic">Tus Preferencias</h2><p className="text-on-surface-variant font-body text-sm mt-1">Para hacer tu visita más placentera</p></div>
            <div className="bg-warm-beige/50 p-5 rounded-xl space-y-4">
              <div><label className={label}>Snacks favoritos</label><input className={inp} value={form.favoriteSnacks} onChange={e => set('favoriteSnacks', e.target.value)} placeholder="Galletas, fruta, chocolates..." /></div>
              <div><label className={label}>Bebidas preferidas</label><input className={inp} value={form.favoriteDrinks} onChange={e => set('favoriteDrinks', e.target.value)} placeholder="Café, té, jugos..." /></div>
              <label className="flex items-center gap-3 cursor-pointer"><input type="checkbox" className="accent-gold w-4 h-4" checked={form.indifferentToFood} onChange={e => set('indifferentToFood', e.target.checked)} /><span className="font-body text-sm">Sin preferencias especiales</span></label>
              <div><label className={label}>Fecha de cumpleaños</label><input type="date" className={inp} value={form.birthday} onChange={e => set('birthday', e.target.value)} /><p className="text-xs text-on-surface-variant mt-1">Queremos celebrar contigo 🎉</p></div>
              <div className="border-t border-outline/20 pt-4 space-y-3"><h3 className="font-headline text-lg text-dark-deeper">Entretenimiento</h3><div className="grid grid-cols-1 md:grid-cols-2 gap-3"><div><label className={label}>Película favorita</label><input className={inp} value={form.favoriteMovie} onChange={e => set('favoriteMovie', e.target.value)} /></div><div><label className={label}>Serie preferida</label><input className={inp} value={form.favoriteSeries} onChange={e => set('favoriteSeries', e.target.value)} /></div></div><div><label className={label}>Género musical</label><input className={inp} value={form.favoriteMusic} onChange={e => set('favoriteMusic', e.target.value)} placeholder="Pop, rock, reggaeton..." /></div></div>
            </div>
          </div>
        )}

        {/* ── STEP 5: Payment Summary ── */}
        {step === 5 && (
          <div className="space-y-5">
            <div><h2 className="font-headline text-2xl text-dark-deepest italic">Anticipo</h2><p className="text-on-surface-variant font-body text-sm mt-1">Revisa los detalles y procede al pago</p></div>
            <div className="bg-warm-beige/50 p-5 rounded-xl space-y-3 text-sm font-body">
              <h3 className="font-headline text-lg text-dark-deeper border-b border-outline/20 pb-2">Resumen</h3>
              <div className="flex justify-between"><span>Nombre:</span><span className="font-semibold">{form.name}</span></div>
              <div className="flex justify-between"><span>Servicio:</span><span className="font-semibold">{services[form.serviceType]?.name}</span></div>
              <div className="flex justify-between"><span>Fecha:</span><span className="font-semibold">{form.appointmentDate && new Date(form.appointmentDate + 'T12:00:00').toLocaleDateString('es-MX', { weekday: 'long', day: 'numeric', month: 'long' })}</span></div>
              <div className="flex justify-between"><span>Hora:</span><span className="font-semibold">{form.appointmentTime}</span></div>
              <div className="border-t border-outline/20 pt-3 space-y-2">
                <div className="flex justify-between"><span>Servicio:</span><span>${services[form.serviceType]?.price || 0} MXN</span></div>
                {form.retiroMaterial && <div className="flex justify-between"><span>Retiro material:</span><span>+$150 MXN</span></div>}
                {form.appliedCoupon && <div className="flex justify-between text-green-600"><span>Descuento:</span><span>-${form.discount} MXN</span></div>}
                <div className="flex justify-between font-bold text-base"><span>Total:</span><span>${form.total || form.subtotal || services[form.serviceType]?.price || 0} MXN</span></div>
                <div className="flex justify-between bg-gold/15 p-2 rounded-lg font-bold text-gold"><span>Anticipo hoy:</span><span>${form.anticipoAmount || DEPOSIT_MXN} MXN</span></div>
                <div className="flex justify-between text-xs"><span>Restante el día de tu cita:</span><span>${form.remainingAmount >= 0 ? form.remainingAmount : 0} MXN</span></div>
              </div>
            </div>

            {/* Coupon */}
            <div className="p-4 bg-warm-beige/30 rounded-xl">
              <h3 className="font-headline text-sm text-dark-deeper mb-2">¿Tienes un cupón?</h3>
              {!form.appliedCoupon ? <div className="flex gap-2"><input className={`${inp} flex-1`} value={form.couponCode} onChange={e => set('couponCode', e.target.value.toUpperCase())} placeholder="Código" /><button onClick={applyCoupon} disabled={couponStatus.loading} className="px-4 py-2 bg-gold text-dark-deepest rounded-xl font-bold text-sm hover:brightness-110 transition-all disabled:opacity-50">{couponStatus.loading ? '...' : 'Aplicar'}</button></div>
              : <div className="flex items-center justify-between"><span className="text-green-600 text-sm font-semibold">✅ {form.appliedCoupon.code} aplicado</span><button onClick={() => { setForm(p => ({ ...p, couponCode: '', appliedCoupon: null, discount: 0, total: p.subtotal, anticipoAmount: DEPOSIT_MXN, remainingAmount: Math.max(0, p.subtotal - DEPOSIT_MXN) })); setCouponStatus({ loading: false, error: '', success: '' }) }} className="text-xs text-red-500 underline">Remover</button></div>}
              {couponStatus.error && <p className="text-red-500 text-xs mt-1">❌ {couponStatus.error}</p>}
              {couponStatus.success && <p className="text-green-600 text-xs mt-1">✅ {couponStatus.success}</p>}
            </div>

            {/* Policies */}
            <div className="flex items-start gap-2">
              <input type="checkbox" className="mt-1 accent-gold w-4 h-4" checked={form.acceptPolicies} onChange={e => set('acceptPolicies', e.target.checked)} />
              <span className="text-sm font-body">Acepto las <button type="button" onClick={() => setShowPolicies(true)} className="text-gold underline font-semibold">políticas del estudio</button> *</span>
            </div>
            {errors.acceptPolicies && <span className={errMsg}>{errors.acceptPolicies}</span>}

            {/* Pay Button */}
            <div className="text-center">
              <div className="flex justify-between items-center mb-3 text-lg"><span className="font-body">Total a pagar ahora:</span><span className="font-bold text-gold text-xl">${form.anticipoAmount || DEPOSIT_MXN} MXN</span></div>
              <button onClick={handlePayment} disabled={isProcessing || !form.acceptPolicies} className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-gold-dim to-gold text-dark-deepest font-label font-bold text-base uppercase tracking-wide shadow-lg hover:brightness-110 hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed">{isProcessing ? 'Procesando...' : 'Pagar Anticipo y Confirmar Cita'}</button>
              {!form.acceptPolicies && <p className="text-xs text-red-500 mt-2">Debes aceptar las políticas para continuar</p>}
            </div>
          </div>
        )}

        {/* ── STEP 6: Confirmation ── */}
        {step === 6 && (
          <div className="text-center py-12 space-y-4">
            <div className="text-5xl">⏳</div>
            <h2 className="font-headline text-2xl text-dark-deepest italic">Redirigiendo a Mercado Pago...</h2>
            <p className="text-on-surface-variant font-body text-sm">Si no eres redirigido automáticamente, espera unos segundos.</p>
          </div>
        )}

        {/* ── Navigation ── */}
        {step < 6 && (
          <div className="flex justify-between items-center mt-8 pt-5 border-t border-outline/20">
            {step > 1 ? <button onClick={prev} className="px-5 py-2.5 rounded-xl border-2 border-gold/40 text-dark-deepest font-label font-bold text-sm uppercase hover:bg-gold/10 transition-colors">← Atrás</button> : <div />}
            {step < 5 && <button onClick={next} className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-gold-dim to-gold text-dark-deepest font-label font-bold text-sm uppercase shadow-md hover:brightness-110 hover:-translate-y-0.5 transition-all">Siguiente →</button>}
          </div>
        )}
      </div>

      {/* ── Policies Modal ── */}
      {showPolicies && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" onClick={() => setShowPolicies(false)}>
          <div className="bg-light-cream rounded-2xl max-w-lg w-full max-h-[80vh] overflow-y-auto shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center p-5 border-b border-outline/20"><h3 className="font-headline text-xl text-dark-deepest italic">Políticas del Estudio</h3><button onClick={() => setShowPolicies(false)} className="text-2xl text-on-surface-variant hover:text-dark-deepest">×</button></div>
            <div className="p-5 space-y-3 text-sm font-body text-dark-deeper leading-relaxed">
              <p><strong>Revisa mi trabajo antes de agendar</strong> para confirmar que mi estilo es lo que buscas.</p>
              <p><strong>No hago retoques de otros salones.</strong> Haré retiro de lo que traigas (con costo extra) y colocaremos producto nuevo.</p>
              <p><strong>Tolerancia de 15 minutos.</strong> Pasado este tiempo, se reagendará tu cita.</p>
              <p><strong>El anticipo no es reembolsable</strong> si cancelas el mismo día o cancelas en más de dos ocasiones.</p>
              <p><strong>Tómate tu tiempo:</strong> cada servicio requiere su espacio, ven sin prisas.</p>
            </div>
            <div className="p-5 border-t border-outline/20"><button onClick={() => { set('acceptPolicies', true); setShowPolicies(false) }} className="w-full py-3 rounded-xl bg-gold text-dark-deepest font-label font-bold uppercase hover:brightness-110 transition-all">Acepto las Políticas</button></div>
          </div>
        </div>
      )}
    </div>
  )
}

import { DateTime } from 'luxon'

const TZ = 'America/Mexico_City'

// ── Services ──
export const services: Record<string, { name: string; price: number; duration: number; duration_range: string; description: string }> = {
  'Técnica Mixta': {
    name: 'Técnica Mixta',
    price: 500,
    duration: 180,
    duration_range: '3h',
    description: 'Combinación de técnicas para un resultado único y personalizado',
  },
  'Nail Art Completo': {
    name: 'Nail Art Completo',
    price: 700,
    duration: 240,
    duration_range: '4h',
    description: 'Diseño artístico completo con las técnicas más avanzadas',
  },
  'Retoque / Mantenimiento': {
    name: 'Retoque / Mantenimiento',
    price: 400,
    duration: 120,
    duration_range: '2h',
    description: 'Mantenimiento y retoque de tu diseño para mantenerlo impecable',
  },
}

// ── Time blocks ──
export const AM_BLOCK = { start: '09:00', end: '13:00', label: 'Mañana (9–13)' }
export const PM_BLOCK = { start: '16:00', end: '19:00', label: 'Tarde (16–19)' }
export const SAT_BLOCK = { start: '10:00', end: '12:00', label: 'Sábado (10–12)' }
const STEP_MIN = 30

// ── Date helpers ──
export const isWeekendMX = (d: string) => DateTime.fromISO(d, { zone: TZ }).set({ hour: 12 }).weekday === 7
export const isBusinessDayMX = (d: string) => { const w = DateTime.fromISO(d, { zone: TZ }).set({ hour: 12 }).weekday; return w >= 1 && w <= 6 }
export const isSaturdayMX = (d: string) => DateTime.fromISO(d, { zone: TZ }).set({ hour: 12 }).weekday === 6

export const minSelectableDateMX = () => {
  let min = DateTime.now().setZone(TZ).plus({ hours: 48 }).startOf('day')
  if (min.weekday === 7) min = min.plus({ days: 1 })
  return min.toISODate()!
}

export const validateAppointmentDate = (date: string) => {
  if (!date || !isBusinessDayMX(date)) return false
  const sel = DateTime.fromISO(date, { zone: TZ }).startOf('day')
  const min = DateTime.fromISO(minSelectableDateMX(), { zone: TZ }).startOf('day')
  return sel >= min
}

export const deriveSchedule = (time: string) => {
  const h = parseInt(time.split(':')[0], 10)
  return h >= 16 && h <= 19 ? 'afternoon' : 'morning'
}

// ── Slot generation ──
function slotsFromBlock(date: string, block: { start: string; end: string }, step: number) {
  const start = DateTime.fromISO(`${date}T${block.start}`, { zone: TZ })
  const end = DateTime.fromISO(`${date}T${block.end}`, { zone: TZ })
  const slots: { value: string; display: string }[] = []
  let cur = start
  while (cur <= end.minus({ minutes: step })) {
    slots.push({ value: cur.toFormat('HH:mm'), display: cur.toFormat('h:mm a') })
    cur = cur.plus({ minutes: step })
  }
  return slots
}

export function buildTimeSlots(date: string) {
  if (!date || !isBusinessDayMX(date) || !validateAppointmentDate(date))
    return { morning: [] as ReturnType<typeof slotsFromBlock>, afternoon: [] as ReturnType<typeof slotsFromBlock>, saturday: [] as ReturnType<typeof slotsFromBlock>, available: false }

  if (isSaturdayMX(date)) {
    const sat = slotsFromBlock(date, SAT_BLOCK, STEP_MIN)
    return { morning: [], afternoon: [], saturday: sat, available: sat.length > 0 }
  }
  const m = slotsFromBlock(date, AM_BLOCK, STEP_MIN)
  const a = slotsFromBlock(date, PM_BLOCK, STEP_MIN)
  return { morning: m, afternoon: a, saturday: [], available: m.length > 0 || a.length > 0 }
}

// ── Form types ──
export type ImageFile = { name: string; data: string; size: number }

export type FormData = {
  name: string; email: string; phone: string; countryCode: string
  currentNailImages: ImageFile[]; isReturningClient: boolean
  hasAllergies: boolean; allergiesDetails: string
  hasSkinConditions: boolean; skinConditionsDetails: string
  hasMedicalConditions: boolean; medicalConditionsDetails: string
  takingMedications: boolean; medicationsDetails: string
  serviceType: string; appointmentDate: string; appointmentTime: string
  hasDesignIdeas: boolean; designImages: ImageFile[]; freeDesign: boolean
  retiroMaterial: boolean
  favoriteSnacks: string; favoriteDrinks: string; favoriteMovie: string
  favoriteSeries: string; favoriteMusic: string; birthday: string
  indifferentToFood: boolean
  acceptPolicies: boolean; paymentMethod: string; anticipoAmount: number
  couponCode: string; appliedCoupon: any; subtotal: number
  discount: number; total: number; remainingAmount: number
  creditAmount?: number; waiveDeposit?: boolean
}

export const initialFormData: FormData = {
  name: '', email: '', phone: '', countryCode: '+52',
  currentNailImages: [], isReturningClient: false,
  hasAllergies: false, allergiesDetails: '',
  hasSkinConditions: false, skinConditionsDetails: '',
  hasMedicalConditions: false, medicalConditionsDetails: '',
  takingMedications: false, medicationsDetails: '',
  serviceType: '', appointmentDate: '', appointmentTime: '',
  hasDesignIdeas: false, designImages: [], freeDesign: false,
  retiroMaterial: false,
  favoriteSnacks: '', favoriteDrinks: '', favoriteMovie: '',
  favoriteSeries: '', favoriteMusic: '', birthday: '',
  indifferentToFood: false,
  acceptPolicies: false, paymentMethod: 'mercadopago', anticipoAmount: 0,
  couponCode: '', appliedCoupon: null, subtotal: 0,
  discount: 0, total: 0, remainingAmount: 0,
}

// ── Validation ──
export function validateStep(step: number, formData: FormData): Record<string, string> {
  const e: Record<string, string> = {}
  switch (step) {
    case 1:
      if (!formData.name.trim()) e.name = 'Nombre completo requerido'
      if (!formData.email.trim()) e.email = 'Email requerido'
      else if (!/\S+@\S+\.\S+/.test(formData.email)) e.email = 'Email inválido'
      if (!formData.phone.trim()) e.phone = 'Teléfono requerido'
      else if (!/^\d{10}$/.test(formData.phone.replace(/\D/g, ''))) e.phone = 'Teléfono debe tener exactamente 10 dígitos'
      break
    case 2:
      if (formData.hasAllergies && !formData.allergiesDetails.trim()) e.allergiesDetails = 'Por favor describe tus alergias'
      if (formData.hasSkinConditions && !formData.skinConditionsDetails.trim()) e.skinConditionsDetails = 'Describe la condición de piel'
      if (formData.hasMedicalConditions && !formData.medicalConditionsDetails.trim()) e.medicalConditionsDetails = 'Describe la condición médica'
      if (formData.takingMedications && !formData.medicationsDetails.trim()) e.medicationsDetails = 'Menciona los medicamentos'
      break
    case 3:
      if (!formData.serviceType) e.serviceType = 'Selecciona un servicio'
      if (!formData.appointmentDate) e.appointmentDate = 'Selecciona una fecha'
      else if (isWeekendMX(formData.appointmentDate)) e.appointmentDate = 'No atendemos domingos.'
      else if (!validateAppointmentDate(formData.appointmentDate)) e.appointmentDate = 'Citas con 2 días de anticipación en días hábiles.'
      if (!formData.appointmentTime) e.appointmentTime = 'Selecciona una hora'
      break
    case 5:
      if (!formData.acceptPolicies) e.acceptPolicies = 'Debes aceptar las políticas'
      break
  }
  return e
}

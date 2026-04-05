const steps = [
  {
    icon: 'brush',
    title: 'Elige tu servicio',
    desc: 'Selecciona la técnica que mejor se adapte a tu estilo.',
  },
  {
    icon: 'calendar_month',
    title: 'Agenda tu cita',
    desc: 'Encuentra el espacio perfecto en nuestra agenda digital.',
  },
  {
    icon: 'payments',
    title: 'Paga tu anticipo',
    desc: 'Asegura tu lugar con un depósito mínimo reembolsable.',
  },
]

export default function Process() {
  return (
    <section className="py-24 px-8 text-center bg-surface">
      <h3 className="font-headline text-3xl text-primary mb-16">
        Tu Experiencia Gratia
      </h3>

      <div className="grid gap-12 max-w-xs mx-auto">
        {steps.map((step, i) => (
          <div key={i} className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-full bg-surface-high flex items-center justify-center mb-6 text-primary">
              <span className="material-symbols-outlined text-3xl">
                {step.icon}
              </span>
            </div>
            <h5 className="font-headline text-lg text-primary mb-2">
              {step.title}
            </h5>
            <p className="text-on-surface-variant text-sm font-light">
              {step.desc}
            </p>
          </div>
        ))}
      </div>
    </section>
  )
}

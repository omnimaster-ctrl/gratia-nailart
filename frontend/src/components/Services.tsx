const services = [
  {
    title: 'Manicura',
    desc: 'Limpieza profunda y esmaltado de alta precisión.',
    elevated: false,
  },
  {
    title: 'Nivelación en uña natural',
    desc: 'Estructura perfecta para un acabado impecable y duradero.',
    elevated: true,
  },
  {
    title: 'Refuerzo técnica híbrida',
    desc: 'Máxima resistencia combinando gel y acrílico de alta gama.',
    elevated: false,
  },
  {
    title: 'Extensión híbrida',
    desc: 'Longitud personalizada con acabado natural y etéreo.',
    elevated: true,
  },
]

export default function Services() {
  return (
    <section className="py-24 px-6 bg-surface">
      <div className="mb-16">
        <h3 className="font-headline text-3xl text-primary italic mb-2">
          Servicios Exclusivos
        </h3>
        <div className="w-20 h-0.5 bg-secondary" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {services.map((s, i) => (
          <div
            key={i}
            className={`group p-8 rounded-xl flex flex-col justify-between h-64 transition-colors ${
              s.elevated
                ? 'bg-surface-high mt-4 md:mt-12'
                : 'bg-surface hover:bg-surface-high'
            }`}
          >
            <div>
              <h4 className="font-headline text-2xl text-primary mb-2">
                {s.title}
              </h4>
              <p className="text-on-surface-variant text-sm font-light">
                {s.desc}
              </p>
            </div>
            <div className="flex justify-between items-end border-t border-outline-variant/20 pt-4">
              <span className="font-label text-xs uppercase tracking-widest text-secondary">
                Consultar
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

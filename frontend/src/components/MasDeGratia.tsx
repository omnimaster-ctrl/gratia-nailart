type CardData = { image: string; title: string; subtitle?: string; desc: string }
const cards: CardData[] = [
  {
    image: '/assets/mascot/shopping.png',
    title: 'Gratia Nail Shop',
    desc: 'Productos con diseño artesanal de productos.',
  },
  {
    image: '/assets/fairy/reading.png',
    title: 'Gratia Academy',
    desc: 'Aprende las técnicas de los artistas experimentados.',
  },
  {
    image: '/assets/fairy/scroll.png',
    title: 'Reserva tu cita',
    desc: 'Asegura tu cita por adelanto de los mejores artistas disponibles.',
  },
]

export default function MasDeGratia() {
  return (
    <section
      className="relative py-20 px-6 overflow-hidden"
      style={{
        background: `
          radial-gradient(ellipse 60% 50% at 50% 80%, rgba(205,162,85,0.08) 0%, transparent 60%),
          linear-gradient(180deg, #3d4435 0%, #515942 40%, #515942 60%, #3d4435 100%)
        `,
      }}
    >
      {/* Section header with gold accent */}
      <div className="text-center mb-14">
        <h3 className="font-headline text-3xl md:text-4xl text-dark-text italic mb-4">
          Más de Gratia
        </h3>
        <div className="mx-auto w-16 h-0.5 rounded-full bg-gold/60" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {cards.map((card, i) => (
          <div
            key={i}
            className="group bg-warm-beige/90 rounded-2xl p-6 flex flex-col items-center text-center gap-3
              shadow-[0_4px_16px_rgba(42,46,37,0.12)]
              hover:shadow-[0_8px_28px_rgba(42,46,37,0.2)]
              hover:-translate-y-1
              border border-transparent hover:border-gold/20
              transition-all duration-300 ease-out"
          >
            <div className="relative">
              <img
                src={card.image}
                alt={card.title}
                className="w-32 h-32 object-contain drop-shadow-md group-hover:scale-105 transition-transform duration-300"
              />
            </div>
            <h4 className="font-headline text-lg text-dark-deeper font-bold">
              {card.title}
            </h4>
            {card.subtitle && (
              <span className="font-label text-xs text-gold italic -mt-2">
                {card.subtitle}
              </span>
            )}
            <p className="font-body text-sm text-on-surface-variant leading-relaxed">
              {card.desc}
            </p>
          </div>
        ))}
      </div>
    </section>
  )
}

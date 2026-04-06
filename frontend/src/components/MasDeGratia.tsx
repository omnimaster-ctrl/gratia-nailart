const cards = [
  {
    image: '/assets/mascot/shopping.png',
    title: 'Gratia Nail Shop',
    desc: 'Productos con diseño artesanal de productos.',
  },
  {
    image: '/assets/fairy/reading.png',
    title: 'Jardín de las Hadas',
    subtitle: 'Gratia Academy',
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
    <section className="py-20 px-6 bg-dark-bg">
      <h3 className="font-headline text-3xl md:text-4xl text-dark-text text-center italic mb-12">
        Más de Gratia
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {cards.map((card, i) => (
          <div
            key={i}
            className="bg-warm-beige/90 rounded-2xl p-6 flex flex-col items-center text-center gap-3 shadow-[0_4px_16px_rgba(42,46,37,0.12)] hover:shadow-[0_6px_20px_rgba(42,46,37,0.18)] transition-shadow"
          >
            <img
              src={card.image}
              alt={card.title}
              className="w-28 h-28 object-contain"
            />
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

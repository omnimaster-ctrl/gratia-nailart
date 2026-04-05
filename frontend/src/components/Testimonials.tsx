const testimonials = [
  {
    text: 'La atención al detalle es insuperable. Mis manos nunca se habían visto tan artísticas y elegantes.',
    author: 'Elena M.',
  },
  {
    text: 'Un espacio de paz y profesionalismo. La técnica de nivelación cambió por completo la salud de mis uñas.',
    author: 'Isabella R.',
  },
]

function Stars() {
  return (
    <div className="flex gap-1 text-secondary mb-4">
      {[...Array(5)].map((_, i) => (
        <span
          key={i}
          className="material-symbols-outlined text-sm"
          style={{ fontVariationSettings: "'FILL' 1" }}
        >
          star
        </span>
      ))}
    </div>
  )
}

export default function Testimonials() {
  return (
    <section className="py-24 bg-surface overflow-x-auto">
      <h3 className="font-headline text-3xl text-primary px-8 mb-12 italic">
        Voces del Atelier
      </h3>

      <div className="flex gap-6 px-8 pb-8 snap-x">
        {testimonials.map((t, i) => (
          <div
            key={i}
            className="min-w-[80vw] md:min-w-[400px] snap-center bg-surface p-8 rounded-2xl shadow-sm italic"
          >
            <Stars />
            <p className="text-on-surface-variant text-lg mb-6 leading-relaxed">
              "{t.text}"
            </p>
            <span className="font-label text-xs tracking-widest uppercase text-primary">
              — {t.author}
            </span>
          </div>
        ))}
      </div>
    </section>
  )
}

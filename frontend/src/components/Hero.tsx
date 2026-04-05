const HERO_IMG =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuCoc7AuQ2KIDK9NC-BselmmpYR8hjVGs3MEV20W88D_v5ugRm3XI3zYf9MnNCa8pFgTf6iOdMy7OQuW9csxmWJgTg5CS0ISRNcV17yhfB_ga8PDvaYXg9RlgKhk6PE2gM1qGehUmwQcJT9g5VkpSF6f6mtOf0w1mTyObQM4sNp1B7tWh3Al5NWkSoGNQCcNDa_rUoyfazd9oISP_ZVOj8iADak3t8yQul7fVfMMw30US14V8MTtTvU0ZwpDisrhiEA2_9Oer_1A9-c'

export default function Hero() {
  return (
    <section className="relative h-[751px] flex flex-col justify-end px-6 pb-20 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-surface via-transparent to-surface">
        <img
          alt="Nail Art Hero"
          className="w-full h-full object-cover opacity-60 mix-blend-multiply grayscale"
          src={HERO_IMG}
        />
      </div>

      <div className="max-w-xl">
        <span className="font-label tracking-[0.4em] text-secondary text-xs font-bold block mb-4">
          UÑAS & NAIL ART
        </span>
        <h2 className="font-headline text-6xl md:text-8xl text-primary leading-tight mb-6">
          Gratia
        </h2>
        <p className="font-body text-on-surface-variant text-lg max-w-xs mb-10 leading-relaxed italic">
          Técnicas mixtas inspiradas en el jardín de las hadas. Arte y magia en
          cada detalle.
        </p>
        <button className="bg-gradient-to-r from-primary to-primary-container text-on-primary px-8 py-4 rounded-xl font-label tracking-widest text-sm uppercase font-bold active:scale-95 transition-all shadow-xl">
          Agendar Cita
        </button>
      </div>
    </section>
  )
}

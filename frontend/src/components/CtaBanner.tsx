export default function CtaBanner() {
  return (
    <section className="w-full shimmer-bg py-8 md:py-10 px-6 text-center relative overflow-hidden">
      {/* Subtle sparkle accents */}
      <span className="absolute top-3 left-[15%] text-white/20 text-xs pointer-events-none">✦</span>
      <span className="absolute bottom-4 right-[20%] text-white/15 text-sm pointer-events-none">✦</span>

      <p className="font-body text-lg md:text-xl font-semibold text-dark-deeper relative z-10">
        ¿Te gustó un diseño?{' '}
        <a
          href="/booking"
          className="inline-flex items-center gap-2 underline underline-offset-4 decoration-dark-deeper/40 hover:decoration-dark-deeper transition-all duration-300"
        >
          Agenda tu cita
          <span className="text-base">→</span>
        </a>
      </p>
    </section>
  )
}

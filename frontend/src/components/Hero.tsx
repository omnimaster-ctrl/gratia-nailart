export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 pt-20 pb-16 overflow-hidden bg-dark-bg">
      {/* 3-column layout: gems/products | text | fairy mascot */}
      <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-[140px_1fr_200px] items-center gap-6 md:gap-10">
        {/* LEFT — Decorative nail art / product images */}
        <div className="hidden md:flex flex-col gap-4 items-center">
          <img
            src="/assets/products/polish-1.png"
            alt="Gratia Nail Products"
            className="w-28 drop-shadow-lg"
          />
          <img
            src="/assets/products/polish-2.png"
            alt="Gratia Nail Products"
            className="w-28 drop-shadow-lg"
          />
        </div>

        {/* CENTER — Main hero content */}
        <div className="text-center">
          <h2 className="font-headline text-5xl md:text-7xl lg:text-8xl text-gold leading-tight mb-4 italic">
            Gratia Nail Art
          </h2>
          <p className="font-body text-dark-muted text-lg md:text-xl mb-10 tracking-wide">
            Uñas & Nail Art — Técnicas mixtas
          </p>
          <a
            href="#"
            className="inline-block border-2 border-gold text-gold px-8 py-3 rounded-lg font-label text-sm uppercase tracking-widest font-semibold hover:bg-gold hover:text-dark-deeper transition-all duration-300"
          >
            Agenda tu cita
          </a>
        </div>

        {/* RIGHT — Fairy mascot (the one from the Stitch design) */}
        <div className="hidden md:flex justify-center">
          <img
            src="/assets/fairy/flying.jpeg"
            alt="Hada del Bosque — mascota de Gratia"
            className="w-48 drop-shadow-2xl"
          />
        </div>
      </div>

      {/* Mobile: show fairy + products below hero text */}
      <div className="flex md:hidden gap-4 mt-10 justify-center items-end">
        <img
          src="/assets/products/polish-1.png"
          alt="Gratia Products"
          className="w-16 drop-shadow-md"
        />
        <img
          src="/assets/fairy/flying.jpeg"
          alt="Hada del Bosque"
          className="w-28 drop-shadow-xl"
        />
        <img
          src="/assets/products/polish-2.png"
          alt="Gratia Products"
          className="w-16 drop-shadow-md"
        />
      </div>
    </section>
  )
}

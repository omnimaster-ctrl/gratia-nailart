import { useEffect, useState } from 'react'

const carouselImages = [
  '/assets/mascot/artist.png',
  '/assets/fairy/mushroom.png',
  '/assets/mascot/pointing.png',
  '/assets/fairy/reading.png',
  '/assets/mascot/certificate.png',
  '/assets/fairy/scroll.png',
  '/assets/mascot/grinning.png',
  '/assets/mascot/serene.png',
]

export default function Hero() {
  const [active, setActive] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setActive((prev) => (prev + 1) % carouselImages.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  // Show 3 images at a time in the carousel
  const visibleCount = 3
  const getIndex = (offset: number) =>
    (active + offset) % carouselImages.length

  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 pt-20 pb-16 overflow-hidden bg-dark-bg">
      <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-[140px_1fr_200px] items-center gap-6 md:gap-10">
        {/* LEFT — Vertical carousel */}
        <div className="hidden md:flex flex-col gap-3 items-center h-[360px] overflow-hidden relative">
          {Array.from({ length: visibleCount }).map((_, offset) => {
            const idx = getIndex(offset)
            const isCenter = offset === 1
            return (
              <div
                key={`${active}-${offset}`}
                className={`w-24 h-24 rounded-2xl overflow-hidden transition-all duration-700 flex-shrink-0 ${
                  isCenter
                    ? 'scale-110 shadow-lg opacity-100 ring-2 ring-gold/30'
                    : 'scale-90 opacity-60'
                }`}
              >
                <img
                  src={carouselImages[idx]}
                  alt="Gratia"
                  className="w-full h-full object-contain bg-dark-deeper/40 rounded-2xl p-1"
                />
              </div>
            )
          })}

          {/* Dots indicator */}
          <div className="flex gap-1.5 mt-2">
            {carouselImages.map((_, i) => (
              <button
                key={i}
                onClick={() => setActive(i)}
                className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                  i === active ? 'bg-gold w-3' : 'bg-dark-muted/40'
                }`}
              />
            ))}
          </div>
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

        {/* RIGHT — Fairy mascot */}
        <div className="hidden md:flex justify-center">
          <img
            src="/assets/fairy/flying.png"
            alt="Hada del Bosque — mascota de Gratia"
            className="w-48 drop-shadow-2xl"
          />
        </div>
      </div>

      {/* Mobile: horizontal carousel below hero */}
      <div className="flex md:hidden gap-3 mt-10 overflow-x-auto snap-x px-4 pb-2">
        {carouselImages.slice(0, 5).map((src, i) => (
          <img
            key={i}
            src={src}
            alt="Gratia"
            className="w-20 h-20 rounded-xl object-contain bg-dark-deeper/40 p-1 flex-shrink-0 snap-center"
          />
        ))}
      </div>
    </section>
  )
}

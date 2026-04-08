import { useRef, useEffect } from 'react'

const galleryItems = [
  { src: '/assets/gallery/pink-gems.png', label: 'Nail Art' },
  { src: '/assets/gallery/quilted-stars.png', label: 'Técnica mixta' },
  { src: '/assets/gallery/silver-chrome.png', label: 'Nail Art' },
  { src: '/assets/gallery/opal-gold.png', label: 'Nail Art' },
  { src: '/assets/gallery/halloween-faces.png', label: 'Nail Art' },
  { src: '/assets/gallery/polkadot-bows.png', label: 'Técnica mixta' },
  { src: '/assets/gallery/coral-chrome.png', label: 'Nail Art' },
  { src: '/assets/gallery/floral-mixed.png', label: 'Técnica mixta' },
]

export default function Gallery() {
  const scrollRef = useRef<HTMLDivElement>(null)

  // Auto-scroll the carousel
  useEffect(() => {
    const el = scrollRef.current
    if (!el) return

    let scrollPos = 0
    const speed = 0.5
    let animId: number
    let paused = false

    const step = () => {
      if (!paused && el) {
        scrollPos += speed
        if (scrollPos >= el.scrollWidth / 2) {
          scrollPos = 0
        }
        el.scrollLeft = scrollPos
      }
      animId = requestAnimationFrame(step)
    }

    const pause = () => { paused = true }
    const resume = () => {
      paused = false
      scrollPos = el.scrollLeft
    }

    el.addEventListener('pointerenter', pause)
    el.addEventListener('pointerleave', resume)
    el.addEventListener('touchstart', pause)
    el.addEventListener('touchend', resume)

    animId = requestAnimationFrame(step)

    return () => {
      cancelAnimationFrame(animId)
      el.removeEventListener('pointerenter', pause)
      el.removeEventListener('pointerleave', resume)
      el.removeEventListener('touchstart', pause)
      el.removeEventListener('touchend', resume)
    }
  }, [])

  // Duplicate items for infinite scroll illusion
  const items = [...galleryItems, ...galleryItems]

  return (
    <section
      className="relative py-20 overflow-hidden"
      style={{
        background: 'linear-gradient(180deg, #3d4435 0%, #515942 30%, #515942 70%, #3d4435 100%)',
      }}
    >
      {/* Section title with gold accent */}
      <div className="text-center mb-12 px-6">
        <h3 className="font-headline text-3xl md:text-4xl text-dark-text italic mb-4">
          Mi Trabajo
        </h3>
        <div className="mx-auto w-16 h-0.5 rounded-full bg-gold/60" />
      </div>

      {/* Horizontal carousel with fade edges */}
      <div className="carousel-fade-mask">
        <div
          ref={scrollRef}
          className="flex gap-5 overflow-x-auto px-6 pb-4 no-scrollbar"
        >
          {items.map((item, i) => (
            <div
              key={i}
              className="flex-shrink-0 w-[220px] md:w-[270px] group cursor-pointer"
            >
              <div className="relative aspect-[3/4] rounded-2xl overflow-hidden shadow-[0_4px_16px_rgba(42,46,37,0.25)] group-hover:shadow-[0_8px_32px_rgba(205,162,85,0.25)] transition-all duration-500">
                <img
                  src={item.src}
                  alt={item.label}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                />
                {/* Gradient overlay at bottom */}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-dark-deepest/80 via-dark-deepest/30 to-transparent pt-12 pb-3 px-4">
                  <span className="font-label text-sm text-dark-text/90 font-medium tracking-wide">
                    {item.label}
                  </span>
                </div>
                {/* Gold hover ring */}
                <div className="absolute inset-0 rounded-2xl ring-0 ring-gold/0 group-hover:ring-2 group-hover:ring-gold/40 transition-all duration-500 pointer-events-none" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

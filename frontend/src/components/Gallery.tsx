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
    const speed = 0.5 // px per frame
    let animId: number
    let paused = false

    const step = () => {
      if (!paused && el) {
        scrollPos += speed
        // Reset when we've scrolled through half (the duplicated set)
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
    <section className="py-16 bg-dark-deeper/60">
      <h3 className="font-headline text-3xl md:text-4xl text-dark-text text-center italic mb-10">
        Mi Trabajo
      </h3>

      {/* Horizontal carousel — no scrollbar, edge peek */}
      <div
        ref={scrollRef}
        className="flex gap-4 overflow-x-auto px-4 pb-4"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none', WebkitOverflowScrolling: 'touch' }}
      >
        <style>{`[data-gallery-scroll]::-webkit-scrollbar { display: none; }`}</style>
        {items.map((item, i) => (
          <div
            key={i}
            className="flex-shrink-0 w-[220px] md:w-[260px] group"
          >
            <div className="relative aspect-[3/4] rounded-2xl overflow-hidden shadow-[0_4px_16px_rgba(42,46,37,0.2)]">
              <img
                src={item.src}
                alt={item.label}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              {/* Label overlay at bottom */}
              <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-dark-deeper/80 via-dark-deeper/40 to-transparent pt-10 pb-3 px-4">
                <span className="font-label text-sm text-dark-text/90 font-medium">
                  {item.label}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

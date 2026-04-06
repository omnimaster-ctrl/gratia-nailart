import { useRef, useEffect } from 'react'

const galleryItems = [
  {
    src: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA-SKJg3Krqg_YNa20H0I_jxXpNUH1mZ67P1NQY3tLi5Nf0nD6YEzVYGnxgAPGx1jpii-lKTsD5g1Lfp4ELMUto0gV53DeQiZrs50qi3aNT3xvd6ikj1eUB5IKEBttfvTEj7tR4w-d89ye1UC2WHR-hHU4XwDhb8xo4wir6O2GOTRPuGsuRSuXu0VLoV_JSP3Vas5j9hmSX9nzRLvg_d_7f1G-ywhdldZsNGzOzhQge4dJjuZcVRXoVmmRB6PyvJseEkMaIQKtInB0',
    label: 'Nail Art',
  },
  {
    src: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDBorUp44Ge58M7VhYFYusna9ICBEdv9xg6t_9wf3kfq-W_qRpoioVSbPfAvMpe3EgfueuDqQ4x9LuMEOJi_hpsi6-IMk0VQbdT_OhlbSV7nNAGpz1mCzNobIo4hXhRAiDwDDmirvom-6A0wu0RMM1t3HoSG711RWkr4p8WMS-WTbpG0z2vhv8BgwE66RzP3GsZggnzL4hNgMSYAEingyonwVkjyqNI_v7_wnoTVrXlTAT-4AJOdIchwCFMukmLiITIVJH9nOXQhYk',
    label: 'Técnica mixta',
  },
  {
    src: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCDj-AWFEtyGUCh9ccMcj-Veri92jtq1GTftMYo1rP9mq30pHcOkanQWvAQ06E2KLrxxlLNhPDH2K1TrCDcZmZfC1Aztrgh1JPRV2sbyH749wxs_WLq_fvRm54psEJ84EYtTMtEEus24AT0HWUQLYxm4pblWOZ8S701v_h12kSmfXC2DQjdzZqAQvIJ_Bo7eWNwWRIHbaILDCyLm01JzrOnqhIifqFkS38oCZZ90B4fApf7c9KLz8Wisq7rwp0vK4qdSyB_UhLdZNA',
    label: 'Nail Art',
  },
  {
    src: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAQgYTv8sIC4dupJj7pyIASRHVi8qDuCnmCfwOHq8jAO9zeHLk-lLg-ZIAWdkTndo93jvEGb8ZdD1h4nSveUXDJwt7__i5nmuj9CPA8bFWfALbw3vgMT5W6JhFHbtZlJZ1LDHSfcsuRhsnTmVHe3mv5MlqJmxoEZiIpQnrZp_4KOyCN16QdpPp0wHDAxD_0-HqQNqIOwhEWrP14SWwP3DWXDZKHFLD4c-rXyQhSqJpdsLT649inxFawzUzeuUE70cbkg1c6B8N4nzE',
    label: 'Nail Art',
  },
  {
    src: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCoc7AuQ2KIDK9NC-BselmmpYR8hjVGs3MEV20W88D_v5ugRm3XI3zYf9MnNCa8pFgTf6iOdMy7OQuW9csxmWJgTg5CS0ISRNcV17yhfB_ga8PDvaYXg9RlgKhk6PE2gM1qGehUmwQcJT9g5VkpSF6f6mtOf0w1mTyObQM4sNp1B7tWh3Al5NWkSoGNQCcNDa_rUoyfazd9oISP_ZVOj8iADak3t8yQul7fVfMMw30US14V8MTtTvU0ZwpDisrhiEA2_9Oer_1A9-c',
    label: 'Técnica mixta',
  },
  {
    src: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA-SKJg3Krqg_YNa20H0I_jxXpNUH1mZ67P1NQY3tLi5Nf0nD6YEzVYGnxgAPGx1jpii-lKTsD5g1Lfp4ELMUto0gV53DeQiZrs50qi3aNT3xvd6ikj1eUB5IKEBttfvTEj7tR4w-d89ye1UC2WHR-hHU4XwDhb8xo4wir6O2GOTRPuGsuRSuXu0VLoV_JSP3Vas5j9hmSX9nzRLvg_d_7f1G-ywhdldZsNGzOzhQge4dJjuZcVRXoVmmRB6PyvJseEkMaIQKtInB0',
    label: 'Nail Art',
  },
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

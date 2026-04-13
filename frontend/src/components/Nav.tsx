import { useState, useEffect } from 'react'

const navLinks = [
  { label: 'Home', href: '#', active: true },
  { label: 'Servicios', href: '#servicios' },
  { label: 'Enseñamos', href: '#ensenamos' },
  { label: 'Contacto', href: '#contacto' },
]

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 flex justify-center pt-4 md:pt-5 px-4">
        <nav
          className={`flex items-center gap-1 md:gap-2 px-3 md:px-6 py-2.5 rounded-full transition-all duration-500 ${
            scrolled
              ? 'bg-dark-deeper/90 shadow-[0_4px_24px_rgba(0,0,0,0.3)] nav-glass'
              : 'bg-dark-deeper/50 nav-glass'
          }`}
        >
          {/* Mobile hamburger */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden text-dark-text hover:text-gold transition-colors p-1"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>

          {/* Desktop nav links */}
          <div className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className={`font-label text-sm transition-colors duration-200 ${
                  link.active
                    ? 'text-gold underline underline-offset-4 decoration-gold/60'
                    : 'text-dark-text/80 hover:text-gold'
                }`}
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* Divider */}
          <div className="hidden md:block w-px h-5 bg-dark-text/20 mx-2" />

          {/* CTA pill */}
          <a
            href="/booking"
            className="border border-gold/60 text-gold px-4 py-1.5 rounded-full font-label text-sm font-semibold
              hover:bg-gold hover:text-dark-deeper
              transition-all duration-300 whitespace-nowrap"
          >
            Agenda tu cita
          </a>
        </nav>
      </header>

      {/* Mobile menu overlay */}
      {menuOpen && (
        <div className="fixed inset-0 z-40 bg-dark-deepest/95 nav-glass flex flex-col items-center justify-center gap-8"
          onClick={() => setMenuOpen(false)}
        >
          {navLinks.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className={`font-headline text-2xl italic transition-colors ${
                link.active ? 'text-gold' : 'text-dark-text hover:text-gold'
              }`}
            >
              {link.label}
            </a>
          ))}
          <a
            href="/booking"
            className="mt-4 border-2 border-gold text-gold px-8 py-3 rounded-full font-label text-base font-semibold
              hover:bg-gold hover:text-dark-deeper transition-all"
          >
            Agenda tu cita
          </a>
        </div>
      )}
    </>
  )
}

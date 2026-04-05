const navLinks = ['Home', 'Servicios', 'Enseñamos', 'Contacto']

export default function Nav() {
  return (
    <header className="fixed top-0 w-full z-50 glass-nav bg-dark-deeper/80 flex items-center justify-between px-6 md:px-10 h-16">
      {/* Logo */}
      <h1 className="font-headline italic text-gold text-lg tracking-wide">
        Gratia Nail Art
      </h1>

      {/* Desktop nav links */}
      <nav className="hidden md:flex items-center gap-8">
        {navLinks.map((link) => (
          <a
            key={link}
            href="#"
            className="font-label text-sm text-dark-text/80 hover:text-gold transition-colors"
          >
            {link}
          </a>
        ))}
      </nav>

      {/* CTA pill */}
      <a
        href="#"
        className="bg-gold text-dark-deeper px-5 py-2 rounded-full font-label text-sm font-semibold hover:brightness-110 transition-all"
      >
        Agenda tu cita
      </a>

      {/* Mobile hamburger (hidden on desktop) */}
      <button className="md:hidden material-symbols-outlined text-dark-text hover:opacity-70 transition-opacity absolute left-4">
        menu
      </button>
    </header>
  )
}

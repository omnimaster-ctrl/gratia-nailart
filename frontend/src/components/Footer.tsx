export default function Footer() {
  return (
    <footer className="relative w-full pt-14 pb-10 px-8 bg-dark-deepest flex flex-col items-center gap-6 text-center">
      {/* Top gradient fade */}
      <div
        className="absolute top-0 left-0 right-0 h-16 pointer-events-none"
        style={{
          background: 'linear-gradient(to bottom, #3d4435, #2a2e25)',
        }}
      />

      {/* Fairy peeking as footer decoration */}
      <div className="relative -mt-20 mb-2">
        <div
          className="absolute inset-0 -m-4 rounded-full blur-2xl opacity-25"
          style={{
            background: 'radial-gradient(circle, rgba(205,162,85,0.5) 0%, transparent 70%)',
          }}
        />
        <img
          src="/assets/fairy/peeking.png"
          alt="Hada del Bosque"
          className="relative w-24 drop-shadow-lg animate-float-slow"
        />
      </div>

      {/* Social icons */}
      <div className="flex gap-4">
        <a
          href="https://instagram.com/gratia.nailart"
          target="_blank"
          rel="noopener noreferrer"
          className="w-10 h-10 rounded-full border border-dark-muted/30 flex items-center justify-center text-dark-muted
            hover:text-gold hover:border-gold hover:bg-gold/10
            transition-all duration-300"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="2" y="2" width="20" height="20" rx="5" />
            <circle cx="12" cy="12" r="5" />
            <circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none" />
          </svg>
        </a>
        <a
          href="#"
          className="w-10 h-10 rounded-full border border-dark-muted/30 flex items-center justify-center text-dark-muted
            hover:text-gold hover:border-gold hover:bg-gold/10
            transition-all duration-300"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z" />
          </svg>
        </a>
      </div>

      <p className="font-body text-sm text-dark-muted">@gratia.nailart</p>

      <div className="flex flex-col items-center gap-6 mt-6 pb-2">
        <a 
          href="https://omnifractal.dev/" 
          target="_blank" 
          rel="noopener noreferrer"
          className="flex items-center gap-3 md:gap-4 group"
        >
          <span className="font-label text-[10px] md:text-xs tracking-[0.2em] md:tracking-[0.3em] uppercase text-dark-muted/50 group-hover:text-dark-muted transition-colors">
            SOFTWARE BY
          </span>
          
          <svg 
            viewBox="0 0 35 22" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
            className="w-10 h-auto md:w-12 text-gold opacity-70 group-hover:opacity-100 group-hover:drop-shadow-[0_0_12px_rgba(205,162,85,0.8)] transition-all duration-500 transform -rotate-12 group-hover:-rotate-6"
          >
            {/* Golden rectangles */}
            <rect x="0.5" y="0.5" width="34" height="21" stroke="currentColor" strokeWidth="0.5" />
            <line x1="21.5" y1="0.5" x2="21.5" y2="21.5" stroke="currentColor" strokeWidth="0.5" />
            <line x1="21.5" y1="13.5" x2="34.5" y2="13.5" stroke="currentColor" strokeWidth="0.5" />
            <line x1="26.5" y1="13.5" x2="26.5" y2="21.5" stroke="currentColor" strokeWidth="0.5" />
            <line x1="21.5" y1="16.5" x2="26.5" y2="16.5" stroke="currentColor" strokeWidth="0.5" />
            
            {/* Golden spiral sequence */}
            <path d="M 21.5 0.5 A 21 21 0 0 0 0.5 21.5" stroke="currentColor" strokeWidth="1" />
            <path d="M 21.5 0.5 A 13 13 0 0 1 34.5 13.5" stroke="currentColor" strokeWidth="1" />
            <path d="M 34.5 13.5 A 8 8 0 0 1 26.5 21.5" stroke="currentColor" strokeWidth="1" />
            <path d="M 26.5 21.5 A 5 5 0 0 1 21.5 16.5" stroke="currentColor" strokeWidth="1" />
            <path d="M 21.5 16.5 A 3 3 0 0 1 24.5 13.5" stroke="currentColor" strokeWidth="1" />
          </svg>

          <span className="font-label text-sm md:text-base font-bold tracking-[0.15em] md:tracking-widest uppercase text-dark-muted/80 group-hover:text-white transition-colors">
            OMNIFRACTAL
          </span>
        </a>

        <p className="font-label text-[10px] tracking-widest text-dark-muted/40">
          &copy; {new Date().getFullYear()} Gratia Nail Art. All Rights Reserved.
        </p>
      </div>
    </footer>
  )
}

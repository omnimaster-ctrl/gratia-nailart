// Full botanical laurel wreath SVG — thin line-art olive leaves wrapping around an oval frame
function LaurelWreath() {
  // Brighter, bolder colors for visibility
  const leafColor = '#a0b87a'
  const stemColor = '#8da066'

  return (
    <svg
      className="absolute inset-0 w-full h-full pointer-events-none"
      viewBox="0 0 240 280"
      fill="none"
    >
      {/* ── LEFT BRANCH — curving from bottom-center up and over the top ── */}
      <g>
        {/* Main stem - left */}
        <path
          d="M115 268 Q60 240 32 200 Q10 160 10 120 Q10 80 32 45 Q55 15 100 5"
          stroke={stemColor}
          strokeWidth="1.8"
          fill="none"
          opacity="0.8"
        />

        {/* Leaves along left stem — bottom to top */}
        {/* Bottom cluster */}
        <path d="M105 260 Q85 255 80 248" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M80 248 Q85 242 105 245" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M95 255 Q75 248 72 240" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M72 240 Q78 235 95 240" stroke={leafColor} strokeWidth="1.3" fill="none" />

        {/* Lower-left leaves */}
        <path d="M75 240 Q55 230 50 222" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M50 222 Q58 218 75 228" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M65 232 Q45 220 42 210" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M42 210 Q50 207 65 220" stroke={leafColor} strokeWidth="1.3" fill="none" />

        {/* Mid-left leaves */}
        <path d="M50 212 Q32 198 28 188" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M28 188 Q35 185 50 200" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M40 200 Q22 185 20 174" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M20 174 Q28 172 40 188" stroke={leafColor} strokeWidth="1.3" fill="none" />

        {/* Center-left leaves */}
        <path d="M30 178 Q12 162 10 150" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M10 150 Q18 148 30 165" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M22 162 Q6 145 5 132" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M5 132 Q14 130 22 148" stroke={leafColor} strokeWidth="1.3" fill="none" />

        {/* Upper-left leaves */}
        <path d="M18 140 Q4 122 5 110" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M5 110 Q14 110 18 128" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M15 120 Q5 100 8 88" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M8 88 Q16 90 15 108" stroke={leafColor} strokeWidth="1.3" fill="none" />

        {/* Top-left leaves */}
        <path d="M18 95 Q12 75 18 62" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M18 62 Q24 68 18 85" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M25 75 Q22 55 28 42" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M28 42 Q34 50 25 65" stroke={leafColor} strokeWidth="1.3" fill="none" />

        {/* Top curve leaves */}
        <path d="M38 55 Q38 35 48 25" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M48 25 Q50 35 38 48" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M55 38 Q58 20 70 12" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M70 12 Q70 24 55 32" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M75 25 Q82 10 95 8" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M95 8 Q90 18 75 22" stroke={leafColor} strokeWidth="1.3" fill="none" />
      </g>

      {/* ── RIGHT BRANCH — mirrored ── */}
      <g transform="scale(-1,1) translate(-240,0)">
        {/* Main stem - right (mirrored) */}
        <path
          d="M115 268 Q60 240 32 200 Q10 160 10 120 Q10 80 32 45 Q55 15 100 5"
          stroke={stemColor}
          strokeWidth="1.8"
          fill="none"
          opacity="0.8"
        />

        {/* Same leaves mirrored */}
        <path d="M105 260 Q85 255 80 248" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M80 248 Q85 242 105 245" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M95 255 Q75 248 72 240" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M72 240 Q78 235 95 240" stroke={leafColor} strokeWidth="1.3" fill="none" />

        <path d="M75 240 Q55 230 50 222" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M50 222 Q58 218 75 228" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M65 232 Q45 220 42 210" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M42 210 Q50 207 65 220" stroke={leafColor} strokeWidth="1.3" fill="none" />

        <path d="M50 212 Q32 198 28 188" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M28 188 Q35 185 50 200" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M40 200 Q22 185 20 174" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M20 174 Q28 172 40 188" stroke={leafColor} strokeWidth="1.3" fill="none" />

        <path d="M30 178 Q12 162 10 150" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M10 150 Q18 148 30 165" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M22 162 Q6 145 5 132" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M5 132 Q14 130 22 148" stroke={leafColor} strokeWidth="1.3" fill="none" />

        <path d="M18 140 Q4 122 5 110" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M5 110 Q14 110 18 128" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M15 120 Q5 100 8 88" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M8 88 Q16 90 15 108" stroke={leafColor} strokeWidth="1.3" fill="none" />

        <path d="M18 95 Q12 75 18 62" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M18 62 Q24 68 18 85" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M25 75 Q22 55 28 42" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M28 42 Q34 50 25 65" stroke={leafColor} strokeWidth="1.3" fill="none" />

        <path d="M38 55 Q38 35 48 25" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M48 25 Q50 35 38 48" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M55 38 Q58 20 70 12" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M70 12 Q70 24 55 32" stroke={leafColor} strokeWidth="1.3" fill="none" />
        <path d="M75 25 Q82 10 95 8" stroke={leafColor} strokeWidth="1.6" fill="none" />
        <path d="M95 8 Q90 18 75 22" stroke={leafColor} strokeWidth="1.3" fill="none" />
      </g>

      {/* Oval frame border */}
      <ellipse
        cx="120"
        cy="140"
        rx="72"
        ry="90"
        stroke={stemColor}
        strokeWidth="2"
        fill="none"
        opacity="0.7"
      />
    </svg>
  )
}

// Golden fairy dust particles
function Particles() {
  const count = 30
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-[1]">
      {Array.from({ length: count }).map((_, i) => (
        <span
          key={i}
          className="particle"
          style={{
            left: `${5 + Math.random() * 90}%`,
            bottom: `${Math.random() * 80}%`,
            animationDelay: `${Math.random() * 6}s`,
            animationDuration: `${3 + Math.random() * 4}s`,
            opacity: 0.2 + Math.random() * 0.6,
            width: `${2 + Math.random() * 3}px`,
            height: `${2 + Math.random() * 3}px`,
          }}
        />
      ))}
    </div>
  )
}

// Twinkling star particles (stationary, just flickering)
function Twinkles() {
  const count = 40
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-[1]">
      {Array.from({ length: count }).map((_, i) => (
        <span
          key={i}
          className="twinkle"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${2 + Math.random() * 3}s`,
            width: `${1.5 + Math.random() * 2.5}px`,
            height: `${1.5 + Math.random() * 2.5}px`,
          }}
        />
      ))}
    </div>
  )
}

const showcaseNails = [
  { src: '/assets/gallery/opal-gold.png', alt: 'Ópalo Místico' },
  { src: '/assets/gallery/silver-chrome.png', alt: 'Espejo de Hada' },
  { src: '/assets/gallery/pink-gems.png', alt: 'Manantial Encantado' },
]

export default function Hero() {
  return (
    <section
      className="relative min-h-screen flex flex-col items-center justify-center px-4 pt-24 pb-10 overflow-hidden"
      style={{
        background: '#2a2e25',
      }}
    >
      {/* Forest background image */}
      <div
        className="absolute inset-0 z-0 opacity-35 blur-[2px]"
        style={{
          backgroundImage: 'url(/assets/forest-bg.png)',
          backgroundSize: 'cover',
          backgroundPosition: 'center top',
          backgroundRepeat: 'no-repeat',
        }}
      />

      {/* Dark overlay for readability - reduced from 30% to 10% to make the forest lighter */}
      <div className="absolute inset-0 z-0 bg-dark-deepest/5" />

      {/* Light rays from top */}
      <div
        className="absolute top-0 left-1/2 -translate-x-1/2 w-[120%] h-[70%] z-0 pointer-events-none"
        style={{
          background: 'conic-gradient(from 180deg at 50% 0%, transparent 35%, rgba(205,162,85,0.04) 42%, transparent 45%, transparent 50%, rgba(205,162,85,0.06) 53%, transparent 58%, transparent 65%)',
        }}
      />

      {/* Particles and twinkles */}
      <Particles />
      <Twinkles />

      {/* Main content container */}
      <div className="relative z-10 w-full max-w-4xl flex flex-col items-center">

        {/* Title + Fairy row */}
        <div className="w-full flex flex-col md:flex-row items-center justify-center gap-4 md:gap-0 mb-4 md:mb-6">
          {/* Title block */}
          <div className="text-center md:text-left flex-1 animate-fade-in-up">
            <h2
              className="font-headline text-[3.2rem] md:text-[4.5rem] lg:text-[5.5rem] text-gold leading-[1.05] italic"
              style={{
                textShadow: '0 0 80px rgba(205,162,85,0.4), 0 0 160px rgba(205,162,85,0.15), 0 2px 4px rgba(0,0,0,0.3)',
              }}
            >
              Gratia<br />Nail Art
            </h2>
            <p className="font-body text-dark-muted text-base md:text-lg mt-3 tracking-wide">
              Uñas &amp; Nail Art — Técnicas mixtas
            </p>
          </div>

          {/* Fairy mascot */}
          <div className="relative flex-shrink-0 animate-fade-in-up" style={{ animationDelay: '0.15s' }}>
            {/* Golden halo glow */}
            <div
              className="absolute inset-0 -m-10 rounded-full blur-3xl animate-glow-breathe"
              style={{
                background: 'radial-gradient(circle, rgba(205,162,85,0.45) 0%, rgba(205,162,85,0.1) 40%, transparent 70%)',
              }}
            />
              <img
                src="/assets/fairy/fairy_gratia_nobg.png"
                alt="Hada del Bosque"
                className="relative w-52 md:w-64 lg:w-72 h-auto object-contain drop-shadow-[0_0_25px_rgba(205,162,85,0.3)] animate-float"
              />
          </div>
        </div>

        {/* Three nail art showcase ovals with laurel wreaths */}
        <div
          className="flex items-center justify-center gap-8 md:gap-14 lg:gap-18 mt-4 md:mt-8 mb-10 md:mb-12 animate-fade-in-up"
          style={{ animationDelay: '0.3s' }}
        >
          {showcaseNails.map((nail, i) => (
            <div key={i} className="relative group">
              {/* Laurel wreath decoration — sized larger to wrap around the oval */}
              <div className="absolute -inset-8 md:-inset-10 lg:-inset-12">
                <LaurelWreath />
              </div>
              {/* Oval image frame — larger */}
              <div
                className="relative w-32 h-40 md:w-44 md:h-56 lg:w-52 lg:h-64 overflow-hidden
                  border border-primary/40
                  shadow-[0_0_20px_rgba(205,162,85,0.15)]
                  group-hover:border-gold-dim/60 group-hover:shadow-[0_0_30px_rgba(205,162,85,0.25)]
                  transition-all duration-500"
                style={{ borderRadius: '50%' }}
              >
                <img
                  src={nail.src}
                  alt={nail.alt}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                />
              </div>
            </div>
          ))}
        </div>

        {/* CTA Button — metallic gold */}
        <div className="animate-fade-in-up" style={{ animationDelay: '0.45s' }}>
          <a
            href="#"
            className="gold-metallic-btn inline-block px-12 md:px-16 py-3.5 md:py-4 rounded-full
              font-label text-sm md:text-base uppercase tracking-[0.2em] font-bold
              text-dark-deepest
              shadow-[0_4px_20px_rgba(205,162,85,0.35)]
              hover:shadow-[0_6px_32px_rgba(205,162,85,0.5)]
              hover:scale-[1.03]
              transition-all duration-300"
          >
            Agenda tu cita
          </a>
        </div>

        {/* Social icons */}
        <div className="flex items-center gap-5 mt-10 md:mt-14 animate-fade-in-up" style={{ animationDelay: '0.55s' }}>
          <a
            href="https://instagram.com/gratia.nailart"
            target="_blank"
            rel="noopener noreferrer"
            className="text-dark-text/60 hover:text-gold transition-colors duration-300"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="5" />
              <circle cx="12" cy="12" r="5" />
              <circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none" />
            </svg>
          </a>
          <a
            href="#"
            className="text-dark-text/60 hover:text-gold transition-colors duration-300"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z" />
            </svg>
          </a>
        </div>

        {/* Credit line */}
        <p className="mt-4 font-label text-[10px] tracking-widest uppercase text-dark-muted/40 animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
          Credit by Gratia Nail Art &nbsp;·&nbsp; <span className="font-headline italic text-dark-muted/50 text-xs normal-case tracking-normal">Gratia Nail Art</span>
        </p>
      </div>
    </section>
  )
}

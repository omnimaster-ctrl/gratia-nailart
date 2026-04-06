export default function Footer() {
  return (
    <footer className="w-full py-10 px-8 bg-dark-deeper flex flex-col items-center gap-6 text-center">
      {/* Fairy peeking as footer decoration */}
      <img
        src="/assets/fairy/peeking.png"
        alt="Hada del Bosque"
        className="w-20 -mt-16 drop-shadow-lg"
      />

      {/* Social icons */}
      <div className="flex gap-4">
        <a
          href="https://instagram.com/gratia.nailart"
          target="_blank"
          rel="noopener noreferrer"
          className="w-10 h-10 rounded-full border border-dark-muted/40 flex items-center justify-center text-dark-muted hover:text-gold hover:border-gold transition-colors"
        >
          <span className="material-symbols-outlined text-xl">camera</span>
        </a>
        <a
          href="#"
          className="w-10 h-10 rounded-full border border-dark-muted/40 flex items-center justify-center text-dark-muted hover:text-gold hover:border-gold transition-colors"
        >
          <span className="material-symbols-outlined text-xl">group</span>
        </a>
      </div>

      <p className="font-body text-sm text-dark-muted">@gratia.nailart</p>

      <p className="font-label text-[10px] tracking-widest uppercase text-dark-muted/60">
        SOFTWARE BY OMNIFRACTAL
      </p>
      <p className="font-label text-[10px] tracking-widest uppercase text-dark-muted/40">
        © 2026 Gratia Nail Art
      </p>
    </footer>
  )
}

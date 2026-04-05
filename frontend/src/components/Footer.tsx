export default function Footer() {
  return (
    <footer className="w-full py-12 px-8 bg-background flex flex-col items-center gap-8 text-center mb-16">
      <h4 className="font-headline text-lg italic text-primary">
        GRATIA NAIL ART
      </h4>
      <div className="flex gap-6">
        {['Servicios', 'Artistas', 'Privacidad'].map((label) => (
          <span
            key={label}
            className="text-on-surface-variant font-label text-xs tracking-widest uppercase hover:tracking-[0.3em] transition-all duration-500 cursor-pointer"
          >
            {label}
          </span>
        ))}
      </div>
      <p className="font-label text-[10px] tracking-widest uppercase text-primary opacity-80">
        © 2026 GRATIA NAIL ART · SOFTWARE BY OMNIFRACTAL
      </p>
    </footer>
  )
}

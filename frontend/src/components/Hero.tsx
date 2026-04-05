// Placeholder images — will be replaced with real Gratia assets
const FAIRY_IMG =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuCoc7AuQ2KIDK9NC-BselmmpYR8hjVGs3MEV20W88D_v5ugRm3XI3zYf9MnNCa8pFgTf6iOdMy7OQuW9csxmWJgTg5CS0ISRNcV17yhfB_ga8PDvaYXg9RlgKhk6PE2gM1qGehUmwQcJT9g5VkpSF6f6mtOf0w1mTyObQM4sNp1B7tWh3Al5NWkSoGNQCcNDa_rUoyfazd9oISP_ZVOj8iADak3t8yQul7fVfMMw30US14V8MTtTvU0ZwpDisrhiEA2_9Oer_1A9-c'

const GEM_IMAGES = [
  'https://lh3.googleusercontent.com/aida-public/AB6AXuA-SKJg3Krqg_YNa20H0I_jxXpNUH1mZ67P1NQY3tLi5Nf0nD6YEzVYGnxgAPGx1jpii-lKTsD5g1Lfp4ELMUto0gV53DeQiZrs50qi3aNT3xvd6ikj1eUB5IKEBttfvTEj7tR4w-d89ye1UC2WHR-hHU4XwDhb8xo4wir6O2GOTRPuGsuRSuXu0VLoV_JSP3Vas5j9hmSX9nzRLvg_d_7f1G-ywhdldZsNGzOzhQge4dJjuZcVRXoVmmRB6PyvJseEkMaIQKtInB0',
  'https://lh3.googleusercontent.com/aida-public/AB6AXuDBorUp44Ge58M7VhYFYusna9ICBEdv9xg6t_9wf3kfq-W_qRpoioVSbPfAvMpe3EgfueuDqQ4x9LuMEOJi_hpsi6-IMk0VQbdT_OhlbSV7nNAGpz1mCzNobIo4hXhRAiDwDDmirvom-6A0wu0RMM1t3HoSG711RWkr4p8WMS-WTbpG0z2vhv8BgwE66RzP3GsZggnzL4hNgMSYAEingyonwVkjyqNI_v7_wnoTVrXlTAT-4AJOdIchwCFMukmLiITIVJH9nOXQhYk',
]

export default function Hero() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center text-center px-6 pt-24 pb-16 overflow-hidden bg-dark-bg">
      {/* Decorative gem images — left side */}
      <div className="hidden md:block absolute left-4 top-1/4 space-y-4 w-24 opacity-80">
        {GEM_IMAGES.map((src, i) => (
          <img
            key={i}
            src={src}
            alt="Nail art gem"
            className="w-full rounded-xl shadow-lg"
          />
        ))}
      </div>

      {/* Fairy mascot — right side */}
      <div className="hidden md:block absolute right-8 top-1/3 w-48 opacity-90">
        <img
          src={FAIRY_IMG}
          alt="Hada del Bosque — mascota de Gratia"
          className="w-full rounded-2xl shadow-xl"
        />
      </div>

      {/* Main hero content */}
      <div className="relative z-10 max-w-2xl">
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

      {/* Mobile fairy + gems row */}
      <div className="flex md:hidden gap-3 mt-12 px-4 overflow-x-auto">
        {GEM_IMAGES.map((src, i) => (
          <img
            key={i}
            src={src}
            alt="Nail art"
            className="w-20 h-20 rounded-xl object-cover flex-shrink-0 shadow-md"
          />
        ))}
        <img
          src={FAIRY_IMG}
          alt="Hada del Bosque"
          className="w-20 h-20 rounded-xl object-cover flex-shrink-0 shadow-md"
        />
      </div>
    </section>
  )
}

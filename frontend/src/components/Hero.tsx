// Placeholder images — will be replaced with real Gratia assets
const FAIRY_PLACEHOLDER =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuCoc7AuQ2KIDK9NC-BselmmpYR8hjVGs3MEV20W88D_v5ugRm3XI3zYf9MnNCa8pFgTf6iOdMy7OQuW9csxmWJgTg5CS0ISRNcV17yhfB_ga8PDvaYXg9RlgKhk6PE2gM1qGehUmwQcJT9g5VkpSF6f6mtOf0w1mTyObQM4sNp1B7tWh3Al5NWkSoGNQCcNDa_rUoyfazd9oISP_ZVOj8iADak3t8yQul7fVfMMw30US14V8MTtTvU0ZwpDisrhiEA2_9Oer_1A9-c'

const GEM_PLACEHOLDERS = [
  'https://lh3.googleusercontent.com/aida-public/AB6AXuA-SKJg3Krqg_YNa20H0I_jxXpNUH1mZ67P1NQY3tLi5Nf0nD6YEzVYGnxgAPGx1jpii-lKTsD5g1Lfp4ELMUto0gV53DeQiZrs50qi3aNT3xvd6ikj1eUB5IKEBttfvTEj7tR4w-d89ye1UC2WHR-hHU4XwDhb8xo4wir6O2GOTRPuGsuRSuXu0VLoV_JSP3Vas5j9hmSX9nzRLvg_d_7f1G-ywhdldZsNGzOzhQge4dJjuZcVRXoVmmRB6PyvJseEkMaIQKtInB0',
  'https://lh3.googleusercontent.com/aida-public/AB6AXuDBorUp44Ge58M7VhYFYusna9ICBEdv9xg6t_9wf3kfq-W_qRpoioVSbPfAvMpe3EgfueuDqQ4x9LuMEOJi_hpsi6-IMk0VQbdT_OhlbSV7nNAGpz1mCzNobIo4hXhRAiDwDDmirvom-6A0wu0RMM1t3HoSG711RWkr4p8WMS-WTbpG0z2vhv8BgwE66RzP3GsZggnzL4hNgMSYAEingyonwVkjyqNI_v7_wnoTVrXlTAT-4AJOdIchwCFMukmLiITIVJH9nOXQhYk',
  'https://lh3.googleusercontent.com/aida-public/AB6AXuCDj-AWFEtyGUCh9ccMcj-Veri92jtq1GTftMYo1rP9mq30pHcOkanQWvAQ06E2KLrxxlLNhPDH2K1TrCDcZmZfC1Aztrgh1JPRV2sbyH749wxs_WLq_fvRm54psEJ84EYtTMtEEus24AT0HWUQLYxm4pblWOZ8S701v_h12kSmfXC2DQjdzZqAQvIJ_Bo7eWNwWRIHbaILDCyLm01JzrOnqhIifqFkS38oCZZ90B4fApf7c9KLz8Wisq7rwp0vK4qdSyB_UhLdZNA',
]

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 pt-20 pb-16 overflow-hidden bg-dark-bg">
      {/* 3-column layout: gems | text | fairy */}
      <div className="w-full max-w-6xl grid grid-cols-[auto_1fr_auto] md:grid-cols-[120px_1fr_200px] items-center gap-6 md:gap-10">
        {/* LEFT — Gem/nail art images */}
        <div className="hidden md:flex flex-col gap-4">
          {GEM_PLACEHOLDERS.map((src, i) => (
            <img
              key={i}
              src={src}
              alt="Nail art gem"
              className="w-24 h-24 rounded-2xl object-cover shadow-lg"
            />
          ))}
        </div>

        {/* CENTER — Main hero content */}
        <div className="text-center col-span-3 md:col-span-1">
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

        {/* RIGHT — Fairy mascot */}
        <div className="hidden md:flex justify-center">
          <img
            src={FAIRY_PLACEHOLDER}
            alt="Hada del Bosque — mascota de Gratia"
            className="w-44 h-56 rounded-2xl object-cover shadow-xl"
          />
        </div>
      </div>

      {/* Mobile: gems + fairy row below hero text */}
      <div className="flex md:hidden gap-3 mt-10 px-2 overflow-x-auto absolute bottom-8 left-0 right-0 justify-center">
        {GEM_PLACEHOLDERS.slice(0, 2).map((src, i) => (
          <img
            key={i}
            src={src}
            alt="Nail art"
            className="w-16 h-16 rounded-xl object-cover flex-shrink-0 shadow-md"
          />
        ))}
        <img
          src={FAIRY_PLACEHOLDER}
          alt="Hada del Bosque"
          className="w-16 h-16 rounded-xl object-cover flex-shrink-0 shadow-md"
        />
      </div>
    </section>
  )
}

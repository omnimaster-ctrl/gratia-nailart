const MAP_IMG =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuAHJcwSHX2biptzwDs9pS7-dBO9HVJE9G3fNLk-6JwVjZXst2m9HVvhBvq-4cNdRzZpijwLYInfq745XFZJySiTGbYLuD-uYIuB_0z7AJJvIpdEU3Qr66xUCCKRSJic9FHKXhwfkNgIA7Dh7ple-0rRXS9VCiTtCAvZpXxn8A3RQbVt3Yz2pleTV7IcgYyv9DBq_fbpXuiuw7mcjNC9zzc9apMAaA7-l9SBElww1Bdcmm7wRgldQ5cvv57wm4IQHWXCRvBWeOidFFM'

export default function Contact() {
  return (
    <section className="py-24 px-8 bg-surface">
      <div className="grid md:grid-cols-2 gap-16">
        {/* Schedule & Location */}
        <div>
          <h3 className="font-headline text-3xl text-primary mb-8">
            Horarios
          </h3>
          <ul className="space-y-4">
            {[
              ['Lunes - Viernes', '09:00 - 20:00', false],
              ['Sábados', '10:00 - 18:00', false],
              ['Domingos', 'Cerrado', true],
            ].map(([day, time, isClosed], i) => (
              <li
                key={i}
                className="flex justify-between border-b border-outline-variant/30 pb-2"
              >
                <span className="font-label text-xs uppercase text-on-surface-variant">
                  {day as string}
                </span>
                <span
                  className={`font-body font-bold ${isClosed ? 'text-secondary' : 'text-primary'}`}
                >
                  {time as string}
                </span>
              </li>
            ))}
          </ul>

          <div className="mt-12">
            <h3 className="font-headline text-3xl text-primary mb-4">
              Ubicación
            </h3>
            <p className="text-on-surface-variant font-light mb-6 italic">
              Morelia, Michoacán
            </p>
            <div className="w-full h-48 rounded-2xl bg-surface-high overflow-hidden relative">
              <img
                className="w-full h-full object-cover grayscale opacity-50"
                src={MAP_IMG}
                alt="Ubicación"
              />
              <div className="absolute inset-0 flex items-center justify-center">
                <span
                  className="material-symbols-outlined text-primary text-4xl"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  location_on
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Contact Links */}
        <div className="flex flex-col justify-center gap-8">
          <h3 className="font-headline text-3xl text-primary">Contacto</h3>
          <div className="space-y-6">
            <a className="flex items-center gap-6 group" href="#">
              <div className="w-12 h-12 rounded-full border border-secondary flex items-center justify-center group-hover:bg-secondary transition-colors">
                <span className="material-symbols-outlined text-secondary group-hover:text-on-secondary">
                  chat
                </span>
              </div>
              <div>
                <p className="font-label text-[10px] uppercase text-on-surface-variant">
                  WhatsApp
                </p>
                <p className="font-body text-primary font-bold">WhatsApp</p>
              </div>
            </a>
            <a
              className="flex items-center gap-6 group"
              href="https://instagram.com/gratia.nailart"
              target="_blank"
              rel="noopener noreferrer"
            >
              <div className="w-12 h-12 rounded-full border border-secondary flex items-center justify-center group-hover:bg-secondary transition-colors">
                <span className="material-symbols-outlined text-secondary group-hover:text-on-secondary">
                  camera
                </span>
              </div>
              <div>
                <p className="font-label text-[10px] uppercase text-on-surface-variant">
                  Instagram
                </p>
                <p className="font-body text-primary font-bold">
                  @gratia.nailart
                </p>
              </div>
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}

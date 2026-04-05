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
]

export default function Gallery() {
  return (
    <section className="py-20 px-6 bg-dark-bg">
      <h3 className="font-headline text-3xl md:text-4xl text-dark-text text-center italic mb-12">
        Mi Trabajo
      </h3>

      {/* Horizontal scrolling gallery */}
      <div className="flex gap-4 overflow-x-auto pb-4 snap-x scrollbar-hide">
        {galleryItems.map((item, i) => (
          <div
            key={i}
            className="relative flex-shrink-0 w-44 md:w-56 aspect-square rounded-2xl overflow-hidden group snap-center"
          >
            <img
              src={item.src}
              alt={item.label}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
            {/* Label overlay */}
            <div className="absolute bottom-0 left-0 right-0 bg-dark-deeper/75 backdrop-blur-sm px-3 py-2">
              <span className="font-label text-xs text-dark-text font-semibold">
                {item.label}
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

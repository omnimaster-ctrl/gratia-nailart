const images = {
  col1: [
    'https://lh3.googleusercontent.com/aida-public/AB6AXuA-SKJg3Krqg_YNa20H0I_jxXpNUH1mZ67P1NQY3tLi5Nf0nD6YEzVYGnxgAPGx1jpii-lKTsD5g1Lfp4ELMUto0gV53DeQiZrs50qi3aNT3xvd6ikj1eUB5IKEBttfvTEj7tR4w-d89ye1UC2WHR-hHU4XwDhb8xo4wir6O2GOTRPuGsuRSuXu0VLoV_JSP3Vas5j9hmSX9nzRLvg_d_7f1G-ywhdldZsNGzOzhQge4dJjuZcVRXoVmmRB6PyvJseEkMaIQKtInB0',
    'https://lh3.googleusercontent.com/aida-public/AB6AXuDBorUp44Ge58M7VhYFYusna9ICBEdv9xg6t_9wf3kfq-W_qRpoioVSbPfAvMpe3EgfueuDqQ4x9LuMEOJi_hpsi6-IMk0VQbdT_OhlbSV7nNAGpz1mCzNobIo4hXhRAiDwDDmirvom-6A0wu0RMM1t3HoSG711RWkr4p8WMS-WTbpG0z2vhv8BgwE66RzP3GsZggnzL4hNgMSYAEingyonwVkjyqNI_v7_wnoTVrXlTAT-4AJOdIchwCFMukmLiITIVJH9nOXQhYk',
  ],
  col2: [
    'https://lh3.googleusercontent.com/aida-public/AB6AXuCDj-AWFEtyGUCh9ccMcj-Veri92jtq1GTftMYo1rP9mq30pHcOkanQWvAQ06E2KLrxxlLNhPDH2K1TrCDcZmZfC1Aztrgh1JPRV2sbyH749wxs_WLq_fvRm54psEJ84EYtTMtEEus24AT0HWUQLYxm4pblWOZ8S701v_h12kSmfXC2DQjdzZqAQvIJ_Bo7eWNwWRIHbaILDCyLm01JzrOnqhIifqFkS38oCZZ90B4fApf7c9KLz8Wisq7rwp0vK4qdSyB_UhLdZNA',
    'https://lh3.googleusercontent.com/aida-public/AB6AXuAQgYTv8sIC4dupJj7pyIASRHVi8qDuCnmCfwOHq8jAO9zeHLk-lLg-ZIAWdkTndo93jvEGb8ZdD1h4nSveUXDJwt7__i5nmuj9CPA8bFWfALbw3vgMT5W6JhFHbtZlJZ1LDHSfcsuRhsnTmVHe3mv5MlqJmxoEZiIpQnrZp_4KOyCN16QdpPp0wHDAxD_0-HqQNqIOwhEWrP14SWwP3DWXDZKHFLD4c-rXyQhSqJpdsLT649inxFawzUzeuUE70cbkg1c6B8N4nzE',
  ],
}

export default function Gallery() {
  return (
    <section className="py-24 bg-surface overflow-hidden">
      <div className="px-6 mb-12 flex justify-between items-end">
        <h3 className="font-headline text-4xl text-primary italic">
          Portafolio
        </h3>
        <span className="font-label text-[10px] tracking-[0.3em] uppercase text-secondary">
          @GRATIA.NAILART
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 px-4">
        <div className="space-y-4 pt-12">
          <div className="rounded-xl overflow-hidden aspect-[3/4] shadow-sm">
            <img
              className="w-full h-full object-cover"
              src={images.col1[0]}
              alt="Nail art portfolio"
            />
          </div>
          <div className="rounded-xl overflow-hidden aspect-square shadow-sm">
            <img
              className="w-full h-full object-cover"
              src={images.col1[1]}
              alt="Nail art portfolio"
            />
          </div>
        </div>
        <div className="space-y-4">
          <div className="rounded-xl overflow-hidden aspect-square shadow-sm">
            <img
              className="w-full h-full object-cover"
              src={images.col2[0]}
              alt="Nail art portfolio"
            />
          </div>
          <div className="rounded-xl overflow-hidden aspect-[3/4] shadow-sm">
            <img
              className="w-full h-full object-cover"
              src={images.col2[1]}
              alt="Nail art portfolio"
            />
          </div>
        </div>
      </div>
    </section>
  )
}

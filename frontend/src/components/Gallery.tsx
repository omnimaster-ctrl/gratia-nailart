const galleryItems = [
  { src: '/assets/mascot/pointing.png', label: 'Nail Art' },
  { src: '/assets/fairy/flying.png', label: 'Hada del Bosque' },
  { src: '/assets/mascot/artist.png', label: 'Técnica mixta' },
  { src: '/assets/fairy/mushroom.png', label: 'Nail Art' },
  { src: '/assets/mascot/grinning.png', label: 'Técnica mixta' },
]

export default function Gallery() {
  return (
    <section className="py-20 px-6 bg-dark-bg">
      <h3 className="font-headline text-3xl md:text-4xl text-dark-text text-center italic mb-12">
        Mi Trabajo
      </h3>

      <div className="flex gap-5 overflow-x-auto pb-4 snap-x justify-center flex-wrap md:flex-nowrap">
        {galleryItems.map((item, i) => (
          <div
            key={i}
            className="flex-shrink-0 w-40 md:w-48 snap-center flex flex-col items-center gap-2"
          >
            <div className="w-full aspect-square rounded-2xl overflow-hidden group bg-dark-deeper/50">
              <img
                src={item.src}
                alt={item.label}
                className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300 p-2"
              />
            </div>
            <span className="font-label text-xs text-dark-muted italic">
              {item.label}
            </span>
          </div>
        ))}
      </div>
    </section>
  )
}

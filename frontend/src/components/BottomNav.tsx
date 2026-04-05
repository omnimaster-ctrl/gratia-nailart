const items = [
  { icon: 'auto_awesome', label: 'Inicio', active: true },
  { icon: 'brush', label: 'Servicios', active: false },
  { icon: 'calendar_month', label: 'Cita', active: false },
  { icon: 'collections_bookmark', label: 'Galería', active: false },
]

export default function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 w-full flex justify-around items-center px-4 pb-4 pt-2 bg-background/80 glass-nav z-50 shadow-[0_-4px_20px_rgba(28,28,24,0.04)] rounded-t-3xl">
      {items.map((item) => (
        <button
          key={item.label}
          className={`flex flex-col items-center justify-center p-2 transition-colors scale-90 ${
            item.active
              ? 'bg-primary text-on-primary rounded-full p-3'
              : 'text-on-surface-variant hover:text-secondary'
          }`}
        >
          <span className="material-symbols-outlined">{item.icon}</span>
          <span className="font-label text-[8px] uppercase tracking-tighter mt-1">
            {item.label}
          </span>
        </button>
      ))}
    </nav>
  )
}

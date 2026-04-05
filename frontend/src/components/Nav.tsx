export default function Nav() {
  return (
    <header className="fixed top-0 w-full z-50 bg-background/60 glass-nav flex justify-between items-center px-6 h-16">
      <button className="material-symbols-outlined text-primary hover:opacity-70 transition-opacity">
        menu
      </button>
      <h1 className="font-headline italic tracking-[0.2em] text-xl font-bold text-primary uppercase">
        GRATIA NAIL ART
      </h1>
      <button className="material-symbols-outlined text-primary hover:opacity-70 transition-opacity">
        shopping_bag
      </button>
    </header>
  )
}

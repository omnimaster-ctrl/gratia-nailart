import WizardBooking from './WizardBooking'

export default function BookingPage() {
  return (
    <div
      className="min-h-screen flex items-center justify-center px-4 py-12"
      style={{
        background: `
          radial-gradient(ellipse 80% 60% at 50% 20%, rgba(205,162,85,0.08) 0%, transparent 60%),
          linear-gradient(180deg, #2a2e25 0%, #3d4435 40%, #3d4435 60%, #2a2e25 100%)
        `,
      }}
    >
      {/* Decorative particles */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${15 + i * 14}%`,
              bottom: `${10 + (i % 3) * 20}%`,
              width: `${3 + (i % 3)}px`,
              height: `${3 + (i % 3)}px`,
              opacity: 0.4,
              animationDelay: `${i * 0.8}s`,
            }}
          />
        ))}
      </div>

      {/* Back to home link */}
      <a
        href="/"
        className="fixed top-6 left-6 z-20 flex items-center gap-2 px-4 py-2 rounded-full bg-dark-deepest/80 border border-gold/20 text-gold font-label text-sm font-bold hover:bg-dark-deepest hover:border-gold/40 transition-all backdrop-blur-sm"
      >
        ← Gratia Nail Art
      </a>

      <div className="relative z-10 w-full">
        <WizardBooking />
      </div>
    </div>
  )
}

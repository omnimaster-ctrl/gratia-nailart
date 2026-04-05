import Nav from './components/Nav'
import Hero from './components/Hero'
import Services from './components/Services'
import Gallery from './components/Gallery'
import Process from './components/Process'
import Testimonials from './components/Testimonials'
import Contact from './components/Contact'
import Footer from './components/Footer'
import BottomNav from './components/BottomNav'

export default function App() {
  return (
    <>
      <Nav />
      <main className="pt-16 pb-24">
        <Hero />
        <Services />
        <Gallery />
        <Process />
        <Testimonials />
        <Contact />
      </main>
      <Footer />
      <BottomNav />
    </>
  )
}

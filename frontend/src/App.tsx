import Nav from './components/Nav'
import Hero from './components/Hero'
import Gallery from './components/Gallery'
import CtaBanner from './components/CtaBanner'
import MasDeGratia from './components/MasDeGratia'
import Footer from './components/Footer'

export default function App() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <Gallery />
        <CtaBanner />
        <MasDeGratia />
      </main>
      <Footer />
    </>
  )
}

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Nav from './components/Nav'
import Hero from './components/Hero'
import Gallery from './components/Gallery'
import CtaBanner from './components/CtaBanner'
import MasDeGratia from './components/MasDeGratia'
import Footer from './components/Footer'
import BookingPage from './components/BookingPage'

function LandingPage() {
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

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/booking" element={<BookingPage />} />
      </Routes>
    </BrowserRouter>
  )
}

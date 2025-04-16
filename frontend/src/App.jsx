// src/App.jsx
import { useState } from 'react'
import { useRef } from 'react'
import { Dialog, DialogPanel } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import Header from './components/Header'
import Hero from './components/Hero'
import MatchSection from './components/MatchSection'
import ResultsSection from './components/ResultsSection'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import AiChat from './pages/AiChat'

export default function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(false)
  const [visibleCount, setVisibleCount] = useState(5)
  const [resetCounter, setResetCounter] = useState(0)
  const resultsRef = useRef(null)
  const matchSectionRef = useRef(null)

  const resetSearch = () => {
    setMatches([])
    setVisibleCount(5)
    setResetCounter(prev => prev + 1) // Increment the counter to trigger a re-render
  }

  const loadMore = () => {
    setVisibleCount(prev => prev + 5)
  }

  const handleScrollToMatch = () => {
    matchSectionRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleMatchSearch = async (input) => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/match', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_input: input,
          top_n: 30,
        })
      })

      const data = await response.json()
      setMatches(data.matches || [])
      setVisibleCount(5) // Reset visible count when new matches are fetched
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' }) // 👈 Smooth scroll!
      }, 100) // Vent lidt så elementet når at blive vist
    } catch (error) {
      console.error('Error fetching match results:', error)
    } finally {
      setLoading(false)
    }
  } 

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div className="bg-white">
              <Header />
              <Hero onScrollToMatch={handleScrollToMatch} />
              <MatchSection
                onSearch={handleMatchSearch}
                loading={loading}
                scrollRef={matchSectionRef}
                resetCounter={resetCounter}
              />
              {matches.length > 0 && (
                <ResultsSection
                  matches={matches}
                  scrollRef={resultsRef}
                  visibleCount={visibleCount}
                  loadMore={loadMore}
                  onReset={resetSearch}
                />
              )}
            </div>
          }
        />
        <Route path="/ai/chat/:studyName" element={<AiChat />} />
      </Routes>
    </Router>
  )
}

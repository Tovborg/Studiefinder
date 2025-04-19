// import src/components/MatchSection.jsx
import { useState } from 'react'
import { useEffect } from 'react'

export default function MatchSection({ onSearch, loading, resetCounter, scrollRef }) {
  const [input, setInput] = useState('')
  
  useEffect(() => {
    setInput('') // Reset input when resetCounter changes
  }, [resetCounter])
    const handleSubmit = (e) => {
        e.preventDefault()
        if (input.trim() !== '') {
            onSearch(input)
        }
    }

  return (
    <section
      id="start"
      className="isolate bg-gradient-to-b from-[#f4f4fc] via-slate-50 to-indigo-50 px-6 py-24 sm:py-32 lg:px-8 min-h-screen"
    >
      <div className="mx-auto max-w-2xl text-center">
        <img
            src="/images/studie_illustration.png"
            ref={scrollRef}
            alt="Match illustration"
            className="mx-auto mb-8 w-120 rounded-xl shadow-md"
        />
        <h2 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-gray-900">
          Beskriv dine <span className="text-indigo-600">interesser</span>
        </h2>
        <div className="mt-2">
          <span className="inline-block text-sm text-white bg-indigo-500 rounded-full px-3 py-1">
            🤖 Drevet af AI
          </span>
        </div>
        <p className="mt-4 text-lg text-gray-600">
          Fortæl os hvad du interesserer dig for – fx fag, emner eller arbejdstyper – så matcher vi dig med relevante bacheloruddannelser.
        </p>
      </div>
      <form onSubmit={handleSubmit} className="mx-auto mt-16 max-w-xl sm:mt-20">
        <label htmlFor="interesse" className="block text-sm font-medium text-gray-900">
          Hvad interesserer du dig for?
        </label>
        <textarea
          id="interesse"
          name="interesse"
          rows={5}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Jeg kan godt lide teknologi og matematik, og vil gerne arbejde med programmering eller kunstig intelligens."
          className="mt-2 block w-full rounded-lg bg-white px-4 py-3 text-base text-gray-900 shadow-sm transition-all duration-200 outline-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:outline-indigo-600"
        />
        <div className="mt-6">
        <button
          type="submit"
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 hover:scale-[1.02] transition-all duration-200 ease-in-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {loading && (
            <svg
              className="h-5 w-5 animate-spin text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
              />
            </svg>
          )}
          {loading ? 'Finder uddannelser...' : 'Find uddannelser'}
        </button>
        </div>
      </form>
    </section>
  )
} 

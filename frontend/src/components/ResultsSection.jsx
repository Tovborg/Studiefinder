// src/components/ResultsSection.jsx
import MatchCard from './MatchCard'

export default function ResultsSection({ matches, scrollRef, visibleCount, loadMore, onReset }) {
  return (
    <section
      ref={scrollRef}
      className="bg-gradient-to-b from-indigo-50 via-slate-100 to-purple-100 px-6 py-8 sm:py-24 lg:px-8 min-h-screen"
    >
      <div className="mx-auto max-w-3xl">
        <div className="flex flex-col items-center justify-center mb-10">
          <div className="text-5xl mb-2">🧠</div>
          <h2 className="text-4xl font-extrabold text-gray-900 text-center">
            Vi tror disse passer perfekt til netop dig!
          </h2>
          <p className="text-lg text-gray-600 text-center mt-2 max-w-xl">
            Vi har analyseret dine interesser og fundet uddannelser, der matcher – klar til at udforske mulighederne?
          </p>
        </div>

        <div className="space-y-6">
          {matches.slice(0, visibleCount).map((result, idx) => (
            <div
              key={idx}
              className="opacity-0 translate-y-4 animate-fade-in hover:scale-[1.01] hover:shadow-xl transition-transform duration-200"
              style={{ animationDelay: `${idx * 1}ms`, animationFillMode: 'forwards' }}
            >
              <MatchCard
                title={result.titel || result.title}
                description={result.beskrivelse || result.description}
                url={result.url}
                score={result.match_score || result.score}
                rank={idx}
              />
            </div>
          ))}
        </div>

        {/* Vis knappen kun hvis der er flere matches at vise */}
        {visibleCount < matches.length && (
          <div className="mt-10 text-center">
            <button
              onClick={loadMore}
              className="inline-block rounded-full bg-indigo-600 text-white text-sm font-semibold px-6 py-2 shadow-sm hover:bg-indigo-500 transition-all duration-200"
            >
              ✨ Vis flere anbefalinger
            </button>
          </div>
        )}

        <p className="mt-12 text-center text-sm text-gray-500">
          Stadig ikke tilfreds?{' '}
          <a
            href="#start"
            onClick={onReset}
            className="text-indigo-600 font-medium hover:underline cursor-pointer"
          >
            Beskriv dine interesser på en ny måde
          </a>
        </p>
      </div>
    </section>
  )
}
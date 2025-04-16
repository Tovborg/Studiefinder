import { Link } from 'react-router-dom'

export default function MatchCard({ title, description, url, score, rank }) {
  const descriptionMaxLength = 130;
  const shortenedDescription =
    description.length > descriptionMaxLength
      ? description.slice(0, descriptionMaxLength).trim() + '...'
      : description;

  return (
    <div className="relative flex flex-col md:flex-row rounded-xl overflow-hidden shadow-md border border-gray-200 bg-white hover:shadow-lg hover:ring-2 hover:ring-indigo-100 transition-all duration-300">
      <div className="p-4 flex-1">
      <h3 className="text-xl sm:text-lg font-bold text-gray-900 tracking-tight font-sans">
        {title}
      </h3>
      <p className="mt-2 text-sm text-gray-600 leading-relaxed font-light">
        {shortenedDescription}
      </p>

        <div className="mt-2 flex flex-col sm:flex-row sm:items-center sm:justify-between text-sm text-gray-500 gap-1">
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:underline hover:text-indigo-800"
        >
          Læs mere på UG.dk <span aria-hidden="true">↗</span>
        </a>
        <Link
          to={`/ai/chat/${encodeURIComponent(title)}`}
          className="mt-2 inline-flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white text-sm rounded-md shadow-md hover:shadow-lg hover:brightness-105 transition-all duration-200"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 20l9-5-9-5-9 5 9 5zm0-10V4m0 0l3 3m-3-3L9 7" />
          </svg>
          Chat med AI
        </Link>
          {/* Badge */}
          
          <span
            className={`
              mt-2 sm:mt-0
              inline-block sm:absolute
              sm:top-3 sm:right-3
              text-sm font-semibold px-3 py-1 rounded-full shadow-sm
              ${
                rank === 0
                  ? 'bg-yellow-100 text-yellow-800'
                  : rank === 1
                  ? 'bg-gray-200 text-gray-800'
                  : rank === 2
                  ? 'bg-orange-200 text-orange-800'
                  : 'bg-indigo-100 text-indigo-700'
              }
            `}
          >
            {rank === 0
              ? '🥇 #1 anbefaling'
              : rank === 1
              ? '🥈 #2 anbefaling'
              : rank === 2
              ? '🥉 #3 anbefaling'
              : `#${rank + 1} anbefaling`}
          </span>
        </div>
      </div>
    </div>
  );
}
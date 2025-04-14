import { useState } from 'react'
import { Dialog, DialogPanel } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'

export default function Hero({ onScrollToMatch }) {
  return (
    <div className="relative isolate px-6 pt-14 lg:px-8 min-h-screen overflow-hidden">
      {/* Top-baggrundseffekt */}
      <div
        aria-hidden="true"
        className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
      >
        <div
          style={{
            clipPath:
              'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
          }}
          className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-pink-300 to-indigo-300 opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
        />
      </div>

      {/* Indholdet */}
      <div className="relative z-10 mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
        <div className="text-center">
        <h1 className="text-5xl font-semibold tracking-tight text-balance break-words text-gray-900 sm:text-7xl">
          Find din drømmeuddannelse med{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 via-fuchsia-500 to-pink-500">
            Ai
          </span>
        </h1>
          <p className="mt-6 text-lg text-gray-600">
            En intelligent studievejleder til gymnasieelever – matcher dine interesser med bacheloruddannelser.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
          <button
            onClick={onScrollToMatch}
            className="rounded-md bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
          >
            Kom i gang
          </button>
            <a href="#" className="text-sm font-semibold text-gray-900">
              Læs mere <span aria-hidden="true">&rarr;</span>
            </a>
          </div>
        </div>
      </div>

      {/* Gradient i bunden */}
      <div className="absolute inset-x-0 bottom-0 h-64 bg-gradient-to-b from-white to-[#f4f4fc] z-[-1] pointer-events-none" />
    </div>
  )
}
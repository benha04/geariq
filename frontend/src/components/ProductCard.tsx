import React from 'react'

type Candidate = {
  title?: string
  image?: string
  price?: number
  retailer?: string
  url?: string
  score_breakdown?: { total?: number }
}

export default function ProductCard({ candidate }: { candidate: Candidate }) {
  const score = Math.round((candidate.score_breakdown?.total ?? 0) * 100)

  return (
    <div className="border rounded-md p-3 bg-white shadow-sm">
      <a href={candidate.url} target="_blank" rel="noreferrer" className="block">
        <div className="w-full h-40 bg-gray-100 flex items-center justify-center overflow-hidden mb-3">
          {candidate.image ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={candidate.image} alt={candidate.title} className="max-h-full object-contain" />
          ) : (
            <div className="text-gray-400">No image</div>
          )}
        </div>
      </a>

      <div className="text-sm text-gray-700 font-medium mb-1">{candidate.title}</div>
      <div className="text-sm text-gray-500 mb-2">{candidate.retailer ?? 'Unknown retailer'}</div>
      <div className="text-lg font-semibold mb-2">{candidate.price ? `$${candidate.price}` : '—'}</div>

      <div className="mb-2">
        <label className="text-xs text-gray-500">Match rating: {score}%</label>
        <input type="range" min={0} max={100} value={score} readOnly className="w-full" />
      </div>

      <div className="text-xs text-gray-400">Score: {score} — closer to 100 means better match</div>
    </div>
  )
}

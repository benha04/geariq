import { useState } from 'react'
import SearchBar from '@/components/SearchBar'

export default function Home() {
  const [result, setResult] = useState<any | null>(null)
  return (
    <main className="min-h-screen p-8 flex flex-col items-center gap-8">
      <h1 className="text-3xl font-bold">GearIQ</h1>
      <p className="text-gray-600">Find the best product for you — not just the cheapest item.</p>
      <SearchBar onResult={setResult} />
      {result && (
        <div className="w-full max-w-3xl grid gap-4">
          {result.best && (
            <div className="border rounded-xl p-4">
              <h2 className="font-semibold">Best Match</h2>
              <a className="underline" href={result.best.url} target="_blank" rel="noreferrer">{result.best.title}</a>
              <div className="text-sm text-gray-600">{result.best.retailer} • ${result.best.price} • ⭐ {result.best.rating}</div>
            </div>
          )}
          <div className="border rounded-xl p-4">
            <h3 className="font-medium mb-2">All Candidates</h3>
            <ul className="list-disc ml-5">
              {result.candidates.map((c:any, i:number)=> (
                <li key={i}><a className="underline" href={c.url} target="_blank" rel="noreferrer">{c.title}</a> — {c.retailer} • ${c.price} • ⭐ {c.rating}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </main>
  )
}

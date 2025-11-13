import { useState } from 'react'
import SearchBar from '@/components/SearchBar'

export default function Home() {
  const [result, setResult] = useState<any | null>(null)
  return (
    <main className="min-h-screen bg-white text-gray-900">
      <header className="max-w-6xl mx-auto p-8 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-pink-500 rounded-md flex items-center justify-center text-white font-bold">GQ</div>
          <h1 className="text-2xl font-semibold">GearIQ</h1>
        </div>
        <nav className="flex items-center gap-4 text-sm text-gray-600">
          <a href="#features" className="hover:underline">Features</a>
          <a href="#install" className="hover:underline">Get Started</a>
          <a href="#demo" className="hover:underline">Try Demo</a>
        </nav>
      </header>

      <section className="bg-gradient-to-b from-white to-gray-50">
        <div className="max-w-6xl mx-auto py-20 px-6 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-4xl font-extrabold leading-tight">Find the best gear, instantly.</h2>
            <p className="mt-4 text-lg text-gray-600">Describe what you need in plain language — we search across retailers, surface the best value product right now, and explain why.</p>

            <div className="mt-8 flex gap-4">
              <a href="#demo" className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-md shadow hover:bg-indigo-700">Try Demo</a>
              <a href="#install" className="inline-flex items-center px-6 py-3 border rounded-md text-gray-700 hover:bg-gray-100">Get Started</a>
              <TrackButton />
            </div>

            <div className="mt-8 text-sm text-gray-500">
              <strong>Examples:</strong> "best MIPS bike helmet under $150 with 2-day delivery", "50mm lens under $400".
            </div>
          </div>

          <div className="bg-white border rounded-2xl p-6 shadow-sm">
            <h4 className="text-sm text-gray-500">Live demo</h4>
            <div id="demo" className="mt-4">
              <SearchBar onResult={setResult} />
              {result && (
                <div className="mt-4">
                  {result.best && (
                    <div className="border rounded-lg p-4 mb-4">
                      <div className="text-sm text-gray-500">Best Match</div>
                      <a className="text-lg font-medium text-indigo-600" href={result.best.url} target="_blank" rel="noreferrer">{result.best.title}</a>
                      <div className="text-sm text-gray-600">{result.best.retailer} • ${result.best.price} • ⭐ {result.best.rating}</div>
                    </div>
                  )}
                  <div className="border rounded-lg p-3">
                    <div className="text-sm text-gray-500 mb-2">Alternatives</div>
                    <ul className="list-disc ml-5 text-sm text-gray-700">
                      {result.candidates.map((c:any, i:number) => (
                        <li key={i}><a className="text-indigo-600 underline" href={c.url} target="_blank" rel="noreferrer">{c.title}</a> — {c.retailer} • ${c.price}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="max-w-6xl mx-auto py-16 px-6">
        <h3 className="text-2xl font-semibold">Features</h3>
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 border rounded-lg">
            <h4 className="font-medium">Natural language search</h4>
            <p className="mt-2 text-sm text-gray-600">Describe your needs and constraints — we parse budget, shipping, attributes, and brand preferences.</p>
          </div>
          <div className="p-6 border rounded-lg">
            <h4 className="font-medium">Transparent ranking</h4>
            <p className="mt-2 text-sm text-gray-600">We show why a product ranked #1: price, features matched, delivery ETA, and rating.</p>
          </div>
          <div className="p-6 border rounded-lg">
            <h4 className="font-medium">Cross-retailer aggregation</h4>
            <p className="mt-2 text-sm text-gray-600">We aggregate offers from multiple affiliate networks to surface the best value in one place.</p>
          </div>
        </div>
      </section>

      <section id="install" className="bg-white border-t py-12">
        <div className="max-w-6xl mx-auto px-6">
          <h4 className="text-xl font-semibold">Get started</h4>
          <p className="mt-3 text-gray-600">Install locally or use our API to integrate GearIQ into your site.</p>
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 border rounded-lg bg-gray-50">
              <h5 className="font-medium">Install CLI</h5>
              <pre className="mt-3 bg-white p-3 rounded text-sm">pip install geariq-cli</pre>
            </div>
            <div className="p-6 border rounded-lg bg-gray-50">
              <h5 className="font-medium">API</h5>
              <pre className="mt-3 bg-white p-3 rounded text-sm">GET /v1/search?q=best+helmet+under+150</pre>
            </div>
          </div>
        </div>
      </section>

      <footer className="max-w-6xl mx-auto p-8 text-sm text-gray-500">
        © {new Date().getFullYear()} GearIQ — Open source
      </footer>
    </main>
  )
}


function TrackButton() {
  const [loading, setLoading] = useState(false)
  const [done, setDone] = useState(false)
  const track = async () => {
    setLoading(true)
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'}/v1/track`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ q: 'MIPS bike helmet', budget: 150, contact: 'demo@example.com' })
      })
      setDone(true)
    } catch (e) {
      console.error(e)
    }
    setLoading(false)
  }
  return (
    <button onClick={track} disabled={loading || done} className="inline-flex items-center px-4 py-2 bg-yellow-400 text-black rounded-md">{done? 'Tracking enabled' : (loading? '...':'Track this category')}</button>
  )
}

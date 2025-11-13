import { useState } from 'react'
import SearchBar from '@/components/SearchBar'

export default function Home() {
  const [result, setResult] = useState<any | null>(null)
  return (
    <main className="min-h-screen bg-gradient-to-b from-white via-gray-50 to-gray-100 text-gray-900">
      <header className="max-w-6xl mx-auto p-8 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-gradient-to-br from-indigo-600 to-pink-500 rounded-lg flex items-center justify-center text-white font-extrabold">GQ</div>
          <div>
            <h1 className="text-2xl font-semibold">GearIQ</h1>
            <div className="text-xs text-gray-500">WIP — product demo & investor preview</div>
          </div>
        </div>
        <nav className="flex items-center gap-6 text-sm text-gray-600">
          <a href="#features" className="hover:underline">Features</a>
          <a href="#vision" className="hover:underline">Vision</a>
          <a href="#demo" className="hover:underline">Try Demo</a>
        </nav>
      </header>

      <section className="max-w-6xl mx-auto px-6 py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div>
            <div className="inline-flex items-center gap-3 mb-4">
              <span className="px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 text-xs font-semibold">Work in progress</span>
              <span className="text-xs text-gray-500">Proof of concept for partners & integrators</span>
            </div>

            <h2 className="text-5xl font-extrabold leading-tight">Find the best gear, not just the cheapest.</h2>
            <p className="mt-6 text-lg text-gray-700">Describe what you need in plain language — we search across retailers, rank offers by value, and explain exactly why the top result is the best choice. Built for power shoppers, publishers, and partners who want transparent cross-retailer discovery.</p>

            <div className="mt-8 flex gap-4 items-center">
              <a href="#demo" className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white rounded-md shadow hover:bg-indigo-700">Try the demo</a>
              <a href="#vision" className="inline-flex items-center px-6 py-3 border rounded-md text-gray-700 hover:bg-gray-100">See our vision</a>
              <TrackButton />
            </div>

            <div className="mt-6 text-sm text-gray-500">
              <strong>Quick examples:</strong> "best MIPS bike helmet under $150 with 2-day delivery", "studio headphones under $250 with free shipping".
            </div>
          </div>

          <div className="bg-white border rounded-3xl p-8 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-gray-500">Live demo (read-only)</div>
                <div className="text-xs text-gray-400">No backend required for this demo — results come from our development catalog.</div>
              </div>
              <div className="text-sm text-gray-400">v0.1</div>
            </div>

            <div id="demo" className="mt-6">
              <SearchBar onResult={setResult} />
              {result && (
                <div className="mt-6">
                  {result.error && (
                    <div className="mb-4 p-3 rounded bg-red-50 border text-sm text-red-700">{result.error}</div>
                  )}
                  {result.best && (
                    <div className="border rounded-lg p-4 mb-4 bg-gray-50 flex gap-4 items-start">
                      {result.best.image && (
                        <img src={result.best.image} className="w-28 h-28 object-cover rounded-md" alt="best" />
                      )}
                      <div>
                        <div className="text-sm text-gray-500">Best Match</div>
                        <a className="text-lg font-semibold text-indigo-600" href={result.best.url} target="_blank" rel="noreferrer">{result.best.title}</a>
                        <div className="text-sm text-gray-600">{result.best.retailer} • ${result.best.price} • ⭐ {result.best.rating}</div>
                        <div className="mt-2 text-xs text-gray-500">Reason: {result.rationale?.why || 'Matches features & price'}</div>
                      </div>
                    </div>
                  )}

                  <div className="border rounded-lg p-3">
                    <div className="text-sm text-gray-500 mb-2">Alternatives</div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {(result.candidates || []).map((c:any, i:number) => (
                        <div key={i} className="flex gap-3 items-center p-2 border rounded">
                          {c.image ? (
                            <img src={c.image} className="w-16 h-16 object-cover rounded" alt={c.title} />
                          ) : (
                            <div className="w-16 h-16 bg-gray-100 rounded flex items-center justify-center text-xs text-gray-400">No image</div>
                          )}
                          <div className="text-sm">
                            <a className="text-indigo-600 font-medium" href={c.url} target="_blank" rel="noreferrer">{c.title}</a>
                            <div className="text-xs text-gray-600">{c.retailer} • ${c.price}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      <section id="vision" className="max-w-6xl mx-auto px-6 py-16">
        <div className="bg-gradient-to-r from-indigo-50 to-pink-50 p-8 rounded-2xl border">
          <h3 className="text-2xl font-semibold">Our product vision</h3>
          <p className="mt-4 text-gray-700">GearIQ helps users and partners discover the single best product for their needs across retailers, not just the cheapest listing. We combine:</p>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4">
              <h4 className="font-medium">1. Natural language understanding</h4>
              <p className="text-sm text-gray-600 mt-2">Parse budgets, delivery constraints, brands, and product attributes from free text.</p>
            </div>
            <div className="p-4">
              <h4 className="font-medium">2. Cross-retailer signals</h4>
              <p className="text-sm text-gray-600 mt-2">Aggregate offers, ratings, and shipping estimates to compute a transparent value score.</p>
            </div>
            <div className="p-4">
              <h4 className="font-medium">3. Explainable ranking</h4>
              <p className="text-sm text-gray-600 mt-2">Return human-readable rationale for why a result is best—price, matched features, ETA, and quality.</p>
            </div>
          </div>

          <div className="mt-6 text-sm text-gray-700">For partners (publishers, affiliate networks, marketplaces) we provide a small, well-documented API that returns ranked candidates and granular scoring rationale so you can build trust with users and increase conversion.</div>
        </div>
      </section>

      <section id="features" className="max-w-6xl mx-auto py-12 px-6">
        <h3 className="text-2xl font-semibold">Why this matters</h3>
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 border rounded-lg bg-white">
            <h4 className="font-medium">Better decisions</h4>
            <p className="mt-2 text-sm text-gray-600">Users get recommendations that balance price, features and delivery, not just the lowest SKU price.</p>
          </div>
          <div className="p-6 border rounded-lg bg-white">
            <h4 className="font-medium">Higher intent</h4>
            <p className="mt-2 text-sm text-gray-600">Explainable results increase user confidence and conversion for partners.</p>
          </div>
          <div className="p-6 border rounded-lg bg-white">
            <h4 className="font-medium">Easy integration</h4>
            <p className="mt-2 text-sm text-gray-600">A single API returns ranked candidates plus the score breakdown you can display to users.</p>
          </div>
        </div>
      </section>

      <footer className="max-w-6xl mx-auto p-8 text-sm text-gray-500">
        <div className="flex items-center justify-between">
          <div>© {new Date().getFullYear()} GearIQ — Work-in-progress</div>
          <div className="text-xs text-gray-400">Contact: hello@geariq.example</div>
        </div>
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

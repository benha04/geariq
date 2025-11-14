import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import ProductCard from '@/components/ProductCard'

type Candidate = any

export default function ResultsPage() {
  const router = useRouter()
  const { q, budget } = router.query
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [best, setBest] = useState<Candidate | null>(null)

  useEffect(() => {
    if (!q) return
    const fetch = async () => {
      setLoading(true)
      setError(null)
      try {
        const params: any = { q: String(q) }
        if (budget) params.budget = String(budget)
        const { data } = await api.get('/v1/search', { params })
        setCandidates(data.candidates || [])
        setBest(data.best || null)
      } catch (err: any) {
        console.error('Results fetch error', err)
        const serverDetail = err?.response?.data ? JSON.stringify(err.response.data) : ''
        setError(err?.message ? `${err.message} ${serverDetail}` : 'Failed to fetch results')
      } finally {
        setLoading(false)
      }
    }

    fetch()
  }, [q, budget])

  return (
    <div className="min-h-screen p-6 bg-gray-50">
      <div className="max-w-5xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Results for "{q}"</h1>
          {budget && <div className="text-sm text-gray-500">Budget: ${budget}</div>}
        </div>

        {loading && <div className="py-6 text-center">Loading results…</div>}

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded">{error}</div>
        )}

        {best && (
          <div className="mb-6">
            <h2 className="text-lg font-semibold">Top pick</h2>
            <div className="mt-3">
              <ProductCard candidate={best} />
            </div>
          </div>
        )}

        <div>
          <h2 className="text-lg font-semibold mb-3">Other matches</h2>
          {candidates.length === 0 && !loading && <div className="text-sm text-gray-500">No matches found.</div>}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {candidates.map((c: Candidate, i: number) => (
              <ProductCard key={c.url ?? i} candidate={c} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

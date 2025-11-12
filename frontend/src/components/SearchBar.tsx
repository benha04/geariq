import { useState } from 'react'
import { api } from '@/lib/api'

type Props = { onResult: (data: any) => void }
export default function SearchBar({ onResult }: Props) {
  const [q, setQ] = useState('MIPS bike helmet')
  const [budget, setBudget] = useState('150')
  const [loading, setLoading] = useState(false)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    const { data } = await api.get('/v1/search', { params: { q, budget } })
    onResult(data)
    setLoading(false)
  }

  return (
    <form onSubmit={submit} className="flex gap-2 w-full max-w-3xl">
      <input className="flex-1 border rounded-xl px-3 py-2" value={q} onChange={e=>setQ(e.target.value)} placeholder="Describe what you need…" />
      <input className="w-28 border rounded-xl px-3 py-2" value={budget} onChange={e=>setBudget(e.target.value)} placeholder="$" />
      <button className="rounded-xl px-4 py-2 bg-black text-white" disabled={loading}>{loading? 'Searching…':'Search'}</button>
    </form>
  )
}

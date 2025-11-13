import { useEffect, useState } from 'react'

export default function TracksPage() {
  const [rules, setRules] = useState<any[]>([])
  useEffect(()=>{
    fetch((process.env.NEXT_PUBLIC_API_BASE||'http://localhost:8000')+'/v1/admin/tracks')
      .then(r=>r.json())
      .then(j=>setRules(j.rules||[]))
      .catch(console.error)
  },[])
  return (
    <main className="max-w-4xl mx-auto p-8">
      <h1 className="text-2xl font-semibold mb-4">Track rules</h1>
      <div className="space-y-3">
        {rules.length===0 && <div className="text-sm text-gray-500">No rules yet</div>}
        {rules.map((r:any)=> (
          <div key={r.id} className="p-3 border rounded">
            <div className="font-medium">{r.q}</div>
            <div className="text-sm text-gray-600">Budget: {r.budget} • Contact: {r.contact}</div>
          </div>
        ))}
      </div>
    </main>
  )
}

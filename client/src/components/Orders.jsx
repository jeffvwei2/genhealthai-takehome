import { useEffect, useState } from 'react'

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [form, setForm] = useState({ patient_first_name: '', patient_last_name: '', dob: '', status: 'new' })
  const [loading, setLoading] = useState(false)

  useEffect(() => { refresh() }, [])

  async function refresh() {
    const res = await fetch('/api/orders/')
    const data = await res.json()
    setOrders(data)
  }

  async function submit(e) {
    e.preventDefault()
    setLoading(true)
    await fetch('/api/orders/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    setForm({ patient_first_name: '', patient_last_name: '', dob: '', status: 'new' })
    await refresh()
    setLoading(false)
  }

  async function remove(id) {
    await fetch(`/api/orders/${id}/`, { method: 'DELETE' })
    await refresh()
  }

  return (
    <div className="space-y-6">
      <form onSubmit={submit} className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
        <input className="border rounded px-3 py-2" placeholder="First name" value={form.patient_first_name} onChange={e=>setForm(f=>({...f, patient_first_name:e.target.value}))} required />
        <input className="border rounded px-3 py-2" placeholder="Last name" value={form.patient_last_name} onChange={e=>setForm(f=>({...f, patient_last_name:e.target.value}))} required />
        <input className="border rounded px-3 py-2" type="date" value={form.dob} onChange={e=>setForm(f=>({...f, dob:e.target.value}))} />
        <select className="border rounded px-3 py-2" value={form.status} onChange={e=>setForm(f=>({...f, status:e.target.value}))}>
          <option value="new">new</option>
          <option value="processing">processing</option>
          <option value="complete">complete</option>
        </select>
        <div className="sm:col-span-2">
          <button disabled={loading} className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">{loading? 'Saving...':'Create Order'}</button>
        </div>
      </form>

      <ul className="divide-y rounded-lg border border-gray-200 overflow-hidden bg-white shadow-sm">
        {orders.map(o => (
          <li key={o.id} className="p-4 flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">{o.patient_first_name} {o.patient_last_name}</p>
              <p className="text-xs text-gray-500">DOB: {o.dob || '—'} • Status: {o.status}</p>
            </div>
            <button onClick={()=>remove(o.id)} className="text-red-600 hover:text-red-700">Delete</button>
          </li>
        ))}
        {orders.length === 0 && <li className="p-6 text-center text-gray-500">No orders yet</li>}
      </ul>
    </div>
  )
}



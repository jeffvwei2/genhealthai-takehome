import { useState } from 'react'

export default function UploadPDF() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function submit(e) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    const form = new FormData()
    form.append('file', file)
    const res = await fetch('/api/upload/', { method: 'POST', body: form })
    const data = await res.json()
    setResult(data.extracted || data)
    setLoading(false)
  }

  return (
    <div className="space-y-4">
      <form onSubmit={submit} className="flex items-center gap-3 bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
        <label htmlFor="file-upload" className="cursor-pointer bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded border border-gray-300 shadow-sm transition" >
          Choose PDF
        </label>
        <input id="file-upload" type="file" accept="application/pdf" onChange={e=>setFile(e.target.files?.[0] || null)} className="hidden" />
        {file && (
          <span className="text-sm text-gray-600 truncate max-w-[200px]">
            {file.name}
          </span>
        )}
        <button disabled={!file || loading} className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded">{loading? 'Uploading...':'Upload PDF'}</button>
      </form>
      {result && (
        <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm text-left">
          <p className="font-medium text-gray-900 mb-2">Extracted</p>
          <pre className="text-sm text-gray-700 whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}



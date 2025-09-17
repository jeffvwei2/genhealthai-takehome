import Orders from './components/Orders'
import UploadPDF from './components/UploadPDF'
function App() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-100">
      <main className="mx-auto max-w-3xl px-6 py-16 text-center">
        <h1 className="text-2xl font-bold mb-6">GenHealth AI Takehome</h1>
        <div className="grid gap-6 sm:grid-cols-2 text-left">
          <div className="rounded-xl border border-gray-200 bg-white/80 backdrop-blur p-6 shadow-sm">
            <Orders />
          </div>
          <div className="rounded-xl border border-gray-200 bg-white/80 backdrop-blur p-6 shadow-sm sm:col-span-2">
            <UploadPDF />
          </div>
        </div>

      </main>
    </div>
  )
}

export default App

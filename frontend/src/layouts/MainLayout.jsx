export function MainLayout({ children }) {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto py-12 px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">FastAPI React Starter Template</h1>
        {children}
      </div>
    </div>
  )
}

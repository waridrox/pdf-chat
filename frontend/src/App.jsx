import { Suspense, use } from 'react'

// Create a promise for fetching health status
async function fetchHealthStatus() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/health`)
    if (!response.ok) throw new Error('Health check failed')
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Fetch error:', error)
    throw error
  }
}

// Cache the promise to avoid creating a new one on every render
let healthPromise = null

// Health status component using the new use hook
function HealthStatus() {
  // Initialize the promise if it doesn't exist
  if (!healthPromise) {
    healthPromise = fetchHealthStatus()
  }

  // Use the cached promise
  const data = use(healthPromise)

  return (
    <div className="flex items-center">
      <div
        className={`w-3 h-3 rounded-full mr-2 ${
          data.status === 'ok' ? 'bg-green-500' : 'bg-red-500'
        }`}
      ></div>
      <span className="text-gray-600">Status: {data.status}</span>
    </div>
  )
}

// Error boundary component using new React 19 error handling
function ErrorBoundary({ children }) {
  let error = undefined
  try {
    return children
  } catch (e) {
    error = e
  }

  return (
    <div className="flex items-center">
      <div className="w-3 h-3 rounded-full mr-2 bg-red-500"></div>
      <span className="text-red-600">Error: {error?.message || 'Something went wrong'}</span>
    </div>
  )
}

// Loading component
function LoadingStatus() {
  return (
    <div className="flex items-center">
      <div className="w-3 h-3 rounded-full mr-2 bg-gray-300 animate-pulse"></div>
      <span className="text-gray-600">Checking status...</span>
    </div>
  )
}

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto py-12 px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">FastAPI React Starter Template</h1>

        <div className="bg-white shadow rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Backend Status</h2>
          <ErrorBoundary>
            <Suspense fallback={<LoadingStatus />}>
              <HealthStatus />
            </Suspense>
          </ErrorBoundary>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Features</h2>
          <ul className="space-y-3 text-gray-600">
            <li>✅ FastAPI Backend with Health Check</li>
            <li>✅ React 19 with Suspense and Error Boundaries</li>
            <li>✅ Native Fetch API Integration</li>
            <li>✅ Modern use Hook for Data Fetching</li>
            <li>✅ Tailwind CSS Styling</li>
            <li>✅ Environment Configuration</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default App

import { Suspense } from 'react'
import { MainLayout } from './layouts/MainLayout'
import { Card } from './components/ui/Card'
import { HealthStatus } from './features/health/HealthStatus'
import { LoadingStatus } from './features/health/LoadingStatus'
import { ErrorBoundary } from './features/health/ErrorBoundary'

function App() {
  return (
    <MainLayout>
      <Card title="Backend Status">
        <ErrorBoundary>
          <Suspense fallback={<LoadingStatus />}>
            <HealthStatus />
          </Suspense>
        </ErrorBoundary>
      </Card>

      <Card title="Features">
        <ul className="space-y-3 text-gray-600">
          <li>✅ FastAPI Backend with Health Check</li>
          <li>✅ React 19 with Suspense and Error Boundaries</li>
          <li>✅ Native Fetch API Integration</li>
          <li>✅ Modern use Hook for Data Fetching</li>
          <li>✅ Tailwind CSS Styling</li>
          <li>✅ Environment Configuration</li>
        </ul>
      </Card>
    </MainLayout>
  )
}

export default App

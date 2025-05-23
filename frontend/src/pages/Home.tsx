import { Suspense } from 'react'
import { useNavigate } from 'react-router-dom'
import { CircleCheck, Sparkles } from 'lucide-react'
import { ErrorBoundary } from '../features/health/ErrorBoundary'
import { HealthStatus } from '../features/health/HealthStatus'
import { LoadingStatus } from '../features/health/LoadingStatus'
import { Button } from '../components/ui/Button'

type FeatureItem = {
  id: string
  text: string
}

const features: FeatureItem[] = [
  { id: '1', text: 'FastAPI Backend with Health Check' },
  { id: '2', text: 'React 19 with Modern Patterns' },
  { id: '3', text: 'Native Fetch API Integration' },
  { id: '4', text: 'Modern Data Fetching' },
  { id: '5', text: 'Tailwind CSS with Dark Mode' },
  { id: '6', text: 'Responsive Design' },
  { id: '7', text: 'Error Boundaries' },
  { id: '8', text: 'Docker Support' },
]

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="space-y-12 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-gray-900 dark:text-white">
          Welcome to FastAPI React Starter
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          A modern full-stack starter template with React 19 and FastAPI
        </p>
      </div>

      <div className="grid gap-6">
        <div
          className="p-6 rounded-lg border border-gray-200 dark:border-gray-700 
          bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-all"
        >
          <div className="flex items-start space-x-4">
            <div
              className="flex-shrink-0 p-2 rounded-lg bg-blue-50 dark:bg-blue-900/30 
              text-blue-600 dark:text-blue-400"
            >
              <CircleCheck />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                Backend Status
              </h2>
              <ErrorBoundary>
                <Suspense fallback={<LoadingStatus />}>
                  <HealthStatus />
                </Suspense>
              </ErrorBoundary>
            </div>
          </div>
        </div>

        <div
          className="p-6 rounded-lg border border-gray-200 dark:border-gray-700 
          bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-all"
        >
          <div className="flex items-start space-x-4">
            <div
              className="flex-shrink-0 p-2 rounded-lg bg-green-50 dark:bg-green-900/30 
              text-green-600 dark:text-green-400"
            >
              <Sparkles />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Features</h2>
              <ul className="space-y-3 text-gray-600 dark:text-gray-300">
                {features.map(({ id, text }) => (
                  <li key={id} className="flex items-center">
                    <span className="text-green-500 dark:text-green-400 mr-2">✓</span>
                    {text}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center space-x-4">
        <Button onClick={() => navigate('/about')} variant="default">
          Learn More
        </Button>
        <Button onClick={() => navigate('/dashboard')} variant="secondary">
          View Dashboard
        </Button>
      </div>
    </div>
  )
}

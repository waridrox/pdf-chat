import { Suspense } from 'react'
import { useNavigate } from 'react-router-dom'
import { ErrorBoundary } from '../features/health/ErrorBoundary'
import { HealthStatus } from '../features/health/HealthStatus'
import { LoadingStatus } from '../features/health/LoadingStatus'

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
        <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-700 
          bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-all">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 p-2 rounded-lg bg-blue-50 dark:bg-blue-900/30 
              text-blue-600 dark:text-blue-400">
              <StatusIcon />
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

        <div className="p-6 rounded-lg border border-gray-200 dark:border-gray-700 
          bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-all">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 p-2 rounded-lg bg-green-50 dark:bg-green-900/30 
              text-green-600 dark:text-green-400">
              <FeaturesIcon />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                Features
              </h2>
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
        <button
          onClick={() => navigate('/about')}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 
            dark:bg-blue-600 dark:hover:bg-blue-700 transition-colors"
          type="button"
        >
          Learn More
        </button>
        <button
          onClick={() => navigate('/dashboard')}
          className="px-6 py-2 bg-gray-100 text-gray-800 rounded-lg hover:bg-gray-200 
            dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 transition-colors"
          type="button"
        >
          View Dashboard
        </button>
      </div>
    </div>
  )
}

function StatusIcon() {
  return (
    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
  )
}

function FeaturesIcon() {
  return (
    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
      />
    </svg>
  )
}

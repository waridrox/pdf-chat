import { createBrowserRouter, redirect } from 'react-router-dom'
import { lazy, Suspense } from 'react'
import RootLayout from '../layouts/RootLayout'

// Lazy load components
const Home = lazy(() => import('../pages/Home'))
const About = lazy(() => import('../pages/About'))
const Upload = lazy(() => import('../pages/Upload'))
const Chat = lazy(() => import('../pages/Chat'))

// Error boundary component
function ErrorBoundary() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-red-600 mb-4">Oops!</h1>
      <p className="text-lg">Something went wrong. Please try again.</p>
    </div>
  )
}

// Loading component
function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>
  )
}

const withSuspense = (element: React.ReactNode) => (
  <Suspense fallback={<PageLoader />}>{element}</Suspense>
)

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorBoundary />,
    children: [
      {
        index: true,
        element: withSuspense(<Home />),
      },
      {
        path: 'about',
        element: withSuspense(<About />),
      },
      {
        path: 'upload',
        element: withSuspense(<Upload />),
      },
      {
        path: 'chat',
        element: withSuspense(<Chat />),
      },
      // Catch-all route
      {
        path: '*',
        loader: () => redirect('/'),
      },
    ],
  },
])

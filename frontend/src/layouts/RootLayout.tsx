import { Link, Outlet } from 'react-router-dom'
import { AppProvider } from '../context/AppContext'
import { Notification } from '../components/ui/Notification'
import { ThemeToggle } from '../components/ui/ThemeToggle'

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/about', label: 'About' },
  { to: '/dashboard', label: 'Dashboard' },
] as const

export default function RootLayout() {
  const currentYear = new Date().getFullYear()
  const linkClasses = "text-gray-900 dark:text-white hover:text-gray-600 dark:hover:text-gray-300 px-3 py-2 rounded-md text-sm font-medium"

  return (
    <AppProvider>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
        <nav className="bg-white dark:bg-gray-800 shadow-sm transition-colors">
          <div className="container mx-auto px-6">
            <div className="flex justify-between h-16 items-center">
              <div className="flex space-x-8">
                {navLinks.map(({ to, label }) => (
                  <Link
                    key={to}
                    to={to}
                    className={linkClasses}
                  >
                    {label}
                  </Link>
                ))}
              </div>
              <ThemeToggle />
            </div>
          </div>
        </nav>

        <main className="container mx-auto px-6 pb-16">
          <Outlet />
        </main>

        <footer className="bg-white dark:bg-gray-800 mt-auto py-6 transition-colors">
          <div className="container mx-auto px-6 text-center text-gray-600 dark:text-gray-300">
            {currentYear} FastAPI React Starter. All rights reserved.
          </div>
        </footer>

        <Notification />
      </div>
    </AppProvider>
  )
}

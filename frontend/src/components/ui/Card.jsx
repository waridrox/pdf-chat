export function Card({ title, children }) {
  return (
    <div className="bg-white shadow rounded-lg p-6 mb-8">
      {title && <h2 className="text-2xl font-semibold text-gray-800 mb-4">{title}</h2>}
      {children}
    </div>
  )
}

import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Home, ArrowLeft } from 'lucide-react'

const NotFound = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full text-center"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
          className="text-8xl mb-8"
        >
          🐕‍🦺
        </motion.div>
        
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 className="text-2xl font-heading font-semibold text-gray-700 mb-4">
          ¡Ups! Página no encontrada
        </h2>
        <p className="text-gray-600 mb-8">
          Parece que esta página se perdió como un cachorro sin collar. 
          No te preocupes, te ayudaremos a encontrar el camino de vuelta.
        </p>
        
        <div className="space-y-4">
          <Link
            to="/"
            className="btn-primary inline-flex items-center px-6 py-3 text-base"
          >
            <Home className="w-5 h-5 mr-2" />
            Volver al Inicio
          </Link>
          
          <button
            onClick={() => window.history.back()}
            className="btn-ghost inline-flex items-center px-6 py-3 text-base"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Página Anterior
          </button>
        </div>
      </motion.div>
    </div>
  )
}

export default NotFound
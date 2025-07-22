import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Search, Filter, MapPin, Calendar, Heart } from 'lucide-react'
import { Link } from 'react-router-dom'
import LoadingSpinner from '../components/LoadingSpinner'

const Dogs = () => {
  const [dogs, setDogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filters, setFilters] = useState({
    breed: '',
    size: '',
    age: '',
    location: ''
  })
  const [showFilters, setShowFilters] = useState(false)

  // Mock data for development
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setDogs([
        {
          id: 1,
          name: 'Luna',
          breed: 'Labrador Mix',
          age: '2 años',
          size: 'Grande',
          location: 'Madrid',
          description: 'Luna es una perrita muy cariñosa que busca una familia que la ame.',
          image: 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400',
          status: 'available',
          gender: 'Hembra',
          weight: '25kg'
        },
        {
          id: 2,
          name: 'Max',
          breed: 'Pastor Alemán',
          age: '3 años',
          size: 'Grande',
          location: 'Barcelona',
          description: 'Max es un perro muy inteligente y leal, perfecto para familias activas.',
          image: 'https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400',
          status: 'available',
          gender: 'Macho',
          weight: '30kg'
        },
        {
          id: 3,
          name: 'Coco',
          breed: 'French Bulldog',
          age: '1 año',
          size: 'Pequeño',
          location: 'Valencia',
          description: 'Coco es un cachorro juguetón que adora a los niños.',
          image: 'https://images.unsplash.com/photo-1583512603805-3cc6b41f3edb?w=400',
          status: 'fostered',
          gender: 'Macho',
          weight: '12kg'
        },
        {
          id: 4,
          name: 'Bella',
          breed: 'Golden Retriever',
          age: '4 años',
          size: 'Grande',
          location: 'Sevilla',
          description: 'Bella es perfecta para familias con niños, muy paciente y cariñosa.',
          image: 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400',
          status: 'available',
          gender: 'Hembra',
          weight: '28kg'
        },
      ])
      setLoading(false)
    }, 1000)
  }, [])

  const filteredDogs = dogs.filter(dog => {
    const matchesSearch = dog.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         dog.breed.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesBreed = !filters.breed || dog.breed.includes(filters.breed)
    const matchesSize = !filters.size || dog.size === filters.size
    const matchesLocation = !filters.location || dog.location.includes(filters.location)
    
    return matchesSearch && matchesBreed && matchesSize && matchesLocation
  })

  if (loading) {
    return <LoadingSpinner text="Cargando perros disponibles..." />
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl md:text-4xl font-heading font-bold text-gray-900 mb-4">
            Perros en Busca de Hogar
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Encuentra tu compañero perfecto entre nuestros perros disponibles para acogida y adopción
          </p>
        </motion.div>

        {/* Search and Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8"
        >
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Buscar por nombre o raza..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="input-field pl-10"
                />
              </div>
            </div>

            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="btn-secondary flex items-center justify-center lg:w-auto"
            >
              <Filter className="w-4 h-4 mr-2" />
              Filtros
            </button>
          </div>

          {/* Filters */}
          {showFilters && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-6 pt-6 border-t border-gray-200"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Raza
                  </label>
                  <select
                    value={filters.breed}
                    onChange={(e) => setFilters({...filters, breed: e.target.value})}
                    className="input-field"
                  >
                    <option value="">Todas las razas</option>
                    <option value="Labrador">Labrador</option>
                    <option value="Pastor Alemán">Pastor Alemán</option>
                    <option value="Golden Retriever">Golden Retriever</option>
                    <option value="French Bulldog">French Bulldog</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tamaño
                  </label>
                  <select
                    value={filters.size}
                    onChange={(e) => setFilters({...filters, size: e.target.value})}
                    className="input-field"
                  >
                    <option value="">Todos los tamaños</option>
                    <option value="Pequeño">Pequeño</option>
                    <option value="Mediano">Mediano</option>
                    <option value="Grande">Grande</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Edad
                  </label>
                  <select
                    value={filters.age}
                    onChange={(e) => setFilters({...filters, age: e.target.value})}
                    className="input-field"
                  >
                    <option value="">Todas las edades</option>
                    <option value="Cachorro">Cachorro (0-1 año)</option>
                    <option value="Joven">Joven (1-3 años)</option>
                    <option value="Adulto">Adulto (3-7 años)</option>
                    <option value="Senior">Senior (7+ años)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Ubicación
                  </label>
                  <select
                    value={filters.location}
                    onChange={(e) => setFilters({...filters, location: e.target.value})}
                    className="input-field"
                  >
                    <option value="">Todas las ubicaciones</option>
                    <option value="Madrid">Madrid</option>
                    <option value="Barcelona">Barcelona</option>
                    <option value="Valencia">Valencia</option>
                    <option value="Sevilla">Sevilla</option>
                  </select>
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-gray-600">
            Mostrando {filteredDogs.length} de {dogs.length} perros
          </p>
        </div>

        {/* Dogs Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredDogs.map((dog, index) => (
            <motion.div
              key={dog.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="card-hover group hover-lift"
            >
              <div className="relative image-hover-zoom">
                <img
                  src={dog.image}
                  alt={dog.name}
                  className="w-full h-48 object-cover"
                />
                <div className="absolute top-2 right-2">
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    dog.status === 'available' 
                      ? 'bg-green-100 text-green-800'
                      : 'bg-orange-100 text-orange-800'
                  }`}>
                    {dog.status === 'available' ? 'Disponible' : 'En Acogida'}
                  </span>
                </div>
                <button className="absolute top-2 left-2 p-2 bg-white/90 hover:bg-white rounded-full transition-colors">
                  <Heart className="w-4 h-4 text-gray-600 hover:text-red-500" />
                </button>
              </div>
              
              <div className="p-4">
                <h3 className="font-heading font-semibold text-lg text-gray-900 mb-2">
                  {dog.name}
                </h3>
                
                <div className="space-y-2 text-sm text-gray-600 mb-4">
                  <div className="flex items-center">
                    <span className="font-medium w-16">Raza:</span>
                    <span>{dog.breed}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="font-medium w-16">Edad:</span>
                    <span>{dog.age}</span>
                  </div>
                  <div className="flex items-center">
                    <span className="font-medium w-16">Tamaño:</span>
                    <span>{dog.size}</span>
                  </div>
                  <div className="flex items-center">
                    <MapPin className="w-4 h-4 mr-1" />
                    <span>{dog.location}</span>
                  </div>
                </div>
                
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {dog.description}
                </p>
                
                <div className="flex gap-2">
                  <Link 
                    to={`/dogs/${dog.id}`}
                    className="btn-primary flex-1 text-sm py-2 text-center"
                  >
                    Ver Detalles
                  </Link>
                  <button className="btn-secondary text-sm py-2 px-3">
                    <Heart className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Empty State */}
        {filteredDogs.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No se encontraron perros
            </h3>
            <p className="text-gray-600">
              Intenta ajustar tus filtros de búsqueda
            </p>
          </motion.div>
        )}
      </div>
    </div>
  )
}

export default Dogs
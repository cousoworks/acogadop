import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  ArrowLeft, 
  Heart, 
  Share2, 
  MapPin, 
  Calendar, 
  User, 
  Activity, 
  Shield, 
  Camera,
  Phone,
  Mail,
  MessageCircle,
  Star,
  Award,
  Info
} from 'lucide-react'
import LoadingSpinner from '../components/LoadingSpinner'

const DogDetail = () => {
  const { id } = useParams()
  const [dog, setDog] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeImageIndex, setActiveImageIndex] = useState(0)
  const [isFavorite, setIsFavorite] = useState(false)

  // Mock data for development
  useEffect(() => {
    setTimeout(() => {
      const mockDog = {
        id: parseInt(id),
        name: 'Luna',
        breed: 'Labrador Mix',
        age: '2 años',
        size: 'Grande',
        location: 'Madrid, España',
        description: 'Luna es una perrita muy cariñosa que busca una familia que la ame. Le encanta jugar en el parque, es muy social con otros perros y adora a los niños. Ha vivido en una casa con jardín y está acostumbrada a la vida familiar.',
        images: [
          'https://images.unsplash.com/photo-1552053831-71594a27632d?w=800',
          'https://images.unsplash.com/photo-1561037404-61cd46aa615b?w=800',
          'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800',
          'https://images.unsplash.com/photo-1534361960057-19889db9621e?w=800'
        ],
        status: 'available',
        gender: 'Hembra',
        weight: '25kg',
        height: '55cm',
        color: 'Dorado',
        personality: ['Cariñosa', 'Juguetona', 'Sociable', 'Inteligente'],
        goodWith: ['Niños', 'Otros perros', 'Gatos'],
        vaccinated: true,
        sterilized: true,
        microchipped: true,
        dateAdded: '15 de Enero, 2024',
        rescueStory: 'Luna fue encontrada abandonada en un parque cuando era cachorra. Desde entonces ha estado en acogida y está lista para encontrar su hogar definitivo.',
        contact: {
          shelter: 'Refugio Esperanza Canina',
          phone: '+34 612 345 678',
          email: 'adopciones@esperanzacanina.org',
          address: 'Calle de la Esperanza 123, Madrid'
        },
        medicalHistory: 'Completamente sana, vacunas al día, desparasitada',
        specialNeeds: 'Ninguna',
        adoptionFee: '150€'
      }
      setDog(mockDog)
      setLoading(false)
    }, 1000)
  }, [id])

  if (loading) {
    return <LoadingSpinner text="Cargando información del perro..." />
  }

  if (!dog) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🐕</div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">Perro no encontrado</h2>
          <p className="text-gray-600 mb-4">No pudimos encontrar la información de este perro.</p>
          <Link to="/dogs" className="btn-primary">
            Volver a la lista
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with back button */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white shadow-sm border-b"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link 
              to="/dogs" 
              className="flex items-center text-gray-600 hover:text-gray-900 transition-colors group"
            >
              <ArrowLeft className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" />
              Volver a la lista
            </Link>
            <div className="flex items-center gap-3">
              <button 
                onClick={() => setIsFavorite(!isFavorite)}
                className={`p-2 rounded-full transition-all transform hover:scale-110 ${
                  isFavorite 
                    ? 'bg-red-100 text-red-600' 
                    : 'bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-500'
                }`}
              >
                <Heart className={`w-5 h-5 ${isFavorite ? 'fill-current' : ''}`} />
              </button>
              <button className="p-2 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors">
                <Share2 className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Image Gallery */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2"
          >
            <div className="bg-white rounded-xl shadow-sm overflow-hidden hover-lift">
              <div className="relative image-hover-zoom">
                <motion.img
                  key={activeImageIndex}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3 }}
                  src={dog.images[activeImageIndex]}
                  alt={dog.name}
                  className="w-full h-96 object-cover"
                />
                <div className="absolute top-4 right-4">
                  <span className={`px-3 py-1 text-sm font-medium rounded-full ${
                    dog.status === 'available' 
                      ? 'bg-green-100 text-green-800'
                      : 'bg-orange-100 text-orange-800'
                  }`}>
                    {dog.status === 'available' ? 'Disponible' : 'En Acogida'}
                  </span>
                </div>
              </div>
              
              {/* Image thumbnails */}
              <div className="p-4">
                <div className="flex gap-2 overflow-x-auto">
                  {dog.images.map((image, index) => (
                    <motion.button
                      key={index}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setActiveImageIndex(index)}
                      className={`flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-colors ${
                        activeImageIndex === index 
                          ? 'border-blue-500' 
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <img
                        src={image}
                        alt={`${dog.name} ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </motion.button>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Dog Information */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
          >
            {/* Basic Info */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-3xl font-heading font-bold text-gray-900 mb-2">
                    {dog.name}
                  </h1>
                  <p className="text-lg text-gray-600">{dog.breed}</p>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-500">Tarifa de adopción</div>
                  <div className="text-2xl font-bold text-green-600">{dog.adoptionFee}</div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="flex items-center text-gray-600">
                  <Calendar className="w-4 h-4 mr-2" />
                  <span className="text-sm">{dog.age}</span>
                </div>
                <div className="flex items-center text-gray-600">
                  <User className="w-4 h-4 mr-2" />
                  <span className="text-sm">{dog.gender}</span>
                </div>
                <div className="flex items-center text-gray-600">
                  <Activity className="w-4 h-4 mr-2" />
                  <span className="text-sm">{dog.size}</span>
                </div>
                <div className="flex items-center text-gray-600">
                  <MapPin className="w-4 h-4 mr-2" />
                  <span className="text-sm">{dog.location}</span>
                </div>
              </div>

              {/* Health Status */}
              <div className="border-t pt-4">
                <h3 className="font-semibold text-gray-900 mb-3">Estado de Salud</h3>
                <div className="grid grid-cols-3 gap-2">
                  <div className={`flex items-center justify-center p-2 rounded-lg ${
                    dog.vaccinated ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    <Shield className="w-4 h-4 mr-1" />
                    <span className="text-xs">Vacunado</span>
                  </div>
                  <div className={`flex items-center justify-center p-2 rounded-lg ${
                    dog.sterilized ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    <Award className="w-4 h-4 mr-1" />
                    <span className="text-xs">Castrado</span>
                  </div>
                  <div className={`flex items-center justify-center p-2 rounded-lg ${
                    dog.microchipped ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    <Info className="w-4 h-4 mr-1" />
                    <span className="text-xs">Chip</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Contact Card */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Información de Contacto</h3>
              <div className="space-y-3">
                <div>
                  <div className="font-medium text-gray-900">{dog.contact.shelter}</div>
                  <div className="text-sm text-gray-600">{dog.contact.address}</div>
                </div>
                <div className="space-y-2">
                  <a 
                    href={`tel:${dog.contact.phone}`}
                    className="flex items-center text-blue-600 hover:text-blue-700 transition-colors"
                  >
                    <Phone className="w-4 h-4 mr-2" />
                    <span className="text-sm">{dog.contact.phone}</span>
                  </a>
                  <a 
                    href={`mailto:${dog.contact.email}`}
                    className="flex items-center text-blue-600 hover:text-blue-700 transition-colors"
                  >
                    <Mail className="w-4 h-4 mr-2" />
                    <span className="text-sm">{dog.contact.email}</span>
                  </a>
                </div>
              </div>
              
              <div className="mt-6 space-y-2">
                <motion.button 
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="btn-primary w-full"
                >
                  Solicitar Adopción
                </motion.button>
                <motion.button 
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="btn-secondary w-full flex items-center justify-center"
                >
                  <MessageCircle className="w-4 h-4 mr-2" />
                  Contactar Refugio
                </motion.button>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Detailed Information */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8"
        >
          {/* About */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Sobre {dog.name}</h3>
            <p className="text-gray-600 mb-6 leading-relaxed">
              {dog.description}
            </p>
            
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Personalidad</h4>
                <div className="flex flex-wrap gap-2">
                  {dog.personality.map((trait, index) => (
                    <motion.span
                      key={trait}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.5 + index * 0.1 }}
                      className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                    >
                      {trait}
                    </motion.span>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-medium text-gray-900 mb-2">Se lleva bien con</h4>
                <div className="flex flex-wrap gap-2">
                  {dog.goodWith.map((item, index) => (
                    <motion.span
                      key={item}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.7 + index * 0.1 }}
                      className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full"
                    >
                      {item}
                    </motion.span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Additional Details */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Detalles Adicionales</h3>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-gray-500">Peso</div>
                  <div className="font-medium">{dog.weight}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Altura</div>
                  <div className="font-medium">{dog.height}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Color</div>
                  <div className="font-medium">{dog.color}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Fecha de rescate</div>
                  <div className="font-medium">{dog.dateAdded}</div>
                </div>
              </div>

              <div>
                <div className="text-sm text-gray-500 mb-1">Historia de rescate</div>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {dog.rescueStory}
                </p>
              </div>

              <div>
                <div className="text-sm text-gray-500 mb-1">Historial médico</div>
                <p className="text-gray-600 text-sm">
                  {dog.medicalHistory}
                </p>
              </div>

              {dog.specialNeeds !== 'Ninguna' && (
                <div>
                  <div className="text-sm text-gray-500 mb-1">Necesidades especiales</div>
                  <p className="text-gray-600 text-sm">
                    {dog.specialNeeds}
                  </p>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default DogDetail
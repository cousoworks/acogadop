import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'
import api from '../services/api'

const AddDog = () => {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  const [formData, setFormData] = useState({
    name: '',
    breed: '',
    age: '',
    size: 'medium',
    gender: 'male',
    weight: '',
    location: '',
    description: '',
    medical_info: '',
    behavior_notes: '',
    good_with_kids: false,
    good_with_dogs: false,
    good_with_cats: false,
    needs_yard: false,
    photos: ''
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // Convert age to number and prepare data
      const dogData = {
        ...formData,
        age: formData.age ? parseInt(formData.age) : null,
        weight: formData.weight ? parseFloat(formData.weight) : null,
        photos: formData.photos ? formData.photos.split(',').map(url => url.trim()) : []
      }

      await api.post('/dogs/', dogData)
      navigate('/dogs')
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear el anuncio')
    } finally {
      setLoading(false)
    }
  }

  // Check if user can add dogs
  if (!user || !['shelter_admin', 'admin'].includes(user.user_type)) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="card p-8 text-center">
            <div className="text-6xl mb-4">🔒</div>
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Acceso Restringido
            </h1>
            <p className="text-gray-600 mb-6">
              Solo las perreras aprobadas pueden añadir perros a la plataforma.
            </p>
            {user?.user_type === 'shelter' && (
              <p className="text-yellow-600">
                Tu solicitud de perrera está pendiente de aprobación.
              </p>
            )}
          </div>
        </div>
      </div>
    )
  }

  if (loading) {
    return <LoadingSpinner />
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-heading font-bold text-gray-900">
            Añadir Perro
          </h1>
          <p className="mt-2 text-gray-600">
            Completa la información del perro para crear un nuevo anuncio
          </p>
        </div>

        <div className="card p-8">
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Información Básica */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Información Básica
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                    Nombre *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label htmlFor="breed" className="block text-sm font-medium text-gray-700">
                    Raza
                  </label>
                  <input
                    type="text"
                    id="breed"
                    name="breed"
                    value={formData.breed}
                    onChange={handleChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label htmlFor="age" className="block text-sm font-medium text-gray-700">
                    Edad (en meses)
                  </label>
                  <input
                    type="number"
                    id="age"
                    name="age"
                    min="1"
                    value={formData.age}
                    onChange={handleChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label htmlFor="weight" className="block text-sm font-medium text-gray-700">
                    Peso (kg)
                  </label>
                  <input
                    type="number"
                    id="weight"
                    name="weight"
                    step="0.1"
                    min="0"
                    value={formData.weight}
                    onChange={handleChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label htmlFor="size" className="block text-sm font-medium text-gray-700">
                    Tamaño *
                  </label>
                  <select
                    id="size"
                    name="size"
                    required
                    value={formData.size}
                    onChange={handleChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="small">Pequeño</option>
                    <option value="medium">Mediano</option>
                    <option value="large">Grande</option>
                    <option value="extra_large">Extra Grande</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="gender" className="block text-sm font-medium text-gray-700">
                    Sexo *
                  </label>
                  <select
                    id="gender"
                    name="gender"
                    required
                    value={formData.gender}
                    onChange={handleChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="male">Macho</option>
                    <option value="female">Hembra</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Ubicación */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Ubicación
              </h3>
              <div>
                <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                  Ubicación del perro
                </label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  placeholder="Ciudad, provincia..."
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Descripción */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Descripción
              </h3>
              <div className="space-y-4">
                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                    Descripción general
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    rows={4}
                    value={formData.description}
                    onChange={handleChange}
                    placeholder="Describe la personalidad, historia y características del perro..."
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label htmlFor="medical_info" className="block text-sm font-medium text-gray-700">
                    Información médica
                  </label>
                  <textarea
                    id="medical_info"
                    name="medical_info"
                    rows={3}
                    value={formData.medical_info}
                    onChange={handleChange}
                    placeholder="Vacunas, esterilización, tratamientos, etc."
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label htmlFor="behavior_notes" className="block text-sm font-medium text-gray-700">
                    Notas de comportamiento
                  </label>
                  <textarea
                    id="behavior_notes"
                    name="behavior_notes"
                    rows={3}
                    value={formData.behavior_notes}
                    onChange={handleChange}
                    placeholder="Nivel de energía, entrenamiento, comportamiento especial..."
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Compatibilidad */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Compatibilidad
              </h3>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="good_with_kids"
                    checked={formData.good_with_kids}
                    onChange={handleChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Bueno con niños</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="good_with_dogs"
                    checked={formData.good_with_dogs}
                    onChange={handleChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Bueno con otros perros</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="good_with_cats"
                    checked={formData.good_with_cats}
                    onChange={handleChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Bueno con gatos</span>
                </label>

                <label className="flex items-center">
                  <input
                    type="checkbox"
                    name="needs_yard"
                    checked={formData.needs_yard}
                    onChange={handleChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Necesita jardín</span>
                </label>
              </div>
            </div>

            {/* Fotos */}
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Fotos
              </h3>
              <div>
                <label htmlFor="photos" className="block text-sm font-medium text-gray-700">
                  URLs de fotos (separadas por comas)
                </label>
                <textarea
                  id="photos"
                  name="photos"
                  rows={3}
                  value={formData.photos}
                  onChange={handleChange}
                  placeholder="https://ejemplo.com/foto1.jpg, https://ejemplo.com/foto2.jpg"
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Ingresa las URLs de las fotos separadas por comas
                </p>
              </div>
            </div>

            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={() => navigate('/dogs')}
                className="px-6 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading ? 'Creando...' : 'Crear Anuncio'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default AddDog
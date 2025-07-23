import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'
import UserManagement from './UserManagement'
import api from '../services/api'

const AdminPanel = () => {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [pendingShelters, setPendingShelters] = useState([])
  const [approvedShelters, setApprovedShelters] = useState([])
  const [activeTab, setActiveTab] = useState('pending')
  const [processingId, setProcessingId] = useState(null)

  useEffect(() => {
    if (user?.user_type === 'admin') {
      fetchShelters()
    }
  }, [user])

  const fetchShelters = async () => {
    try {
      setLoading(true)
      
      // Fetch pending shelters
      const pendingResponse = await api.get('/api/shelters/pending')
      setPendingShelters(pendingResponse.data)
      
      // Fetch approved shelters
      const approvedResponse = await api.get('/api/shelters/approved')
      setApprovedShelters(approvedResponse.data)
      
    } catch (error) {
      console.error('Error fetching shelters:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApproval = async (userId, approved, adminNotes = '') => {
    try {
      setProcessingId(userId)
      
      await api.post('/api/shelters/approve', {
        user_id: userId,
        approved: approved,
        admin_notes: adminNotes
      })
      
      // Refresh the data
      await fetchShelters()
      
    } catch (error) {
      console.error('Error processing approval:', error)
      alert('Error al procesar la solicitud')
    } finally {
      setProcessingId(null)
    }
  }

  if (user?.user_type !== 'admin') {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="card p-8 text-center">
            <h1 className="text-2xl font-bold text-red-600 mb-4">
              Acceso Denegado
            </h1>
            <p className="text-gray-600">
              Solo los administradores pueden acceder a este panel.
            </p>
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
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-heading font-bold text-gray-900">
            Panel de Administración
          </h1>
          <p className="mt-2 text-gray-600">
            Gestiona las solicitudes de registro de perreras
          </p>
        </div>

        {/* Tabs */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('pending')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'pending'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Solicitudes Pendientes ({pendingShelters.length})
            </button>
            <button
              onClick={() => setActiveTab('approved')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'approved'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Perreras Aprobadas ({approvedShelters.length})
            </button>
            <button
              onClick={() => setActiveTab('users')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'users'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Gestión de Usuarios
            </button>
          </nav>
        </div>

        {/* Pending Shelters */}
        {activeTab === 'pending' && (
          <div className="space-y-6">
            {pendingShelters.length === 0 ? (
              <div className="card p-8 text-center">
                <div className="text-4xl mb-4">✅</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No hay solicitudes pendientes
                </h3>
                <p className="text-gray-600">
                  Todas las solicitudes han sido procesadas.
                </p>
              </div>
            ) : (
              pendingShelters.map((shelter) => (
                <ShelterApplicationCard
                  key={shelter.id}
                  shelter={shelter}
                  onApprove={(adminNotes) => handleApproval(shelter.id, true, adminNotes)}
                  onReject={(adminNotes) => handleApproval(shelter.id, false, adminNotes)}
                  isProcessing={processingId === shelter.id}
                />
              ))
            )}
          </div>
        )}

        {/* Approved Shelters */}
        {activeTab === 'approved' && (
          <div className="space-y-4">
            {approvedShelters.length === 0 ? (
              <div className="card p-8 text-center">
                <div className="text-4xl mb-4">🏠</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No hay perreras aprobadas
                </h3>
                <p className="text-gray-600">
                  Las perreras aprobadas aparecerán aquí.
                </p>
              </div>
            ) : (
              approvedShelters.map((shelter) => (
                <ApprovedShelterCard key={shelter.id} shelter={shelter} />
              ))
            )}
          </div>
        )}

        {/* User Management */}
        {activeTab === 'users' && (
          <UserManagement />
        )}
      </div>
    </div>
  )
}

const ShelterApplicationCard = ({ shelter, onApprove, onReject, isProcessing }) => {
  const [showNotes, setShowNotes] = useState(false)
  const [adminNotes, setAdminNotes] = useState('')

  const handleApprove = () => {
    onApprove(adminNotes)
    setShowNotes(false)
    setAdminNotes('')
  }

  const handleReject = () => {
    if (!adminNotes.trim()) {
      alert('Por favor, proporciona una razón para el rechazo')
      return
    }
    onReject(adminNotes)
    setShowNotes(false)
    setAdminNotes('')
  }

  return (
    <div className="card p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-medium text-gray-900">
            {shelter.shelter_name}
          </h3>
          <p className="text-sm text-gray-600">
            Solicitado por: {shelter.name} ({shelter.email})
          </p>
          <p className="text-sm text-gray-500">
            Fecha: {new Date(shelter.created_at).toLocaleDateString()}
          </p>
        </div>
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
          Pendiente
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <h4 className="font-medium text-gray-900 mb-2">Información de Contacto</h4>
          <div className="space-y-1 text-sm text-gray-600">
            <p><strong>Teléfono:</strong> {shelter.phone || 'No proporcionado'}</p>
            <p><strong>Ubicación:</strong> {shelter.location || 'No proporcionada'}</p>
            <p><strong>Sitio Web:</strong> {shelter.shelter_website || 'No proporcionado'}</p>
          </div>
        </div>

        <div>
          <h4 className="font-medium text-gray-900 mb-2">Información Legal</h4>
          <div className="space-y-1 text-sm text-gray-600">
            <p><strong>Licencia:</strong> {shelter.shelter_license || 'No proporcionada'}</p>
            <p><strong>Dirección:</strong> {shelter.shelter_address || 'No proporcionada'}</p>
          </div>
        </div>
      </div>

      {shelter.shelter_description && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-900 mb-2">Descripción</h4>
          <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded-md">
            {shelter.shelter_description}
          </p>
        </div>
      )}

      <div className="flex justify-end space-x-3">
        {!showNotes ? (
          <>
            <button
              onClick={() => setShowNotes(true)}
              disabled={isProcessing}
              className="px-4 py-2 border border-red-300 rounded-md text-sm font-medium text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
            >
              Rechazar
            </button>
            <button
              onClick={handleApprove}
              disabled={isProcessing}
              className="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
            >
              {isProcessing ? 'Procesando...' : 'Aprobar'}
            </button>
          </>
        ) : (
          <div className="w-full">
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notas del administrador:
              </label>
              <textarea
                value={adminNotes}
                onChange={(e) => setAdminNotes(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Proporciona detalles sobre la decisión..."
              />
            </div>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => {
                  setShowNotes(false)
                  setAdminNotes('')
                }}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                onClick={handleReject}
                disabled={isProcessing}
                className="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-red-600 hover:bg-red-700 disabled:opacity-50"
              >
                Confirmar Rechazo
              </button>
              <button
                onClick={handleApprove}
                disabled={isProcessing}
                className="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
              >
                Aprobar con Notas
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

const ApprovedShelterCard = ({ shelter }) => {
  return (
    <div className="card p-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium text-gray-900">
            {shelter.shelter_name}
          </h3>
          <p className="text-sm text-gray-600">
            {shelter.name} ({shelter.email})
          </p>
          <p className="text-sm text-gray-500">
            Aprobado: {new Date(shelter.created_at).toLocaleDateString()}
          </p>
        </div>
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Activa
        </span>
      </div>
    </div>
  )
}

export default AdminPanel

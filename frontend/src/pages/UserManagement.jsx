import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'
import api from '../services/api'

const UserManagement = () => {
  const { user } = useAuth()
  const [loading, setLoading] = useState(true)
  const [users, setUsers] = useState([])
  const [stats, setStats] = useState({})
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('')
  const [editingUser, setEditingUser] = useState(null)
  const [showEditModal, setShowEditModal] = useState(false)
  const [processingAction, setProcessingAction] = useState(null)

  useEffect(() => {
    if (user?.user_type === 'admin') {
      fetchData()
    }
  }, [user, searchTerm, filterType])

  const fetchData = async () => {
    try {
      setLoading(true)
      
      // Fetch users
      const params = new URLSearchParams()
      if (searchTerm) params.append('search', searchTerm)
      if (filterType) params.append('user_type', filterType)
      
      const [usersResponse, statsResponse] = await Promise.all([
        api.get(`/auth/admin/users?${params.toString()}`),
        api.get('/auth/admin/stats')
      ])
      
      setUsers(usersResponse.data)
      setStats(statsResponse.data)
      
    } catch (error) {
      console.error('Error fetching data:', error)
      alert('Error al cargar los datos')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteUser = async (userId, userName) => {
    const confirmMessage = `⚠️ ATENCIÓN: ¿Estás seguro de que quieres ELIMINAR PERMANENTEMENTE al usuario "${userName}"?

Esta acción:
• Eliminará al usuario completamente del sistema
• Eliminará todos sus datos asociados
• NO SE PUEDE DESHACER

¿Confirmas que quieres proceder?`

    if (!window.confirm(confirmMessage)) {
      return
    }

    try {
      setProcessingAction(userId)
      await api.delete(`/auth/admin/users/${userId}`)
      await fetchData() // Refresh data
      alert(`✅ Usuario "${userName}" eliminado exitosamente`)
    } catch (error) {
      console.error('Error deleting user:', error)
      alert('❌ Error al eliminar el usuario. Por favor, inténtalo de nuevo.')
    } finally {
      setProcessingAction(null)
    }
  }

  const handleEditUser = (user) => {
    setEditingUser({
      ...user,
      password: '' // Don't pre-fill password
    })
    setShowEditModal(true)
  }

  const handleSaveUser = async (updatedUser) => {
    try {
      const updateData = { ...updatedUser }
      
      // Remove empty password field
      if (!updateData.password) {
        delete updateData.password
      }
      
      // Remove unchanged fields
      Object.keys(updateData).forEach(key => {
        if (updateData[key] === editingUser[key]) {
          delete updateData[key]
        }
      })
      
      await api.put(`/auth/admin/users/${editingUser.id}`, updateData)
      await fetchData() // Refresh data
      setShowEditModal(false)
      setEditingUser(null)
      alert('Usuario actualizado exitosamente')
    } catch (error) {
      console.error('Error updating user:', error)
      alert('Error al actualizar el usuario')
    }
  }

  const getUserTypeLabel = (type) => {
    const labels = {
      'foster': 'Acogedor',
      'shelter': 'Perrera (Pendiente)',
      'shelter_admin': 'Perrera (Aprobada)',
      'volunteer': 'Voluntario',
      'admin': 'Administrador'
    }
    return labels[type] || type
  }

  const getUserTypeBadgeColor = (type) => {
    const colors = {
      'foster': 'bg-blue-100 text-blue-800',
      'shelter': 'bg-yellow-100 text-yellow-800',
      'shelter_admin': 'bg-green-100 text-green-800',
      'volunteer': 'bg-purple-100 text-purple-800',
      'admin': 'bg-red-100 text-red-800'
    }
    return colors[type] || 'bg-gray-100 text-gray-800'
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
              Solo los administradores pueden acceder a la gestión de usuarios.
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
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-heading font-bold text-gray-900">
            Gestión de Usuarios
          </h1>
          <p className="mt-2 text-gray-600">
            Administra todos los usuarios de la plataforma
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 font-bold">👥</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Usuarios</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_users || 0}</p>
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 font-bold">✓</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Usuarios Activos</p>
                <p className="text-2xl font-bold text-gray-900">{stats.active_users || 0}</p>
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
                  <span className="text-orange-600 font-bold">🏠</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Perreras</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_shelters || 0}</p>
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 font-bold">🐕</span>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Perros</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_dogs || 0}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="card p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Buscar usuarios
              </label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Buscar por nombre o email..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Filtrar por tipo
              </label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Todos los tipos</option>
                <option value="foster">Acogedores</option>
                <option value="shelter">Perreras (Pendientes)</option>
                <option value="shelter_admin">Perreras (Aprobadas)</option>
                <option value="volunteer">Voluntarios</option>
                <option value="admin">Administradores</option>
              </select>
            </div>
          </div>
        </div>

        {/* Users Table */}
        <div className="card">
          <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Usuario
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tipo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Datos Relacionados
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha Registro
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-medium">
                            {user.name.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {user.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {user.email}
                          </div>
                          {user.shelter_name && (
                            <div className="text-xs text-gray-400">
                              Perrera: {user.shelter_name}
                            </div>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getUserTypeBadgeColor(user.user_type)}`}>
                        {getUserTypeLabel(user.user_type)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        user.is_active 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {user.is_active ? 'Activo' : 'Inactivo'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {user.user_type === 'shelter' || user.user_type === 'shelter_admin' ? (
                          <div className="space-y-1">
                            <div className="text-xs text-gray-600">🐕 Perros registrados</div>
                            <div className="text-xs text-gray-600">📋 Aplicaciones recibidas</div>
                          </div>
                        ) : (
                          <div className="space-y-1">
                            <div className="text-xs text-gray-600">📝 Aplicaciones enviadas</div>
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(user.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center space-x-4">
                        <button
                          onClick={() => handleEditUser(user)}
                          disabled={processingAction === user.id}
                          className="text-blue-600 hover:text-blue-800 disabled:opacity-50"
                          title="Editar usuario"
                        >
                          ✏️ Editar
                        </button>
                        
                        {user.email !== 'admin@acogadop.com' && ( // Prevent actions on main admin
                          <button
                            onClick={() => handleDeleteUser(user.id, user.name)}
                            disabled={processingAction === user.id}
                            className="text-red-600 hover:text-red-800 disabled:opacity-50"
                            title="Eliminar usuario permanentemente"
                          >
                            🗑️ Eliminar
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
        </div>

        {/* Edit Modal */}
        {showEditModal && editingUser && (
          <EditUserModal
            user={editingUser}
            onSave={handleSaveUser}
            onCancel={() => {
              setShowEditModal(false)
              setEditingUser(null)
            }}
          />
        )}
      </div>
    </div>
  )
}

const EditUserModal = ({ user, onSave, onCancel }) => {
  const [formData, setFormData] = useState(user)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave(formData)
  }

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Editar Usuario: {user.name}
          </h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Nombre *
                </label>
                <input
                  type="text"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Email *
                </label>
                <input
                  type="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Teléfono
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone || ''}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Ubicación
                </label>
                <input
                  type="text"
                  name="location"
                  value={formData.location || ''}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Tipo de Usuario
                </label>
                <select
                  name="user_type"
                  value={formData.user_type}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="foster">Acogedor</option>
                  <option value="shelter">Perrera (Pendiente)</option>
                  <option value="shelter_admin">Perrera (Aprobada)</option>
                  <option value="volunteer">Voluntario</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Estado del Usuario
                </label>
                <select
                  name="is_active"
                  value={formData.is_active ? 'true' : 'false'}
                  onChange={(e) => handleChange({
                    target: { name: 'is_active', value: e.target.value === 'true', type: 'checkbox', checked: e.target.value === 'true' }
                  })}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="true">Activo</option>
                  <option value="false">Inactivo</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Nueva Contraseña
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password || ''}
                  onChange={handleChange}
                  placeholder="Dejar vacío para no cambiar"
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  name="is_verified"
                  checked={formData.is_verified}
                  onChange={handleChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-700">Email verificado</span>
              </label>
            </div>

            <div className="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Guardar Cambios
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default UserManagement

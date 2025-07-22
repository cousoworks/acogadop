import axios from 'axios'
import Cookies from 'js-cookie'
import toast from 'react-hot-toast'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = Cookies.get('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      Cookies.remove('token')
      window.location.href = '/login'
    }
    
    const message = error.response?.data?.detail || 'Ha ocurrido un error'
    if (error.response?.status !== 401) {
      toast.error(message)
    }
    
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  me: () => api.get('/auth/me'),
  updateProfile: (userData) => api.put('/auth/profile', userData),
  changePassword: (passwordData) => api.put('/auth/password', passwordData),
}

// Dogs API
export const dogsAPI = {
  getAll: (params) => api.get('/dogs', { params }),
  getById: (id) => api.get(`/dogs/${id}`),
  create: (dogData) => api.post('/dogs', dogData),
  update: (id, dogData) => api.put(`/dogs/${id}`, dogData),
  delete: (id) => api.delete(`/dogs/${id}`),
  uploadPhoto: (id, formData) => api.post(`/dogs/${id}/photos`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deletePhoto: (dogId, photoId) => api.delete(`/dogs/${dogId}/photos/${photoId}`),
  generateAdoptionPoster: (id) => api.get(`/dogs/${id}/adoption-poster`, {
    responseType: 'blob'
  }),
}

// Foster applications API
export const fostersAPI = {
  getMyApplications: () => api.get('/fosters/my-applications'),
  apply: (dogId, applicationData) => api.post(`/fosters/apply/${dogId}`, applicationData),
  updateStatus: (applicationId, status) => api.put(`/fosters/${applicationId}/status`, { status }),
  getApplications: (params) => api.get('/fosters/applications', { params }),
}

// Favorites API
export const favoritesAPI = {
  get: () => api.get('/favorites'),
  add: (dogId) => api.post(`/favorites/${dogId}`),
  remove: (dogId) => api.delete(`/favorites/${dogId}`),
}

// Search API
export const searchAPI = {
  dogs: (query, filters) => api.get('/search/dogs', { 
    params: { q: query, ...filters } 
  }),
  breeds: () => api.get('/search/breeds'),
  locations: (query) => api.get('/search/locations', { 
    params: { q: query } 
  }),
}

// Admin API
export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  getUsers: (params) => api.get('/admin/users', { params }),
  updateUserRole: (userId, role) => api.put(`/admin/users/${userId}/role`, { role }),
  deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
}

export default api
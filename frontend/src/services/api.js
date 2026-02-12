import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API Methods
export const songsAPI = {
  // Get all songs with pagination
  getAllSongs: (params = {}) => {
    const queryParams = new URLSearchParams({
      page: params.page || 1,
      per_page: params.per_page || 10,
      sort_by: params.sort_by || 'index',
      order: params.order || 'asc',
    }).toString();
    
    return api.get(`/songs?${queryParams}`);
  },

  // Search songs by title
  searchSongs: (title, exact = false) => {
    return api.get(`/songs/search?title=${encodeURIComponent(title)}&exact=${exact}`);
  },

  // Get song by ID
  getSongById: (id) => {
    return api.get(`/songs/${id}`);
  },

  // Update song rating
  updateRating: (id, rating) => {
    return api.put(`/songs/${id}/rating`, { rating });
  },

  // Get statistics
  getStats: () => {
    return api.get('/stats');
  },

  // Upload JSON data
  uploadData: (data) => {
    return api.post('/songs/upload', data);
  },
};

export default api;
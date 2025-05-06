import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Backend base URL
  withCredentials: true, // Include cookies in requests
});

// Add a response interceptor
// api.interceptors.response.use(
//   (response) => response, // Pass through successful responses
//   (error) => {
//     if (error.response && error.response.status === 401) {
//       // Redirect to login page on 401 Unauthorized
//       window.location.href = '/auth-failed';
//     }
//     return Promise.reject(error);
//   }
// );

export default api;
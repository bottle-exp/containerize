import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import BlogPage from './components/BlogPage';
import AuthFailed from './components/AuthFailed';
import api from './api/axiosInstance'; // Import Axios instance
import { AxiosError } from 'axios'; // Import AxiosError for better error handling

const App: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    // Prevent fetching user data on the /auth-failed route
    if (location.pathname === '/auth-failed') {
      return;
    }

    const fetchUser = async () => {
      try {
        const response = await api.get('/me'); // Call the /me endpoint
        setUser(response.data.user); // Set the user data
      } catch (error) {
        const axiosError = error as AxiosError;
        console.warn(
          'User is not authenticated:',
          axiosError.response?.data || axiosError.message
        );
        setUser(null); // Ensure user is null if not authenticated
        // navigate('/auth-failed'); // Redirect to the failed page
      }
    };

    // Fetch user details on app load
    fetchUser();
  }, [location.pathname, navigate]);

  return (
    <Routes>
      <Route path="/" element={<BlogPage user={user} />} />
      {/* <Route path="/auth-failed" element={<AuthFailed />} /> */}
    </Routes>
  );
};

export default App;
import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/LoginModal.module.css';
import api from '../api/axiosInstance';

interface LoginModalProps {
  onClose: () => void;
}

const LoginModal: React.FC<LoginModalProps> = ({ onClose }) => {
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      // Redirect to the backend login endpoint
      window.location.href = 'http://localhost:8000/login/';
    } catch (error) {
      console.error('Login failed:', error);
      navigate('/auth-failed'); // Redirect to /auth-failed on login failure
    }
  };

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <button className={styles.closeButton} onClick={onClose}>
          &times;
        </button>
        <h2 className={styles.title}>Log in to My Blog</h2>
        <button className={styles.loginButton} onClick={handleLogin}>
          Login with Google
        </button>
      </div>
    </div>
  );
};

export default LoginModal;
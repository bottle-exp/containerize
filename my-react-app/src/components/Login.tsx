import React, { useState } from 'react';
import styles from '../styles/Login.module.css';
import api from '../api/axiosInstance'; // Import the Axios instance

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError('');
        setLoading(true);

        if (!username || !password) {
            setError('Please fill in both fields.');
            setLoading(false);
            return;
        }

        try {
            const response = await api.post('/login', { username, password }); // Use Axios
            console.log('Login successful:', response.data);
        } catch (error: any) {
            setError(error.response?.data?.detail || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = () => {
        window.location.href = 'http://localhost:8000/login/';
    };

    return (
        <div className={styles.container}>
            <h2 className={styles.title}>Login</h2>
            <form onSubmit={handleSubmit} className={styles.form}>
                {error && <p className={styles.error}>{error}</p>}
                <div className={styles.inputGroup}>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className={styles.input}
                        placeholder="Enter your username"
                    />
                </div>
                <div className={styles.inputGroup}>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className={styles.input}
                        placeholder="Enter your password"
                    />
                </div>
                <button type="submit" className={styles.button} disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </form>
            <div className={styles.divider}>OR</div>
            <button className={styles.googleButton} onClick={handleGoogleLogin}>
                <img
                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png"
                    alt="Google Logo"
                    className={styles.googleIcon}
                />
                Login with Gmail
            </button>
        </div>
    );
};

export default Login;
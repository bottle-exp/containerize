import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/AuthFailed.module.css';

const AuthFailed: React.FC = () => {
    const navigate = useNavigate();

    const handleRetry = () => {
        navigate('/login'); // Redirect to the login page
    };

    const handleGoHome = () => {
        navigate('/'); // Redirect to the homepage
    };

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Authentication Failed</h1>
            <p className={styles.message}>
                We couldn't log you in. Please check your credentials or try again.
            </p>
            <div className={styles.actions}>
                <button className={styles.retryButton} onClick={handleRetry}>
                    Retry Login
                </button>
                <button className={styles.homeButton} onClick={handleGoHome}>
                    Go to Homepage
                </button>
            </div>
        </div>
    );
};

export default AuthFailed;
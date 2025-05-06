import React, { useState } from 'react';
import styles from '../styles/Navbar.module.css';
import LoginModal from './LoginModal';

const Navbar = () => {
    const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

    const handleLoginClick = () => {
        setIsLoginModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsLoginModalOpen(false);
    };

    return (
        <nav className={styles.navbar}>
            <div className={styles.logo}>My Blog</div>
            <ul className={styles.navLinks}>
                <li><a href="/">Home</a></li>
                <li><a href="/blog">Blog</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
            <button className={styles.loginButton} onClick={handleLoginClick}>
                Login
            </button>
            {isLoginModalOpen && <LoginModal onClose={handleCloseModal} />}
        </nav>
    );
};

export default Navbar;
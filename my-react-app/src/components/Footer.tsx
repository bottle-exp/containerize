import React from 'react';
import styles from '../styles/Footer.module.css';

const Footer = () => {
    return (
        <footer className={styles.footer}>
            <div className={styles.container}>
                <p className={styles.text}>
                    © 2025 My Blog. All rights reserved.
                </p>
                <div className={styles.links}>
                    <a href="/privacy" className={styles.link}>Privacy Policy</a>
                    <a href="/terms" className={styles.link}>Terms of Service</a>
                    <a href="/contact" className={styles.link}>Contact Us</a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
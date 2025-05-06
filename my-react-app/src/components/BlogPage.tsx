import React from 'react';
import Navbar from './Navbar';
import Footer from './Footer';
import styles from '../styles/BlogPage.module.css';

interface BlogPageProps {
  user: any; // User data passed as a prop
}

const BlogPage: React.FC<BlogPageProps> = ({ user }) => {
  return (
    <div>
      <Navbar />
      <div className={styles.container}>
        <h1 className={styles.title}>Welcome to My Blog</h1>
        {user ? (
          <p>Hello, {user.name || 'User'}! Enjoy your personalized experience.</p>
        ) : (
          <p>Welcome, guest! Please log in to access more features.</p>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default BlogPage;
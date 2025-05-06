import React from 'react';
import styles from '../styles/BlogCard.module.css';

interface BlogCardProps {
    title: string;
    author: string;
    date: string;
    excerpt: string;
    image: string;
}

const BlogCard: React.FC<BlogCardProps> = ({ title, author, date, excerpt, image }) => {
    return (
        <div className={styles.card}>
            <img src={image} alt={title} className={styles.image} />
            <div className={styles.content}>
                <h3 className={styles.title}>{title}</h3>
                <p className={styles.meta}>By {author} on {date}</p>
                <p className={styles.excerpt}>{excerpt}</p>
                <button className={styles.readMore}>Read More</button>
            </div>
        </div>
    );
};

export default BlogCard;
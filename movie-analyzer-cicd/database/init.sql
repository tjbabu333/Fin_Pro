-- Movie Review Database Initialization Script
-- This script creates multiple databases for different environments

-- Create user and set password
CREATE USER movieuser WITH ENCRYPTED PASSWORD 'moviepass';

-- Create databases for different environments
CREATE DATABASE moviereviews;        -- Production
CREATE DATABASE moviereviews_dev;    -- Development  
CREATE DATABASE moviereviews_staging; -- Staging

-- Grant permissions on all databases
GRANT ALL PRIVILEGES ON DATABASE moviereviews TO movieuser;
GRANT ALL PRIVILEGES ON DATABASE moviereviews_dev TO movieuser;
GRANT ALL PRIVILEGES ON DATABASE moviereviews_staging TO movieuser;

-- Initialize Production Database
\c moviereviews;

-- Grant schema permissions to user
GRANT ALL ON SCHEMA public TO movieuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO movieuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO movieuser;

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id BIGSERIAL PRIMARY KEY,
    movie_id VARCHAR(255) NOT NULL,
    review_text VARCHAR(2000) NOT NULL,
    sentiment VARCHAR(50),
    sentiment_score DOUBLE PRECISION,
    rating DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_reviews_movie_id ON reviews(movie_id);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment);

-- Grant permissions on the table to movieuser
GRANT ALL PRIVILEGES ON TABLE reviews TO movieuser;
GRANT USAGE, SELECT ON SEQUENCE reviews_id_seq TO movieuser;

-- Create a view for review statistics
CREATE OR REPLACE VIEW review_stats AS
SELECT 
    movie_id,
    COUNT(*) as total_reviews,
    AVG(rating) as avg_rating,
    AVG(sentiment_score) as avg_sentiment_score,
    COUNT(CASE WHEN sentiment = 'positive' THEN 1 END) as positive_reviews,
    COUNT(CASE WHEN sentiment = 'negative' THEN 1 END) as negative_reviews,
    COUNT(CASE WHEN sentiment = 'neutral' THEN 1 END) as neutral_reviews,
    MAX(created_at) as latest_review
FROM reviews 
GROUP BY movie_id;

-- Grant permissions on the view
GRANT ALL PRIVILEGES ON TABLE review_stats TO movieuser;

-- Insert production sample data
INSERT INTO reviews (movie_id, review_text, sentiment, sentiment_score, rating, created_at) VALUES
('shawshank', 'This is an absolutely incredible movie! The story is so inspiring and the acting is phenomenal.', 'positive', 0.95, 4.8, '2024-01-15 10:30:00'),
('inception', 'Mind-bending plot that keeps you thinking long after the credits roll. Christopher Nolan at his finest.', 'positive', 0.88, 4.6, '2024-01-16 14:22:00'),
('interstellar', 'A beautiful exploration of love, time, and space. Visually stunning with an emotional core.', 'positive', 0.92, 4.7, '2024-01-17 09:15:00'),
('fight-club', 'Dark and twisted but brilliantly executed. Not for everyone but definitely memorable.', 'neutral', 0.65, 3.8, '2024-01-18 16:45:00'),
('gladiator', 'Epic historical drama with Russell Crowe delivering a powerful performance.', 'positive', 0.85, 4.4, '2024-01-19 11:30:00'),
('dark-knight', 'Heath Ledger''s Joker is absolutely legendary. A masterpiece of the superhero genre.', 'positive', 0.93, 4.9, '2024-01-20 13:20:00');

-- Initialize Development Database
\c moviereviews_dev;

-- Grant schema permissions to user
GRANT ALL ON SCHEMA public TO movieuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO movieuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO movieuser;

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id BIGSERIAL PRIMARY KEY,
    movie_id VARCHAR(255) NOT NULL,
    review_text VARCHAR(2000) NOT NULL,
    sentiment VARCHAR(50),
    sentiment_score DOUBLE PRECISION,
    rating DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_reviews_movie_id ON reviews(movie_id);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment);

-- Grant permissions on the table to movieuser
GRANT ALL PRIVILEGES ON TABLE reviews TO movieuser;
GRANT USAGE, SELECT ON SEQUENCE reviews_id_seq TO movieuser;

-- Create a view for review statistics
CREATE OR REPLACE VIEW review_stats AS
SELECT 
    movie_id,
    COUNT(*) as total_reviews,
    AVG(rating) as avg_rating,
    AVG(sentiment_score) as avg_sentiment_score,
    COUNT(CASE WHEN sentiment = 'positive' THEN 1 END) as positive_reviews,
    COUNT(CASE WHEN sentiment = 'negative' THEN 1 END) as negative_reviews,
    COUNT(CASE WHEN sentiment = 'neutral' THEN 1 END) as neutral_reviews,
    MAX(created_at) as latest_review
FROM reviews 
GROUP BY movie_id;

-- Grant permissions on the view
GRANT ALL PRIVILEGES ON TABLE review_stats TO movieuser;

-- Insert development sample data
INSERT INTO reviews (movie_id, review_text, sentiment, sentiment_score, rating, created_at) VALUES
('shawshank', 'Development test review - This is a great movie for testing!', 'positive', 0.90, 4.5, '2024-01-15 10:30:00'),
('inception', 'Dev environment - Complex plot but good for testing sentiment analysis.', 'positive', 0.80, 4.2, '2024-01-16 14:22:00'),
('test-movie', 'This is a test movie review for development purposes.', 'neutral', 0.50, 3.0, '2024-01-17 09:15:00');

-- Initialize Staging Database  
\c moviereviews_staging;

-- Grant schema permissions to user
GRANT ALL ON SCHEMA public TO movieuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO movieuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO movieuser;

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id BIGSERIAL PRIMARY KEY,
    movie_id VARCHAR(255) NOT NULL,
    review_text VARCHAR(2000) NOT NULL,
    sentiment VARCHAR(50),
    sentiment_score DOUBLE PRECISION,
    rating DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_reviews_movie_id ON reviews(movie_id);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment);

-- Grant permissions on the table to movieuser
GRANT ALL PRIVILEGES ON TABLE reviews TO movieuser;
GRANT USAGE, SELECT ON SEQUENCE reviews_id_seq TO movieuser;

-- Create a view for review statistics
CREATE OR REPLACE VIEW review_stats AS
SELECT 
    movie_id,
    COUNT(*) as total_reviews,
    AVG(rating) as avg_rating,
    AVG(sentiment_score) as avg_sentiment_score,
    COUNT(CASE WHEN sentiment = 'positive' THEN 1 END) as positive_reviews,
    COUNT(CASE WHEN sentiment = 'negative' THEN 1 END) as negative_reviews,
    COUNT(CASE WHEN sentiment = 'neutral' THEN 1 END) as neutral_reviews,
    MAX(created_at) as latest_review
FROM reviews 
GROUP BY movie_id;

-- Grant permissions on the view
GRANT ALL PRIVILEGES ON TABLE review_stats TO movieuser;

-- Insert staging sample data
INSERT INTO reviews (movie_id, review_text, sentiment, sentiment_score, rating, created_at) VALUES
('shawshank', 'Staging test - Excellent movie for user acceptance testing.', 'positive', 0.88, 4.6, '2024-01-15 10:30:00'),
('inception', 'Staging environment - Great for testing the complete flow.', 'positive', 0.85, 4.4, '2024-01-16 14:22:00'),
('staging-movie', 'This review is specifically for staging environment testing.', 'positive', 0.75, 4.0, '2024-01-17 09:15:00'),
('dark-knight', 'UAT review - Batman movie testing in staging.', 'positive', 0.90, 4.7, '2024-01-18 16:45:00');

-- Display initialization summary
\echo ''
\echo '========================================='
\echo 'Movie Review Databases Initialized Successfully!'
\echo '========================================='
\echo 'Databases Created:'
\echo '  - moviereviews (Production): 6 reviews'
\echo '  - moviereviews_dev (Development): 3 reviews'  
\echo '  - moviereviews_staging (Staging): 4 reviews'
\echo 'User: movieuser'
\echo 'Tables in each DB: reviews, review_stats (view)'
\echo '========================================='
\echo ''

-- Connect back to production and show sample
\c moviereviews;
SELECT 'Production Sample Reviews:' as info;
SELECT movie_id, LEFT(review_text, 50) || '...' as review_preview, sentiment, rating 
FROM reviews 
ORDER BY created_at 
LIMIT 3; 
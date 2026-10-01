CREATE TABLE IF NOT EXISTS reviews (
    id BIGSERIAL PRIMARY KEY,
    movie_id VARCHAR(255) NOT NULL,
    review_text VARCHAR(2000) NOT NULL,
    sentiment VARCHAR(50),
    sentiment_score DOUBLE PRECISION,
    rating DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reviews_movie_id ON reviews(movie_id);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at);

INSERT INTO reviews (movie_id, review_text, sentiment, sentiment_score, rating)
SELECT * FROM (VALUES
    ('shawshank', 'An inspiring story with unforgettable performances.', 'positive', 0.80, 4.8),
    ('inception', 'A smart and visually impressive science fiction movie.', 'positive', 0.72, 4.7),
    ('interstellar', 'Beautiful visuals and an emotional story about time and family.', 'positive', 0.75, 4.7),
    ('fight-club', 'Dark, unusual and thought provoking.', 'positive', 0.35, 4.4),
    ('gladiator', 'Epic action and a powerful lead performance.', 'positive', 0.67, 4.6),
    ('dark-knight', 'A gripping superhero film with a memorable villain.', 'positive', 0.70, 4.9),
    ('Peddi', 'It was a massive Indian rooted film which includes sports drama with great acting.', 'Blockbuster',0.90,5.0) 
) AS seed(movie_id, review_text, sentiment, sentiment_score, rating)
WHERE NOT EXISTS (SELECT 1 FROM reviews);

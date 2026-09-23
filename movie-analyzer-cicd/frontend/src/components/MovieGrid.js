import React, { useState } from 'react';

/**
 * MovieGrid Component
 * Displays movie thumbnails in a grid layout
 * Works even when backend is down - shows movies with thumbnails
 */
function MovieGrid({ movies, onMovieSelect }) {
  const [imageErrors, setImageErrors] = useState({});

  const handleImageError = (movieId) => {
    setImageErrors(prev => ({ ...prev, [movieId]: true }));
  };

  const handleMovieClick = (movie) => {
    onMovieSelect(movie);
  };

  return (
    <div className="movies-grid">
      {movies.map(movie => (
        <div 
          key={movie.id} 
          className="movie-card"
          onClick={() => handleMovieClick(movie)}
        >
          <div className="movie-thumbnail">
            {imageErrors[movie.id] ? (
              <div className="movie-thumbnail-placeholder">
                🎬
              </div>
            ) : (
              <img
                src={movie.thumbnail}
                alt={movie.title}
                onError={() => handleImageError(movie.id)}
              />
            )}
          </div>
          
          <div className="movie-info">
            <div className="movie-title">{movie.title}</div>
            <div className="movie-meta">
              <span>{movie.year}</span>
              <span className="movie-genre">{movie.genre}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MovieGrid; 
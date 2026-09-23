import React, { useState } from 'react';

/**
 * MovieDetail Component
 * Shows detailed movie view with review submission and history
 * Handles service availability states as specified in rules
 */
function MovieDetail({ 
  movie, 
  reviews, 
  serviceStatus, 
  onSubmitReview, 
  onBack, 
  submitting,
  latestAnalysis
}) {
  const [reviewText, setReviewText] = useState('');
  const [imageError, setImageError] = useState(false);

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    
    if (!reviewText.trim()) {
      alert('Please enter a review');
      return;
    }

    const success = await onSubmitReview(movie.id, reviewText.trim());
    
    if (success) {
      setReviewText('');
    }
  };

  // Check if review submission should be disabled
  const isSubmissionDisabled = () => {
    return !serviceStatus.backend || submitting;
  };

  // Get submission status message
  const getSubmissionStatusMessage = () => {
    if (!serviceStatus.backend) {
      return '❌ Backend service unavailable - cannot submit reviews';
    }
    if (!serviceStatus.database && !serviceStatus.model) {
      return '⚠️ Both database and model server unavailable';
    }
    if (!serviceStatus.database) {
      return '⚠️ Database unavailable - reviews will be analyzed but not saved';
    }
    if (!serviceStatus.model) {
      return '⚠️ Model server unavailable - cannot analyze sentiment';
    }
    return '✅ All services available';
  };

  // Get reviews display message
  const getReviewsStatusMessage = () => {
    if (!serviceStatus.backend) {
      return 'Cannot load reviews - backend service unavailable';
    }
    if (!serviceStatus.database) {
      return 'Database connection failed - cannot load reviews';
    }
    return null;
  };

  const reviewsError = getReviewsStatusMessage();

  return (
    <div className="movie-detail">
      <button className="back-button" onClick={onBack}>
        ← Back to Movies
      </button>

      <div className="movie-detail-header">
        <div className="movie-detail-thumbnail">
          {imageError ? (
            <div className="movie-thumbnail-placeholder" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              fontSize: '3rem',
              background: 'linear-gradient(45deg, #f3f4f6, #e5e7eb)',
              width: '100%',
              height: '100%'
            }}>
              🎬
            </div>
          ) : (
            <img
              src={movie.thumbnail}
              alt={movie.title}
              onError={() => setImageError(true)}
            />
          )}
        </div>
        
        <div className="movie-detail-info">
          <h2>{movie.title}</h2>
          <div style={{ color: '#6b7280', marginBottom: '1rem' }}>
            <p><strong>Year:</strong> {movie.year}</p>
            <p><strong>Genre:</strong> {movie.genre}</p>
            <p><strong>Movie ID:</strong> {movie.id}</p>
          </div>
        </div>
      </div>

      {/* Service Status Message */}
      <div style={{ marginBottom: '2rem' }}>
        <div 
          className={serviceStatus.backend ? 'status-online' : 'status-offline'}
          style={{ 
            padding: '0.75rem', 
            borderRadius: '8px', 
            textAlign: 'center',
            fontSize: '0.9rem'
          }}
        >
          {getSubmissionStatusMessage()}
        </div>
      </div>

      {/* Review Submission Form */}
      <div style={{ 
        background: '#f8fafc', 
        padding: '2rem', 
        borderRadius: '12px', 
        marginBottom: '2rem',
        border: '1px solid #e2e8f0'
      }}>
        <h3 style={{ marginBottom: '1rem', color: '#1f2937' }}>
          ✍️ Write Your Review for {movie.title}
        </h3>
        
        <form onSubmit={handleSubmitReview}>
          <div className="form-group">
            <label className="form-label">Your Review</label>
            <textarea
              className="form-textarea"
              placeholder={`Share your thoughts about ${movie.title}...`}
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              disabled={isSubmissionDisabled()}
              rows="4"
            />
          </div>

          <button 
            type="submit" 
            className="button button-success"
            disabled={isSubmissionDisabled() || !reviewText.trim()}
          >
            {submitting ? (
              <>
                <div className="loading-spinner"></div>
                Submitting...
              </>
            ) : (
              <>
                📝 Submit Review
              </>
            )}
          </button>
        </form>
      </div>

      {/* Latest Review Analysis - Show results prominently */}
      {latestAnalysis && latestAnalysis.movieId === movie.id && (
        <div style={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          padding: '2rem', 
          borderRadius: '16px', 
          marginBottom: '2rem',
          color: 'white',
          boxShadow: '0 10px 25px rgba(102, 126, 234, 0.3)'
        }}>
          <h3 style={{ 
            marginBottom: '1.5rem', 
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '1.2rem'
          }}>
            🎯 Your Latest Review Analysis
          </h3>
          
          <div style={{ 
            background: 'rgba(255, 255, 255, 0.15)',
            borderRadius: '12px',
            padding: '1.5rem',
            backdropFilter: 'blur(10px)'
          }}>
            {/* Review Text */}
            <div style={{ marginBottom: '1rem' }}>
              <h4 style={{ color: 'rgba(255, 255, 255, 0.9)', marginBottom: '0.5rem', fontSize: '0.9rem' }}>
                📝 YOUR REVIEW
              </h4>
              <p style={{ 
                fontSize: '1.1rem', 
                fontStyle: 'italic',
                lineHeight: '1.4',
                color: 'white'
              }}>
                "{latestAnalysis.reviewText}"
              </p>
            </div>

            {/* Analysis Results */}
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', 
              gap: '1rem',
              marginTop: '1.5rem'
            }}>
              {/* Sentiment */}
              <div style={{ 
                background: 'rgba(255, 255, 255, 0.2)',
                borderRadius: '10px',
                padding: '1rem',
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                  {latestAnalysis.sentiment === 'positive' ? '😊' : 
                   latestAnalysis.sentiment === 'negative' ? '😞' : '😐'}
                </div>
                <div style={{ 
                  fontSize: '0.8rem', 
                  opacity: 0.8, 
                  marginBottom: '0.25rem' 
                }}>
                  SENTIMENT
                </div>
                <div style={{ 
                  fontSize: '1.1rem', 
                  fontWeight: 'bold',
                  textTransform: 'uppercase'
                }}>
                  {latestAnalysis.sentiment}
                </div>
              </div>

              {/* Rating */}
              <div style={{ 
                background: 'rgba(255, 255, 255, 0.2)',
                borderRadius: '10px',
                padding: '1rem',
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                  ⭐
                </div>
                <div style={{ 
                  fontSize: '0.8rem', 
                  opacity: 0.8, 
                  marginBottom: '0.25rem' 
                }}>
                  RATING
                </div>
                <div style={{ 
                  fontSize: '1.1rem', 
                  fontWeight: 'bold'
                }}>
                  {latestAnalysis.rating.toFixed(1)}/5.0
                </div>
              </div>

              {/* Confidence Score */}
              <div style={{ 
                background: 'rgba(255, 255, 255, 0.2)',
                borderRadius: '10px',
                padding: '1rem',
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                  📊
                </div>
                <div style={{ 
                  fontSize: '0.8rem', 
                  opacity: 0.8, 
                  marginBottom: '0.25rem' 
                }}>
                  CONFIDENCE
                </div>
                <div style={{ 
                  fontSize: '1.1rem', 
                  fontWeight: 'bold'
                }}>
                  {(latestAnalysis.sentimentScore * 100).toFixed(0)}%
                </div>
              </div>
            </div>

            {/* Timestamp */}
            <div style={{ 
              marginTop: '1rem', 
              textAlign: 'center', 
              fontSize: '0.8rem', 
              opacity: 0.7 
            }}>
              Analyzed {new Date(latestAnalysis.timestamp).toLocaleString()}
            </div>
          </div>
        </div>
      )}

      {/* Reviews History */}
      <div>
        <h3 style={{ 
          marginBottom: '1rem', 
          color: '#1f2937',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          📖 Reviews for {movie.title} ({reviews?.length || 0})
        </h3>
        
        {reviewsError ? (
          <div className="error-message">
            {reviewsError}
          </div>
        ) : reviews?.length > 0 ? (
          <div>
            {reviews.map((review, index) => (
              <div key={index} className="review-card">
                <div className="review-text">"{review.reviewText}"</div>
                <div className="review-meta">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <span 
                      className={`sentiment-badge sentiment-${review.sentiment}`}
                      style={{
                        padding: '0.25rem 0.5rem',
                        borderRadius: '12px',
                        fontSize: '0.8rem',
                        fontWeight: 'bold',
                        textTransform: 'uppercase',
                        backgroundColor: review.sentiment === 'positive' ? '#dcfce7' : 
                                       review.sentiment === 'negative' ? '#fef2f2' : '#f1f5f9',
                        color: review.sentiment === 'positive' ? '#166534' : 
                               review.sentiment === 'negative' ? '#dc2626' : '#475569'
                      }}
                    >
                      {review.sentiment === 'positive' ? '😊 Positive' : 
                       review.sentiment === 'negative' ? '😞 Negative' : '😐 Neutral'}
                    </span>
                    <span style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: '0.25rem',
                      fontSize: '0.9rem',
                      fontWeight: '500'
                    }}>
                      ⭐ {review.rating ? review.rating.toFixed(1) : '0.0'}/5.0 stars
                    </span>
                    {review.sentimentScore !== undefined && (
                      <span style={{ 
                        fontSize: '0.8rem', 
                        color: '#6b7280',
                        padding: '0.2rem 0.4rem',
                        background: '#f9fafb',
                        borderRadius: '8px'
                      }}>
                        Score: {review.sentimentScore.toFixed(2)}
                      </span>
                    )}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#9ca3af', marginTop: '0.5rem' }}>
                    {review.timestamp ? new Date(review.timestamp).toLocaleDateString() : 'Just now'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">🎬</div>
            <p>No reviews yet for {movie.title}</p>
            <p style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
              Be the first to share your thoughts!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default MovieDetail; 
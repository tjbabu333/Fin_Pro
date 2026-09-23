import React from 'react';
import { MOVIES } from '../data/movies';

/**
 * LatestReviews Component
 * Displays the latest 5 reviews across all movies on the homepage
 */
function LatestReviews({ latestReviews }) {
  // Get movie title by ID
  const getMovieTitle = (movieId) => {
    const movie = MOVIES.find(m => m.id === movieId);
    return movie ? movie.title : movieId;
  };

  // Format date
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
      });
    } catch {
      return 'Recent';
    }
  };

  // Get emoji for sentiment
  const getSentimentEmoji = (sentiment) => {
    switch (sentiment) {
      case 'positive': return '😊';
      case 'negative': return '😞';
      default: return '😐';
    }
  };

  if (!latestReviews || latestReviews.length === 0) {
    return (
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: '16px',
        padding: '2rem',
        marginTop: '2rem',
        textAlign: 'center',
        border: '1px solid rgba(255, 255, 255, 0.2)'
      }}>
        <h3 style={{ 
          color: '#1f2937', 
          marginBottom: '1rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.5rem'
        }}>
          📝 Latest Community Reviews
        </h3>
        <p style={{ color: '#6b7280' }}>
          No reviews available yet. Be the first to share your thoughts!
        </p>
      </div>
    );
  }

  return (
    <div style={{
      background: 'rgba(255, 255, 255, 0.95)',
      borderRadius: '16px',
      padding: '2rem',
      marginTop: '2rem',
      border: '1px solid rgba(255, 255, 255, 0.2)',
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
    }}>
      <h3 style={{ 
        color: '#1f2937', 
        marginBottom: '1.5rem',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        fontSize: '1.5rem'
      }}>
        📝 Latest Community Reviews
      </h3>
      
      <div style={{
        display: 'grid',
        gap: '1rem'
      }}>
        {latestReviews.map((review, index) => (
          <div key={review.id || index} style={{
            background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
            borderRadius: '12px',
            padding: '1.5rem',
            border: '1px solid #e2e8f0',
            transition: 'all 0.3s ease',
            ':hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)'
            }
          }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'flex-start',
              marginBottom: '0.5rem'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}>
                <span style={{ fontSize: '1.1rem', fontWeight: '600', color: '#1f2937' }}>
                  {getMovieTitle(review.movieId)}
                </span>
                <span style={{
                  background: review.sentiment === 'positive' ? '#dcfce7' : 
                             review.sentiment === 'negative' ? '#fef2f2' : '#f1f5f9',
                  color: review.sentiment === 'positive' ? '#166534' : 
                         review.sentiment === 'negative' ? '#dc2626' : '#475569',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '12px',
                  fontSize: '0.8rem',
                  fontWeight: '500',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.25rem'
                }}>
                  {getSentimentEmoji(review.sentiment)} {review.sentiment || 'neutral'}
                </span>
              </div>
              
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                fontSize: '0.9rem',
                color: '#6b7280'
              }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  ⭐ {(review.rating || 0).toFixed(1)}
                </span>
                <span>•</span>
                <span>{formatDate(review.createdAt)}</span>
              </div>
            </div>
            
            <p style={{
              color: '#374151',
              fontSize: '0.95rem',
              lineHeight: '1.5',
              margin: 0,
              fontStyle: 'italic'
            }}>
              "{review.reviewText}"
            </p>
          </div>
        ))}
      </div>
      
      <div style={{
        textAlign: 'center',
        marginTop: '1.5rem',
        padding: '1rem',
        background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
        borderRadius: '10px'
      }}>
        <p style={{
          color: '#0369a1',
          fontSize: '0.9rem',
          margin: 0,
          fontWeight: '500'
        }}>
          💡 Click on any movie above to add your own review and see AI sentiment analysis!
        </p>
      </div>
    </div>
  );
}

export default LatestReviews; 
package com.moviereview.service;

import com.moviereview.entity.Review;
import com.moviereview.repository.ReviewRepository;
import com.moviereview.service.ModelServerService.SentimentResult;
import com.moviereview.service.ModelServerService.ModelServerException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataAccessException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class ReviewService {

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private ModelServerService modelServerService;

    private boolean databaseConnected = true; // Default to true - only disable through admin for failure simulation

    /**
     * Get all reviews for a movie
     */
    public List<Review> getReviewsByMovieId(String movieId) {
        if (!databaseConnected) {
            throw new DatabaseException("Database connection is disabled - review history is not available");
        }

        try {
            System.out.println("🗄️ Fetching reviews for movie: " + movieId);
            List<Review> reviews = reviewRepository.findByMovieIdOrderByCreatedAtDesc(movieId);
            System.out.println("✅ Found " + reviews.size() + " reviews for movie: " + movieId);
            return reviews;
        } catch (DataAccessException e) {
            System.err.println("❌ Database error while fetching reviews: " + e.getMessage());
            throw new DatabaseException("Database is down - review history does not work at this moment");
        }
    }

    /**
     * Submit a new review
     */
    public ReviewSubmissionResult submitReview(String movieId, String reviewText) {
        System.out.println("📝 Submitting review for movie: " + movieId);
        
        // Validate input
        if (movieId == null || movieId.trim().isEmpty()) {
            throw new IllegalArgumentException("Movie ID is required");
        }
        if (reviewText == null || reviewText.trim().isEmpty()) {
            throw new IllegalArgumentException("Review text is required");
        }

        // First, try to get sentiment analysis from model server
        SentimentResult sentimentResult;
        try {
            sentimentResult = modelServerService.analyzeSentiment(reviewText);
        } catch (ModelServerException e) {
            // Model server is down - reject the review
            System.err.println("❌ Cannot submit review: " + e.getMessage());
            throw new ReviewSubmissionException(e.getMessage());
        }

        // Check database availability before any database operations
        if (!databaseConnected) {
            // Database is down - analysis was done but can't be stored
            System.err.println("❌ Review analyzed but cannot be saved: Database is down");
            
            // Create review object without saving (for response only)
            Review review = new Review();
            review.setMovieId(movieId);
            review.setReviewText(reviewText);
            review.setSentiment(sentimentResult.getSentiment());
            review.setSentimentScore(sentimentResult.getScore());
            review.setRating(sentimentResult.getRating());
            
            return new ReviewSubmissionResult(false, review, 
                "Review was analyzed but could not be saved - database is down. History does not work at this moment.");
        }

        // Only try database operations if connection is enabled
        try {
            // Create review object for saving
            Review review = new Review(movieId, reviewText, 
                                     sentimentResult.getSentiment(), 
                                     sentimentResult.getScore(),
                                     sentimentResult.getRating());
            
            Review savedReview = reviewRepository.save(review);
            System.out.println("✅ Review saved successfully with ID: " + savedReview.getId());
            return new ReviewSubmissionResult(true, savedReview, "Review submitted successfully");
        } catch (Exception e) {
            // Any database exception - return graceful response
            System.err.println("❌ Database error while saving review: " + e.getMessage());
            
            // Create review object for response
            Review review = new Review();
            review.setMovieId(movieId);
            review.setReviewText(reviewText);
            review.setSentiment(sentimentResult.getSentiment());
            review.setSentimentScore(sentimentResult.getScore());
            review.setRating(sentimentResult.getRating());
            
            return new ReviewSubmissionResult(false, review, 
                "Review was analyzed but could not be saved - database is down. History does not work at this moment.");
        }
    }

    /**
     * Check database connection status
     */
    public boolean isDatabaseAvailable() {
        if (!databaseConnected) {
            return false;
        }

        try {
            // Try a simple query to check database connectivity
            reviewRepository.count();
            return true;
        } catch (Exception e) {
            // Catch ALL exceptions, not just DataAccessException
            System.err.println("❌ Database health check failed: " + e.getMessage());
            return false;
        }
    }

    /**
     * Admin function to toggle database connection simulation
     */
    public void toggleDatabaseConnection() {
        databaseConnected = !databaseConnected;
        System.out.println("🔧 Database connection toggled: " + (databaseConnected ? "ENABLED" : "DISABLED"));
    }

    /**
     * Get current database connection status
     */
    public boolean isDatabaseConnectionEnabled() {
        return databaseConnected;
    }

    /**
     * Get review statistics for admin panel
     */
    public Map<String, Object> getReviewStats() {
        try {
            long totalReviews = reviewRepository.count();
            return Map.of(
                "totalReviews", totalReviews,
                "databaseConnected", isDatabaseAvailable()
            );
        } catch (Exception e) {
            return Map.of(
                "totalReviews", 0,
                "databaseConnected", false,
                "error", "Database unavailable"
            );
        }
    }

    /**
     * Get latest reviews across all movies
     */
    public List<Review> getLatestReviews(int limit) {
        if (!databaseConnected) {
            throw new DatabaseException("Database connection is disabled - latest reviews are not available");
        }

        try {
            System.out.println("🗄️ Fetching latest 5 reviews across all movies");
            List<Review> reviews = reviewRepository.findTop5ByOrderByCreatedAtDesc();
            System.out.println("✅ Found " + reviews.size() + " latest reviews");
            return reviews;
        } catch (DataAccessException e) {
            System.err.println("❌ Database error while fetching latest reviews: " + e.getMessage());
            throw new DatabaseException("Database is down - latest reviews are not available");
        }
    }

    /**
     * Review submission result
     */
    public static class ReviewSubmissionResult {
        private final boolean success;
        private final Review review;
        private final String message;

        public ReviewSubmissionResult(boolean success, Review review, String message) {
            this.success = success;
            this.review = review;
            this.message = message;
        }

        public boolean isSuccess() {
            return success;
        }

        public Review getReview() {
            return review;
        }

        public String getMessage() {
            return message;
        }
    }

    /**
     * Custom exceptions
     */
    public static class DatabaseException extends RuntimeException {
        public DatabaseException(String message) {
            super(message);
        }
    }

    public static class ReviewSubmissionException extends RuntimeException {
        public ReviewSubmissionException(String message) {
            super(message);
        }
    }
} 
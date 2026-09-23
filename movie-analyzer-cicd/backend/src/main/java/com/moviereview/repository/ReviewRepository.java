package com.moviereview.repository;

import com.moviereview.entity.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {
    
    /**
     * Find all reviews for a specific movie
     */
    List<Review> findByMovieIdOrderByCreatedAtDesc(String movieId);
    
    /**
     * Count reviews for a specific movie
     */
    long countByMovieId(String movieId);
    
    /**
     * Find recent reviews (for demo purposes)
     */
    @Query("SELECT r FROM Review r ORDER BY r.createdAt DESC")
    List<Review> findRecentReviews();
    
    /**
     * Find top N latest reviews across all movies
     */
    List<Review> findTop5ByOrderByCreatedAtDesc();
} 
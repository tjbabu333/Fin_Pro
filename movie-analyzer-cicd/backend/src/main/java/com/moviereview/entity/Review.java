package com.moviereview.entity;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import java.time.LocalDateTime;

@Entity
@Table(name = "reviews")
public class Review {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "movie_id", nullable = false)
    private String movieId;
    
    @Column(name = "review_text", nullable = false, length = 2000)
    private String reviewText;
    
    @Column(name = "sentiment")
    private String sentiment;
    
    @Column(name = "sentiment_score")
    private Double sentimentScore;
    
    @Column(name = "rating")
    private Double rating;
    
    @Column(name = "created_at")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createdAt;
    
    // Default constructor
    public Review() {
        this.createdAt = LocalDateTime.now();
    }
    
    // Constructor with parameters
    public Review(String movieId, String reviewText, String sentiment, Double sentimentScore, Double rating) {
        this.movieId = movieId;
        this.reviewText = reviewText;
        this.sentiment = sentiment;
        this.sentimentScore = sentimentScore;
        this.rating = rating;
        this.createdAt = LocalDateTime.now();
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getMovieId() {
        return movieId;
    }
    
    public void setMovieId(String movieId) {
        this.movieId = movieId;
    }
    
    public String getReviewText() {
        return reviewText;
    }
    
    public void setReviewText(String reviewText) {
        this.reviewText = reviewText;
    }
    
    public String getSentiment() {
        return sentiment;
    }
    
    public void setSentiment(String sentiment) {
        this.sentiment = sentiment;
    }
    
    public Double getSentimentScore() {
        return sentimentScore;
    }
    
    public void setSentimentScore(Double sentimentScore) {
        this.sentimentScore = sentimentScore;
    }
    
    public Double getRating() {
        return rating;
    }
    
    public void setRating(Double rating) {
        this.rating = rating;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    @Override
    public String toString() {
        return "Review{" +
                "id=" + id +
                ", movieId='" + movieId + '\'' +
                ", reviewText='" + reviewText + '\'' +
                ", sentiment='" + sentiment + '\'' +
                ", sentimentScore=" + sentimentScore +
                ", rating=" + rating +
                ", createdAt=" + createdAt +
                '}';
    }
} 
package com.moviereview.controller;

import com.moviereview.entity.Review;
import com.moviereview.service.ReviewService;
import com.moviereview.service.ReviewService.ReviewSubmissionResult;
import com.moviereview.service.ReviewService.DatabaseException;
import com.moviereview.service.ReviewService.ReviewSubmissionException;
import com.moviereview.service.AdminService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import jakarta.servlet.http.HttpServletRequest;
import java.io.BufferedReader;
import java.lang.StringBuilder;

@RestController
@RequestMapping("/api/reviews")
@CrossOrigin(origins = "*")
public class ReviewController {

    @Autowired
    private ReviewService reviewService;

    @Autowired
    private AdminService adminService;

    /**
     * Get all reviews for a specific movie
     */
    @GetMapping("/{movieId}")
    public ResponseEntity<?> getReviewsByMovieId(@PathVariable String movieId) {
        // Check if backend is healthy
        if (!adminService.isBackendHealthy()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Backend service is unhealthy"));
        }

        try {
            System.out.println("📋 GET /api/reviews/" + movieId);
            List<Review> reviews = reviewService.getReviewsByMovieId(movieId);
            return ResponseEntity.ok(reviews);
        } catch (DatabaseException e) {
            System.err.println("❌ Database error: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            System.err.println("❌ Unexpected error: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Internal server error"));
        }
    }

    /**
     * Submit a new review - DISABLED due to proxy compatibility issues
     */
    @PostMapping("/legacy")
    public ResponseEntity<?> submitReviewLegacy(@RequestBody Map<String, String> request) {
        // Check if backend is healthy
        if (!adminService.isBackendHealthy()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Backend service is unhealthy"));
        }

        try {
            String movieId = request.get("movieId");
            String reviewText = request.get("reviewText");

            System.out.println("📝 POST /api/reviews/legacy - Movie: " + movieId);

            // Validate input
            if (movieId == null || movieId.trim().isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(Map.of("error", "Movie ID is required"));
            }
            if (reviewText == null || reviewText.trim().isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(Map.of("error", "Review text is required"));
            }

            ReviewSubmissionResult result = reviewService.submitReview(movieId, reviewText);

            if (result.isSuccess()) {
                return ResponseEntity.ok(Map.of(
                    "review", result.getReview(),
                    "message", result.getMessage()
                ));
            } else {
                // Review was analyzed but not saved (database issue)
                return ResponseEntity.status(HttpStatus.PARTIAL_CONTENT)
                        .body(Map.of(
                            "review", result.getReview(),
                            "message", result.getMessage(),
                            "warning", "Review analysis completed but storage failed"
                        ));
            }

        } catch (ReviewSubmissionException e) {
            // Model server is down - reject the review
            System.err.println("❌ Review submission failed: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", e.getMessage()));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            System.err.println("❌ Unexpected error during review submission: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Internal server error"));
        }
    }

    /**
     * Submit a new review - Primary endpoint with proxy compatibility
     */
    @PostMapping
    public ResponseEntity<?> submitReview(
            @RequestParam(required = false) String movieId,
            @RequestParam(required = false) String reviewText,
            @RequestBody(required = false) Map<String, String> requestBody,
            HttpServletRequest request) {
        
        // Check if backend is healthy
        if (!adminService.isBackendHealthy()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Backend service is unhealthy"));
        }

        try {
            // Try to get parameters from request body first, then fall back to query params
            String finalMovieId = movieId;
            String finalReviewText = reviewText;
            
            if (requestBody != null && !requestBody.isEmpty()) {
                finalMovieId = requestBody.getOrDefault("movieId", movieId);
                finalReviewText = requestBody.getOrDefault("reviewText", reviewText);
            }
            
            // If still null, try to read from request stream manually
            if ((finalMovieId == null || finalReviewText == null) && request.getContentLength() > 0) {
                try {
                    StringBuilder sb = new StringBuilder();
                    BufferedReader reader = request.getReader();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        sb.append(line);
                    }
                    String body = sb.toString();
                    
                    // Simple JSON parsing for movieId and reviewText
                    if (body.contains("movieId") && body.contains("reviewText")) {
                        // Extract movieId
                        int movieIdStart = body.indexOf("\"movieId\"") + 11;
                        int movieIdEnd = body.indexOf("\"", movieIdStart);
                        if (movieIdEnd > movieIdStart) {
                            finalMovieId = body.substring(movieIdStart, movieIdEnd);
                        }
                        
                        // Extract reviewText
                        int reviewStart = body.indexOf("\"reviewText\"") + 14;
                        int reviewEnd = body.lastIndexOf("\"");
                        if (reviewEnd > reviewStart) {
                            finalReviewText = body.substring(reviewStart, reviewEnd);
                        }
                    }
                } catch (Exception e) {
                    System.err.println("❌ Failed to manually parse request body: " + e.getMessage());
                }
            }

            System.out.println("📝 POST /api/reviews - Movie: " + finalMovieId);

            // Validate input
            if (finalMovieId == null || finalMovieId.trim().isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(Map.of("error", "Movie ID is required"));
            }
            if (finalReviewText == null || finalReviewText.trim().isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(Map.of("error", "Review text is required"));
            }

            ReviewSubmissionResult result = reviewService.submitReview(finalMovieId, finalReviewText);

            if (result.isSuccess()) {
                return ResponseEntity.ok(Map.of(
                    "review", result.getReview(),
                    "message", result.getMessage()
                ));
            } else {
                // Review was analyzed but not saved (database issue)
                return ResponseEntity.status(HttpStatus.PARTIAL_CONTENT)
                        .body(Map.of(
                            "review", result.getReview(),
                            "message", result.getMessage(),
                            "warning", "Review analysis completed but storage failed"
                        ));
            }

        } catch (ReviewSubmissionException e) {
            // Model server is down - reject the review
            System.err.println("❌ Review submission failed: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", e.getMessage()));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            System.err.println("❌ Unexpected error during review submission: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Internal server error"));
        }
    }

    /**
     * Submit a new review - Alternative /submit endpoint (same functionality as primary)
     */
    @PostMapping("/submit")
    public ResponseEntity<?> submitReviewSubmit(
            @RequestParam(required = false) String movieId,
            @RequestParam(required = false) String reviewText,
            @RequestBody(required = false) Map<String, String> requestBody,
            HttpServletRequest request) {
        
        // Check if backend is healthy
        if (!adminService.isBackendHealthy()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Backend service is unhealthy"));
        }

        try {
            // Try to get parameters from request body first, then fall back to query params
            String finalMovieId = movieId;
            String finalReviewText = reviewText;
            
            if (requestBody != null && !requestBody.isEmpty()) {
                finalMovieId = requestBody.getOrDefault("movieId", movieId);
                finalReviewText = requestBody.getOrDefault("reviewText", reviewText);
            }
            
            // If still null, try to read from request stream manually
            if ((finalMovieId == null || finalReviewText == null) && request.getContentLength() > 0) {
                try {
                    StringBuilder sb = new StringBuilder();
                    BufferedReader reader = request.getReader();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        sb.append(line);
                    }
                    String body = sb.toString();
                    
                    // Simple JSON parsing for movieId and reviewText
                    if (body.contains("movieId") && body.contains("reviewText")) {
                        // Extract movieId
                        int movieIdStart = body.indexOf("\"movieId\"") + 11;
                        int movieIdEnd = body.indexOf("\"", movieIdStart);
                        if (movieIdEnd > movieIdStart) {
                            finalMovieId = body.substring(movieIdStart, movieIdEnd);
                        }
                        
                        // Extract reviewText
                        int reviewStart = body.indexOf("\"reviewText\"") + 14;
                        int reviewEnd = body.lastIndexOf("\"");
                        if (reviewEnd > reviewStart) {
                            finalReviewText = body.substring(reviewStart, reviewEnd);
                        }
                    }
                } catch (Exception e) {
                    System.err.println("❌ Failed to manually parse request body: " + e.getMessage());
                }
            }

            System.out.println("📝 POST /api/reviews/submit - Movie: " + finalMovieId);

            // Validate input
            if (finalMovieId == null || finalMovieId.trim().isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(Map.of("error", "Movie ID is required"));
            }
            if (finalReviewText == null || finalReviewText.trim().isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(Map.of("error", "Review text is required"));
            }

            ReviewSubmissionResult result = reviewService.submitReview(finalMovieId, finalReviewText);

            if (result.isSuccess()) {
                return ResponseEntity.ok(Map.of(
                    "review", result.getReview(),
                    "message", result.getMessage()
                ));
            } else {
                // Review was analyzed but not saved (database issue)
                return ResponseEntity.status(HttpStatus.PARTIAL_CONTENT)
                        .body(Map.of(
                            "review", result.getReview(),
                            "message", result.getMessage(),
                            "warning", "Review analysis completed but storage failed"
                        ));
            }

        } catch (ReviewSubmissionException e) {
            // Model server is down - reject the review
            System.err.println("❌ Review submission failed: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", e.getMessage()));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            System.err.println("❌ Unexpected error during review submission: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Internal server error"));
        }
    }

    /**
     * Submit a new review - GET endpoint (most reliable through proxies)
     */
    @GetMapping("/submit-get")
    public ResponseEntity<?> submitReviewGet(
            @RequestParam String movieId,
            @RequestParam String reviewText) {
        
        // Check if backend is healthy
        if (!adminService.isBackendHealthy()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Backend service is unhealthy"));
        }

        try {
            System.out.println("📝 GET /api/reviews/submit-get - Movie: " + movieId + ", Text: " + reviewText);

            // Validate input
            if (movieId == null || movieId.trim().isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(Map.of("error", "Movie ID is required"));
            }
            if (reviewText == null || reviewText.trim().isEmpty()) {
                return ResponseEntity.badRequest()
                        .body(Map.of("error", "Review text is required"));
            }

            ReviewSubmissionResult result = reviewService.submitReview(movieId, reviewText);

            if (result.isSuccess()) {
                return ResponseEntity.ok(Map.of(
                    "review", result.getReview(),
                    "message", result.getMessage()
                ));
            } else {
                // Review was analyzed but not saved (database issue)
                return ResponseEntity.status(HttpStatus.PARTIAL_CONTENT)
                        .body(Map.of(
                            "review", result.getReview(),
                            "message", result.getMessage(),
                            "warning", "Review analysis completed but storage failed"
                        ));
            }

        } catch (ReviewSubmissionException e) {
            // Model server is down - reject the review
            System.err.println("❌ Review submission failed: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", e.getMessage()));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            System.err.println("❌ Unexpected error during review submission: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Internal server error"));
        }
    }

    /**
     * Get review statistics
     */
    @GetMapping("/stats")
    public ResponseEntity<?> getReviewStats() {
        if (!adminService.isBackendHealthy()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Backend service is unhealthy"));
        }

        try {
            Map<String, Object> stats = reviewService.getReviewStats();
            return ResponseEntity.ok(stats);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to get review statistics"));
        }
    }

    /**
     * Get latest reviews across all movies for homepage
     */
    @GetMapping("/latest")
    public ResponseEntity<?> getLatestReviews() {
        // Check if backend is healthy
        if (!adminService.isBackendHealthy()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Backend service is unhealthy"));
        }

        try {
            System.out.println("📋 GET /api/reviews/latest");
            List<Review> latestReviews = reviewService.getLatestReviews(5);
            return ResponseEntity.ok(latestReviews);
        } catch (DatabaseException e) {
            System.err.println("❌ Database error: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            System.err.println("❌ Unexpected error: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Internal server error"));
        }
    }
} 
package com.moviereview.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.Map;

@Service
public class ModelServerService {

    @Autowired
    private WebClient webClient;

    @Value("${model.server.timeout:1000}")
    private int timeoutMs;

    private boolean modelServerConnected = true; // For admin simulation

    /**
     * Analyze sentiment of review text
     */
    public SentimentResult analyzeSentiment(String reviewText) {
        if (!modelServerConnected) {
            throw new ModelServerException("Model server connection is disabled (admin simulation)");
        }

        try {
            System.out.println("🤖 Calling model server for sentiment analysis: " + reviewText.substring(0, Math.min(50, reviewText.length())) + "...");
            
            Map<String, Object> response = webClient.post()
                    .uri("/analyze")
                    .bodyValue(Map.of("text", reviewText))
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofMillis(timeoutMs))
                    .block();

            if (response != null && response.containsKey("sentiment")) {
                String sentiment = (String) response.get("sentiment");
                Double score = response.get("score") != null ? 
                    Double.valueOf(response.get("score").toString()) : 0.0;
                Double rating = response.get("rating") != null ? 
                    Double.valueOf(response.get("rating").toString()) : 3.0;
                
                System.out.println("✅ Model server response: " + sentiment + " (score: " + score + ", rating: " + rating + " stars)");
                return new SentimentResult(sentiment, score, rating);
            } else {
                System.err.println("❌ Invalid response from model server");
                throw new ModelServerException("Invalid response from model server");
            }
            
        } catch (Exception e) {
            System.err.println("❌ Failed to connect to model server: " + e.getMessage());
            throw new ModelServerException("Model server is down - analysis cannot be done at this moment");
        }
    }

    /**
     * Check if model server is available
     */
    public boolean isModelServerAvailable() {
        if (!modelServerConnected) {
            return false;
        }

        try {
            System.out.println("🔍 Checking model server health...");
            
            Map<String, Object> response = webClient.get()
                    .uri("/health")
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofMillis(3000))
                    .block();

            boolean available = response != null && "healthy".equals(response.get("status"));
            System.out.println(available ? "✅ Model server is healthy" : "❌ Model server is unhealthy");
            return available;
            
        } catch (Exception e) {
            System.err.println("❌ Model server health check failed: " + e.getMessage());
            return false;
        }
    }

    /**
     * Admin function to toggle model server connection simulation
     */
    public void toggleModelConnection() {
        modelServerConnected = !modelServerConnected;
        System.out.println("🔧 Model server connection toggled: " + (modelServerConnected ? "ENABLED" : "DISABLED"));
    }

    /**
     * Get current model server connection status
     */
    public boolean isModelConnectionEnabled() {
        return modelServerConnected;
    }

    /**
     * Sentiment analysis result with rating
     */
    public static class SentimentResult {
        private final String sentiment;
        private final Double score;
        private final Double rating;

        public SentimentResult(String sentiment, Double score, Double rating) {
            this.sentiment = sentiment;
            this.score = score;
            this.rating = rating;
        }

        public String getSentiment() {
            return sentiment;
        }

        public Double getScore() {
            return score;
        }

        public Double getRating() {
            return rating;
        }
    }

    /**
     * Custom exception for model server issues
     */
    public static class ModelServerException extends RuntimeException {
        public ModelServerException(String message) {
            super(message);
        }
    }
} 
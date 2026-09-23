package com.moviereview;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.web.reactive.function.client.WebClient;

@SpringBootApplication
public class MovieReviewApplication {

    @Value("${model.server.url}")
    private String modelServerUrl;

    public static void main(String[] args) {
        System.out.println("🚀 Starting Movie Review Backend Service");
        System.out.println("📋 This service is designed to be resilient to downstream failures");
        System.out.println("🗄️ Database connection will be tested at runtime, not startup");
        System.out.println("🤖 Model server connection will be tested per request");
        
        SpringApplication.run(MovieReviewApplication.class, args);
    }

    @Bean
    public WebClient webClient() {
        return WebClient.builder()
                .baseUrl(modelServerUrl)
                .build();
    }
} 
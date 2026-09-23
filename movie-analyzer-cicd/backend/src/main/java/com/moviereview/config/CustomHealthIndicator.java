package com.moviereview.config;

import com.moviereview.service.AdminService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

/**
 * Custom Health Indicator that integrates with AdminService
 * This makes the Spring Boot Actuator /actuator/health endpoint respect the admin health toggle
 */
@Component
public class CustomHealthIndicator implements HealthIndicator {

    @Autowired
    private AdminService adminService;

    @Override
    public Health health() {
        // Check if admin has marked the backend as unhealthy
        if (!adminService.isBackendHealthy()) {
            return Health.down()
                    .withDetail("reason", "Backend marked as unhealthy via admin toggle")
                    .withDetail("service", "backend")
                    .withDetail("admin_status", "unhealthy")
                    .build();
        }

        // If admin health is OK, return UP
        return Health.up()
                .withDetail("service", "backend")
                .withDetail("admin_status", "healthy")
                .withDetail("message", "Backend is healthy")
                .build();
    }
} 
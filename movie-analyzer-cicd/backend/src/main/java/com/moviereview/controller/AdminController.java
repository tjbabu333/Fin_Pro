package com.moviereview.controller;

import com.moviereview.service.AdminService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    @Autowired
    private AdminService adminService;

    /**
     * Health check endpoint - called by frontend every 10 seconds
     */
    @GetMapping("/health")
    public ResponseEntity<?> getHealth() {
        Map<String, Object> healthStatus = adminService.getHealthStatus();
        
        // Return 503 if backend is marked as unhealthy
        if ("unhealthy".equals(healthStatus.get("status"))) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(healthStatus);
        }
        
        System.out.println("🏥 Health check: " + healthStatus.get("status"));
        return ResponseEntity.ok(healthStatus);
    }

    /**
     * Toggle backend health status - ALWAYS respond to allow re-enabling from frontend
     */
    @PostMapping("/toggle-health")
    public ResponseEntity<?> toggleBackendHealth() {
        try {
            Map<String, Object> result = adminService.toggleBackendHealth();
            // Always return 200 OK even if currently unhealthy, so frontend can toggle back
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to toggle backend health"));
        }
    }

    /**
     * Toggle backend overload simulation - now fully functional
     */
    @PostMapping("/toggle-overload")
    public ResponseEntity<?> toggleOverload() {
        try {
            Map<String, Object> result = adminService.toggleBackendOverload();
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to toggle backend overload"));
        }
    }

    /**
     * Toggle database connection simulation
     */
    @PostMapping("/toggle-database")
    public ResponseEntity<?> toggleDatabaseConnection() {
        try {
            Map<String, Object> result = adminService.toggleDatabaseConnection();
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to toggle database connection"));
        }
    }

    /**
     * Toggle model server connection simulation
     */
    @PostMapping("/toggle-model")
    public ResponseEntity<?> toggleModelServerConnection() {
        try {
            Map<String, Object> result = adminService.toggleModelServerConnection();
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to toggle model server connection"));
        }
    }

    /**
     * Get comprehensive admin status
     */
    @GetMapping("/status")
    public ResponseEntity<?> getAdminStatus() {
        try {
            Map<String, Object> status = adminService.getAdminStatus();
            return ResponseEntity.ok(status);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to get admin status"));
        }
    }

    /**
     * System information endpoint
     */
    @GetMapping("/info")
    public ResponseEntity<?> getSystemInfo() {
        try {
            Runtime runtime = Runtime.getRuntime();
            return ResponseEntity.ok(Map.of(
                "service", "backend",
                "version", "1.0.0",
                "timestamp", java.time.Instant.now().toString(),
                "uptime", System.currentTimeMillis(),
                "memory", Map.of(
                    "total", runtime.totalMemory(),
                    "free", runtime.freeMemory(),
                    "used", runtime.totalMemory() - runtime.freeMemory(),
                    "max", runtime.maxMemory()
                ),
                "processors", runtime.availableProcessors(),
                "overloaded", adminService.isBackendOverloaded()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to get system info"));
        }
    }
} 
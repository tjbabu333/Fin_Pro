const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const helmet = require('helmet');
const cors = require('cors');
const hpp = require('hpp');
const xss = require('xss-clean');

const app = express();
const PORT = process.env.PORT || 3000;

// Backend URL for proxying API requests - using BACKEND_API_URL as specified
const BACKEND_URL = process.env.BACKEND_API_URL || 'http://localhost:8080';

// Security middleware
app.use(helmet()); // Set security HTTP headers
app.use(cors()); // Enable CORS
app.use(xss()); // Sanitize data
app.use(hpp()); // Prevent HTTP Parameter Pollution

// Add JSON parsing middleware with size limit
app.use(express.json({ limit: '10kb' })); // Body limit is 10kb

console.log('🚀 Starting Movie Review Frontend Server');
console.log(`📡 Backend URL: ${BACKEND_URL}`);
console.log(`🌐 Frontend Port: ${PORT}`);

// Server state for simulation
let serverHealthy = true;
let serverOverloaded = false;
let overloadInterval = null;

// Health check endpoint for Kubernetes
app.get('/health', (req, res) => {
  if (!serverHealthy) {
    res.status(503).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      service: 'frontend'
    });
    return;
  }

  res.status(200).json({
    status: serverOverloaded ? 'degraded' : 'healthy',
    timestamp: new Date().toISOString(),
    service: 'frontend',
    overloaded: serverOverloaded
  });
});

// Frontend admin endpoints for crash/overload simulation
app.post('/admin/crash', (req, res) => {
  console.log('💥 CRASH ENDPOINT CALLED - Container will terminate in 3 seconds');
  res.json({ 
    message: 'Frontend container crash initiated', 
    countdown: 3,
    timestamp: new Date().toISOString()
  });
  
  let countdown = 3;
  const crashInterval = setInterval(() => {
    countdown--;
    console.log(`💥 Container crashing in ${countdown} second${countdown !== 1 ? 's' : ''}...`);
    
    if (countdown <= 0) {
      clearInterval(crashInterval);
      console.log('💥 FRONTEND CONTAINER CRASH - Forcing exit');
      
      // Multiple crash methods to ensure it works
      setTimeout(() => process.exit(1), 100);  // Exit with error code
      setTimeout(() => { throw new Error('Forced container crash'); }, 200);
      setTimeout(() => process.kill(process.pid, 'SIGKILL'), 300);
    }
  }, 1000);
});

app.post('/admin/toggle-health', (req, res) => {
  serverHealthy = !serverHealthy;
  console.log(`🏥 Frontend health toggled: ${serverHealthy ? 'HEALTHY' : 'UNHEALTHY'}`);
  res.json({ 
    message: `Frontend health ${serverHealthy ? 'enabled' : 'disabled'}`,
    healthy: serverHealthy,
    timestamp: new Date().toISOString()
  });
});

app.post('/admin/start-overload', (req, res) => {
  if (overloadInterval) {
    res.json({ message: 'Overload already running', overloaded: true });
    return;
  }

  serverOverloaded = true;
  console.log('🔥 STARTING FRONTEND SERVER OVERLOAD');
  
  // CPU overload - intensive operations that will max out the container
  overloadInterval = setInterval(() => {
    // CPU intensive operations
    const start = Date.now();
    while (Date.now() - start < 500) { // 500ms of pure CPU work
      Math.random() * Math.random() * Math.sin(Date.now()) * Math.cos(Date.now());
      Math.sqrt(Math.random() * 1000000);
      JSON.stringify(new Array(1000).fill(Math.random()));
    }
    
    // Memory allocation
    const wasteMemory = [];
    for (let i = 0; i < 100000; i++) {
      wasteMemory.push(new Array(100).fill(Math.random()));
    }
    
    // Keep references longer to pressure GC
    setTimeout(() => wasteMemory.length = 0, 200);
    
    console.log('🔥 CPU/Memory overload cycle completed');
  }, 100); // Every 100ms

  res.json({ 
    message: 'Frontend server overload started - High CPU/Memory usage',
    overloaded: true,
    timestamp: new Date().toISOString()
  });
});

app.post('/admin/stop-overload', (req, res) => {
  if (overloadInterval) {
    clearInterval(overloadInterval);
    overloadInterval = null;
    serverOverloaded = false;
    console.log('✅ Frontend server overload stopped');
    
    res.json({ 
      message: 'Frontend server overload stopped',
      overloaded: false,
      timestamp: new Date().toISOString()
    });
  } else {
    res.json({ message: 'No overload running', overloaded: false });
  }
});

// Get current server status
app.get('/admin/status', (req, res) => {
  res.json({
    healthy: serverHealthy,
    overloaded: serverOverloaded,
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    cpu: process.cpuUsage()
  });
});

// Proxy all /api requests to the backend
app.use('/api', createProxyMiddleware({
  target: BACKEND_URL,
  changeOrigin: true,
  timeout: 30000, // 30 second timeout for proxy requests
  proxyTimeout: 30000, // 30 second proxy timeout
  secure: true, // Enable HTTPS
  ws: false,
  buffer: false, // Don't buffer request/response
  onError: (err, req, res) => {
    console.error('❌ Proxy Error:', err.message);
    if (!res.headersSent) {
      res.status(500).json({
        error: 'Backend service unavailable',
        message: 'Cannot connect to backend server'
      });
    }
  },
  onProxyReq: (proxyReq, req, res) => {
    // Add security headers to proxy requests
    proxyReq.setHeader('X-Forwarded-Proto', 'https');
    proxyReq.setHeader('X-Real-IP', req.ip);
    console.log(`🔄 Proxying: ${req.method} ${req.path} -> ${BACKEND_URL}${req.path}`);
  },
  onProxyRes: (proxyRes, req, res) => {
    // Add security headers to proxy responses
    proxyRes.headers['X-Content-Type-Options'] = 'nosniff';
    proxyRes.headers['X-Frame-Options'] = 'DENY';
    proxyRes.headers['X-XSS-Protection'] = '1; mode=block';
    console.log(`✅ Proxy Response: ${proxyRes.statusCode} ${req.method} ${req.path}`);
  }
}));

// Serve static files from React build
app.use(express.static(path.join(__dirname, 'build')));

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// Start the server
app.listen(PORT, () => {
  console.log(`✅ Frontend server running on port ${PORT}`);
  console.log(`🎬 Movie Review App is ready!`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 Received SIGTERM, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 Received SIGINT, shutting down gracefully');
  process.exit(0);
}); 
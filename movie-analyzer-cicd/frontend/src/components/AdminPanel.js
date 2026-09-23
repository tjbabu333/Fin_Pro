import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AdminPanel({
  serviceStatus,
  frontendHealthy,
  frontendOverloaded,
  onToggleFrontendHealth,
  onStartFrontendOverload,
  onStopFrontendOverload,
  onCrashFrontend,
  onNotification,
  onRefreshStatus
}) {
  const [backendOverloaded, setBackendOverloaded] = useState(false);

  // Track backend overload state from service status
  useEffect(() => {
    if (serviceStatus.backendOverloaded !== undefined) {
      setBackendOverloaded(serviceStatus.backendOverloaded);
    }
  }, [serviceStatus]);

  const callBackendAdmin = async (endpoint, action, forceCall = false) => {
    try {
      // For health toggle, always try the call even if backend seems down
      if (forceCall || serviceStatus.backend) {
        const response = await axios.post(`/api/admin/${endpoint}`, {}, { timeout: 5000 });
        onNotification(`${action} successful`, 'success');
        setTimeout(onRefreshStatus, 1000);
        return response.data;
      } else {
        onNotification('Backend service unavailable', 'error');
        return null;
      }
    } catch (err) {
      console.error(`Failed to ${action}:`, err);
      
      // For health toggle, this might succeed even if other calls fail
      if (endpoint === 'toggle-health' && err.response?.status !== 404) {
        onNotification(`${action} - ${err.response?.data?.message || 'Backend may be unhealthy but toggle attempted'}`, 'warning');
        setTimeout(onRefreshStatus, 1000);
      } else {
        onNotification(`Failed to ${action} - ${err.response?.data?.message || 'Backend unavailable'}`, 'error');
      }
    }
  };

  const handleToggleFrontendHealth = () => {
    const newState = !frontendHealthy;
    onToggleFrontendHealth(newState);
    onNotification(
      `Frontend health ${newState ? 'enabled' : 'disabled'}`, 
      newState ? 'success' : 'warning'
    );
  };

  const handleToggleBackendHealth = () => {
    // Always try to toggle health, even if backend appears down
    callBackendAdmin('toggle-health', 'Toggle backend health', true);
  };

  const handleToggleBackendOverload = async () => {
    try {
      const response = await axios.post('/api/admin/toggle-overload', {}, { timeout: 5000 });
      const isNowOverloaded = response.data.overloaded;
      setBackendOverloaded(isNowOverloaded);
      onNotification(
        `Backend overload ${isNowOverloaded ? 'started' : 'stopped'}`, 
        isNowOverloaded ? 'warning' : 'success'
      );
      setTimeout(onRefreshStatus, 1000);
    } catch (err) {
      console.error('Failed to toggle backend overload:', err);
      onNotification(`Failed to toggle backend overload - ${err.response?.data?.message || 'Backend unavailable'}`, 'error');
    }
  };

  const handleToggleDatabaseConnection = () => {
    callBackendAdmin('toggle-database', 'Toggle database connection');
  };

  const handleToggleModelConnection = () => {
    callBackendAdmin('toggle-model', 'Toggle model server connection');
  };

  const handleRefreshStatus = () => {
    onRefreshStatus();
    onNotification('Status refreshed', 'info');
  };

  return (
    <div className="admin-panel">
      <div className="admin-section">
        <h3>🌐 Frontend Controls</h3>
        <p style={{ fontSize: '0.9rem', color: '#6b7280', marginBottom: '1rem' }}>
          Control frontend service health and performance simulation
        </p>
        
        <div className="toggle-group">
          <button
            className={`button ${frontendHealthy ? 'button-success' : 'button-danger'}`}
            onClick={handleToggleFrontendHealth}
          >
            {frontendHealthy ? '✅ Frontend Healthy' : '❌ Frontend Unhealthy'}
          </button>

          {frontendOverloaded ? (
            <button
              className="button button-success"
              onClick={onStopFrontendOverload}
            >
              🛑 Stop Frontend Overload
            </button>
          ) : (
            <button
              className="button button-warning"
              onClick={onStartFrontendOverload}
            >
              ⚡ Start Frontend Overload
            </button>
          )}

          <button
            className="button button-danger"
            onClick={onCrashFrontend}
          >
            💥 Crash Frontend App
          </button>
        </div>
      </div>

      <div className="admin-section">
        <h3>🔧 Backend Controls</h3>
        <p style={{ fontSize: '0.9rem', color: '#6b7280', marginBottom: '1rem' }}>
          Control backend service health, overload simulation, and connection states
        </p>
        
        <div className="toggle-group">
          <button
            className={`button ${serviceStatus.backend ? 'button-success' : 'button-danger'}`}
            onClick={handleToggleBackendHealth}
          >
            {serviceStatus.backend ? '✅ Backend Healthy' : '❌ Backend Unhealthy'}
          </button>

          {backendOverloaded ? (
            <button
              className="button button-success"
              onClick={handleToggleBackendOverload}
              disabled={!serviceStatus.backend}
            >
              🛑 Stop Backend Overload
            </button>
          ) : (
            <button
              className="button button-warning"
              onClick={handleToggleBackendOverload}
              disabled={!serviceStatus.backend}
            >
              ⚡ Start Backend Overload
            </button>
          )}

          <button
            className={`button ${serviceStatus.database ? 'button-success' : 'button-danger'}`}
            onClick={handleToggleDatabaseConnection}
            disabled={!serviceStatus.backend}
          >
            {serviceStatus.database ? '🗄️ DB Connected' : '🗄️ DB Disconnected'}
          </button>

          <button
            className={`button ${serviceStatus.model ? 'button-success' : 'button-danger'}`}
            onClick={handleToggleModelConnection}
            disabled={!serviceStatus.backend}
          >
            {serviceStatus.model ? '🤖 Model Connected' : '🤖 Model Disconnected'}
          </button>
        </div>

        {!serviceStatus.backend && (
          <div style={{ 
            marginTop: '1rem', 
            padding: '0.5rem', 
            background: '#fef3c7', 
            border: '1px solid #f59e0b',
            borderRadius: '6px',
            fontSize: '0.9rem',
            color: '#92400e'
          }}>
            ⚠️ Most backend controls are disabled because backend service is unavailable
            <br />
            <small>Health toggle may still work to re-enable the service</small>
          </div>
        )}
      </div>

      <div className="admin-section">
        <h3>🔄 Actions</h3>
        <p style={{ fontSize: '0.9rem', color: '#6b7280', marginBottom: '1rem' }}>
          Manual refresh and system actions
        </p>
        
        <div className="toggle-group">
          <button
            className="button"
            onClick={handleRefreshStatus}
          >
            🔄 Refresh Status
          </button>
        </div>
      </div>

      <div className="admin-section">
        <h3>📖 Demo Instructions</h3>
        <div style={{ fontSize: '0.9rem', color: '#6b7280', lineHeight: '1.6' }}>
          <p><strong>Frontend Controls:</strong></p>
          <ul style={{ marginLeft: '1rem', marginBottom: '1rem' }}>
            <li>Toggle health to simulate service up/down</li>
            <li>Start overload to simulate high CPU/memory usage</li>
            <li>Crash app to trigger container restart</li>
          </ul>
          
          <p><strong>Backend Controls:</strong></p>
          <ul style={{ marginLeft: '1rem', marginBottom: '1rem' }}>
            <li>Toggle backend health for service availability</li>
            <li><strong>NEW:</strong> Toggle backend overload for CPU/memory stress</li>
            <li>Toggle DB connection to simulate database issues</li>
            <li>Toggle model connection to simulate ML service issues</li>
          </ul>
          
          <p><strong>Educational Purpose:</strong> This demonstrates microservice failures, 
          health checks, overload handling, and graceful degradation in Kubernetes environments.</p>
          
          <p><strong>Status Monitoring:</strong> Check the bottom status bar for real-time 
          system health across all pages.</p>
        </div>
      </div>
    </div>
  );
}

export default AdminPanel; 
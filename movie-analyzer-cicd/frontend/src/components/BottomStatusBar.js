import React from 'react';

/**
 * BottomStatusBar Component
 * Fixed bottom bar showing real-time status of all services
 * Visible across all pages with system health summary
 */
function BottomStatusBar({ serviceStatus, frontendOverloaded }) {
  // Get system health data
  const getSystemHealth = () => {
    const servicesOnline = [
      serviceStatus.backend,
      serviceStatus.database,
      serviceStatus.model
    ].filter(Boolean).length;
    
    const hasOverload = frontendOverloaded || serviceStatus.backendOverloaded;
    
    if (servicesOnline === 3 && !hasOverload) {
      return {
        status: 'all-good',
        message: '✅ All Systems Operational',
        icon: '✅'
      };
    } else if (servicesOnline === 3 && hasOverload) {
      return {
        status: 'partial',
        message: '⚡ Systems Online but Overloaded',
        icon: '⚡'
      };
    } else if (servicesOnline >= 2) {
      return {
        status: 'partial',
        message: '⚠️ Partial Service Degradation',
        icon: '⚠️'
      };
    } else if (servicesOnline === 1) {
      return {
        status: 'critical',
        message: '🔴 Major Service Outage',
        icon: '🔴'
      };
    } else {
      return {
        status: 'critical',
        message: '💥 Critical System Failure',
        icon: '💥'
      };
    }
  };

  const systemHealth = getSystemHealth();

  return (
    <div className="status-bottom-bar">
      <div className="status-bottom-content">
        {/* Individual Service Status */}
        <div className="status-services">
          <div className="status-service-item">
            <div className="status-dot" style={{ 
              backgroundColor: '#16a34a'
            }}></div>
            <span style={{ color: '#16a34a' }}>
              Frontend
              {frontendOverloaded && <span style={{ color: '#f59e0b' }}> (Overloaded)</span>}
            </span>
          </div>

          <div className="status-service-item">
            <div className="status-dot" style={{ 
              backgroundColor: serviceStatus.backend ? '#16a34a' : '#dc2626'
            }}></div>
            <span style={{ color: serviceStatus.backend ? '#16a34a' : '#dc2626' }}>
              Backend
              {serviceStatus.backendOverloaded && <span style={{ color: '#f59e0b' }}> (Overloaded)</span>}
            </span>
          </div>

          <div className="status-service-item">
            <div className="status-dot" style={{ 
              backgroundColor: serviceStatus.database ? '#16a34a' : '#dc2626'
            }}></div>
            <span style={{ color: serviceStatus.database ? '#16a34a' : '#dc2626' }}>
              Database
            </span>
          </div>

          <div className="status-service-item">
            <div className="status-dot" style={{ 
              backgroundColor: serviceStatus.model ? '#16a34a' : '#dc2626'
            }}></div>
            <span style={{ color: serviceStatus.model ? '#16a34a' : '#dc2626' }}>
              Model
            </span>
          </div>
        </div>

        {/* System Health Summary */}
        <div className={`status-health-summary status-health-${systemHealth.status}`}>
          <span>{systemHealth.message}</span>
        </div>
      </div>
    </div>
  );
}

export default BottomStatusBar; 
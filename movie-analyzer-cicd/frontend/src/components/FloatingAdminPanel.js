import React, { useState } from 'react';
import AdminPanel from './AdminPanel';

/**
 * FloatingAdminPanel Component
 * Floating button at bottom right that expands to show admin controls
 * As requested by user for better UX
 */
function FloatingAdminPanel({
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
  const [isOpen, setIsOpen] = useState(false);

  const togglePanel = () => {
    setIsOpen(!isOpen);
  };

  const handleClosePanel = () => {
    setIsOpen(false);
  };

  // Close panel when clicking outside
  const handlePanelClick = (e) => {
    e.stopPropagation();
  };

  // Close on escape key
  React.useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen]);

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.1)',
            zIndex: 999
          }}
          onClick={handleClosePanel}
        />
      )}

      {/* Floating Admin Panel */}
      <div className="floating-admin">
        {/* Admin Panel (when expanded) */}
        {isOpen && (
          <div className="admin-panel-floating" onClick={handlePanelClick}>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              padding: '1rem 1.5rem',
              borderBottom: '1px solid #e5e7eb'
            }}>
              <h2 style={{ margin: 0, color: '#1f2937' }}>
                ⚙️ Admin Controls
              </h2>
              <button
                onClick={handleClosePanel}
                style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '1.5rem',
                  cursor: 'pointer',
                  color: '#6b7280',
                  padding: '0.25rem'
                }}
              >
                ✕
              </button>
            </div>
            
            <AdminPanel
              serviceStatus={serviceStatus}
              frontendHealthy={frontendHealthy}
              frontendOverloaded={frontendOverloaded}
              onToggleFrontendHealth={onToggleFrontendHealth}
              onStartFrontendOverload={onStartFrontendOverload}
              onStopFrontendOverload={onStopFrontendOverload}
              onCrashFrontend={onCrashFrontend}
              onNotification={onNotification}
              onRefreshStatus={onRefreshStatus}
            />
          </div>
        )}

        {/* Toggle Button */}
        <button 
          className="admin-toggle-button"
          onClick={togglePanel}
          title={isOpen ? 'Close Admin Panel' : 'Open Admin Panel'}
        >
          {isOpen ? '✕' : '⚙️'}
        </button>
      </div>
    </>
  );
}

export default FloatingAdminPanel; 
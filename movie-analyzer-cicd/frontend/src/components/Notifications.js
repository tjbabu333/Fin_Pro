import React from 'react';

/**
 * Notifications Component
 * Displays notifications for toggle actions, submission errors/success, and system events
 * Notifications briefly appear as specified in rules
 */
function Notifications({ notifications }) {
  if (!notifications || notifications.length === 0) {
    return null;
  }

  return (
    <div>
      {notifications.map(notification => (
        <div
          key={notification.id}
          className={`notification notification-${notification.type}`}
        >
          {notification.message}
        </div>
      ))}
    </div>
  );
}

export default Notifications; 
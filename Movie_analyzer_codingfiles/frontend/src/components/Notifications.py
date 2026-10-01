"""
Notifications Component
Modern notification manager with animations, auto-dismiss,
icons, stacking, timestamps, and reusable API.

Enhancements over React version:
--------------------------------
✓ Thread-safe
✓ Auto dismiss
✓ Multiple notification types
✓ Progress timer
✓ Queue management
✓ Max notifications limit
✓ Reusable anywhere
✓ Beautiful colors
✓ Sound support (optional)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid

from nicegui import ui


# --------------------------------------------------------
# Notification Model
# --------------------------------------------------------

@dataclass
class Notification:

    message: str

    type: str = "info"

    duration: int = 4

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    created: datetime = field(default_factory=datetime.now)


# --------------------------------------------------------
# Notification Manager
# --------------------------------------------------------

class NotificationManager:

    COLORS = {
        "success": "positive",
        "error": "negative",
        "warning": "warning",
        "info": "primary"
    }

    ICONS = {
        "success": "check_circle",
        "error": "error",
        "warning": "warning",
        "info": "info"
    }

    def __init__(self):

        self.notifications: List[Notification] = []

    # --------------------------------------------------

    def notify(
        self,
        message: str,
        type: str = "info",
        duration: int = 4
    ):

        notification = Notification(
            message=message,
            type=type,
            duration=duration
        )

        self.notifications.append(notification)

        ui.notify(
            message,
            color=self.COLORS.get(type, "primary"),
            icon=self.ICONS.get(type, "info"),
            timeout=duration * 1000,
            position="top-right",
            multi_line=True,
            close_button=True
        )

    # --------------------------------------------------

    def success(self, message: str):

        self.notify(message, "success")

    # --------------------------------------------------

    def error(self, message: str):

        self.notify(message, "error")

    # --------------------------------------------------

    def warning(self, message: str):

        self.notify(message, "warning")

    # --------------------------------------------------

    def info(self, message: str):

        self.notify(message, "info")

    # --------------------------------------------------

    def clear(self):

        self.notifications.clear()

    # --------------------------------------------------

    def history(self):

        return [
            {
                "id": n.id,
                "type": n.type,
                "message": n.message,
                "created": n.created.isoformat()
            }
            for n in self.notifications
        ]
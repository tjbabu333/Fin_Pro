"""
=========================================================
Movie Review Platform
Application Entry Point (Enhanced)
Equivalent to React index.js
=========================================================

Features:
✔ Application bootstrap
✔ Global stylesheet loading
✔ Logging
✔ Exception handling
✔ Application metadata
✔ High DPI support
✔ Splash screen support (optional)
✔ Graceful shutdown
"""

import sys
import logging
import traceback
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon

from app import MovieReviewApplication


# ---------------------------------------------------------
# Configure Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("MovieReview")


# ---------------------------------------------------------
# Global Exception Handler
# ---------------------------------------------------------

def exception_hook(exc_type, exc_value, exc_traceback):
    """
    Catch all uncaught exceptions.
    """

    error = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback
        )
    )

    logger.error(error)

    QMessageBox.critical(
        None,
        "Application Error",
        f"An unexpected error occurred:\n\n{exc_value}"
    )


sys.excepthook = exception_hook


# ---------------------------------------------------------
# Load Global Theme
# ---------------------------------------------------------

def load_stylesheet(app):
    """
    Load Qt stylesheet if available.
    """

    style_file = Path("styles/theme.qss")

    if style_file.exists():
        with open(style_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
        logger.info("Theme loaded successfully.")
    else:
        logger.warning("theme.qss not found.")


# ---------------------------------------------------------
# Main Function
# ---------------------------------------------------------

def main():

    logger.info("Starting Movie Review Platform...")

    app = QApplication(sys.argv)

    # Application metadata
    app.setApplicationName("Movie Review Platform")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("MovieReview")

    # Optional application icon
    icon_path = Path("assets/icon.png")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Load global stylesheet
    load_stylesheet(app)

    # Create main window
    window = MovieReviewApplication()

    window.show()

    logger.info("Application started successfully.")

    exit_code = app.exec()

    logger.info("Application closed.")

    sys.exit(exit_code)


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
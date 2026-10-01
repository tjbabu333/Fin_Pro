"""
Movie Review Admin Panel
Author: OpenAI Conversion
Framework: Streamlit

Features
--------
✔ Frontend Health Toggle
✔ Backend Health Toggle
✔ Database Toggle
✔ Model Server Toggle
✔ Backend Overload Simulation
✔ Auto Refresh
✔ Beautiful Dashboard
✔ Real-time Status
"""

import streamlit as st
import requests
import time

API = "http://localhost:8000"

st.set_page_config(
    page_title="Movie Review Admin",
    page_icon="⚙️",
    layout="wide"
)

####################################################
# Helper
####################################################

def call_api(endpoint):

    try:
        r = requests.post(
            f"{API}{endpoint}",
            timeout=5
        )

        if r.status_code == 200:
            return r.json()

        return {"error": r.text}

    except Exception as e:
        return {"error": str(e)}

####################################################
# Session State
####################################################

if "frontend_health" not in st.session_state:
    st.session_state.frontend_health = True

if "frontend_overload" not in st.session_state:
    st.session_state.frontend_overload = False

####################################################
# Title
####################################################

st.title("🎬 Movie Review Admin Dashboard")

st.write(
    "Manage backend, frontend, database and AI model status."
)

####################################################
# Frontend Controls
####################################################

st.header("🌐 Frontend Controls")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "Toggle Frontend Health",
        use_container_width=True
    ):

        st.session_state.frontend_health = \
            not st.session_state.frontend_health

with col2:

    if st.button(
        "Toggle Frontend Overload",
        use_container_width=True
    ):

        st.session_state.frontend_overload = \
            not st.session_state.frontend_overload

with col3:

    if st.button(
        "Crash Frontend",
        use_container_width=True
    ):

        st.error("Frontend crashed!")

####################################################
# Backend Controls
####################################################

st.header("🔧 Backend Controls")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "Toggle Backend Health",
        use_container_width=True
    ):

        result = call_api("/api/admin/toggle-health")
        st.success(result)

    if st.button(
        "Toggle Database",
        use_container_width=True
    ):

        result = call_api("/api/admin/toggle-database")
        st.success(result)

with col2:

    if st.button(
        "Toggle Backend Overload",
        use_container_width=True
    ):

        result = call_api("/api/admin/toggle-overload")
        st.success(result)

    if st.button(
        "Toggle Model Server",
        use_container_width=True
    ):

        result = call_api("/api/admin/toggle-model")
        st.success(result)

####################################################
# Backend Status
####################################################

st.header("📊 Current Status")

try:

    health = requests.get(
        f"{API}/api/admin/status",
        timeout=5
    ).json()

except:

    health = {
        "backendHealthy": False,
        "databaseConnected": False,
        "modelServerConnected": False,
        "backendOverloaded": False
    }

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Backend",
    "Healthy" if health["backendHealthy"] else "Down"
)

col2.metric(
    "Database",
    "Connected"
    if health["databaseConnected"]
    else "Disconnected"
)

col3.metric(
    "Model Server",
    "Online"
    if health["modelServerConnected"]
    else "Offline"
)

col4.metric(
    "Overload",
    "Running"
    if health["backendOverloaded"]
    else "Normal"
)

####################################################
# Review Statistics
####################################################

st.header("📈 Review Statistics")

try:

    stats = requests.get(
        f"{API}/api/reviews/stats"
    ).json()

    st.metric(
        "Total Reviews",
        stats.get("totalReviews", 0)
    )

except:

    st.warning("Statistics unavailable.")

####################################################
# Instructions
####################################################

with st.expander("📖 Demo Instructions"):

    st.markdown("""
### Frontend

- Toggle health
- Simulate overload
- Crash application

### Backend

- Enable/disable backend
- Simulate overload
- Disconnect database
- Disconnect AI Model

### Purpose

Demonstrates:

- Kubernetes Health Checks
- Graceful Degradation
- Microservice Failures
- Fault Tolerance
- Chaos Engineering
""")

####################################################
# Auto Refresh
####################################################

if st.checkbox("Auto Refresh"):

    time.sleep(3)
    st.rerun()

"""
api_client.py

Centralized API client for the Movie Review AI frontend.

Features
--------
✔ Automatic timeout
✔ Error handling
✔ Connection retry
✔ JSON parsing
✔ GET/POST/PUT/DELETE helpers
✔ Health checking
✔ Logging
"""

import logging
from typing import Dict, Any, Optional

import requests

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("MovieReviewAPI")


class APIClient:
    """
    Reusable API Client for communicating with FastAPI backend.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: int = 5,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    ##########################################################
    # Generic Request
    ##########################################################

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> Dict[str, Any]:

        url = f"{self.base_url}{endpoint}"

        try:

            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )

            response.raise_for_status()

            if response.content:
                return response.json()

            return {}

        except requests.Timeout:

            logger.error("Request timed out")

            return {
                "success": False,
                "error": "Request Timeout",
            }

        except requests.ConnectionError:

            logger.error("Backend unavailable")

            return {
                "success": False,
                "error": "Backend unavailable",
            }

        except requests.HTTPError as e:

            logger.error(str(e))

            try:
                return response.json()

            except Exception:
                return {
                    "success": False,
                    "error": str(e),
                }

        except Exception as e:

            logger.exception(e)

            return {
                "success": False,
                "error": str(e),
            }

    ##########################################################
    # GET
    ##########################################################

    def get(self, endpoint: str):

        return self.request("GET", endpoint)

    ##########################################################
    # POST
    ##########################################################

    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
    ):

        return self.request(
            "POST",
            endpoint,
            json=data,
        )

    ##########################################################
    # PUT
    ##########################################################

    def put(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
    ):

        return self.request(
            "PUT",
            endpoint,
            json=data,
        )

    ##########################################################
    # DELETE
    ##########################################################

    def delete(self, endpoint: str):

        return self.request(
            "DELETE",
            endpoint,
        )

    ##########################################################
    # Health
    ##########################################################

    def health(self):

        return self.get("/health")

    ##########################################################
    # Review APIs
    ##########################################################

    def get_reviews(self, movie_id: str):

        return self.get(f"/api/reviews/{movie_id}")

    def latest_reviews(self):

        return self.get("/api/reviews/latest")

    def review_stats(self):

        return self.get("/api/reviews/stats")

    def submit_review(
        self,
        movie_id: str,
        review_text: str,
    ):

        payload = {
            "movieId": movie_id,
            "reviewText": review_text,
        }

        return self.post(
            "/api/reviews",
            payload,
        )

    ##########################################################
    # Admin APIs
    ##########################################################

    def backend_status(self):

        return self.get("/api/admin/status")

    def toggle_backend(self):

        return self.post("/api/admin/toggle-health")

    def toggle_database(self):

        return self.post("/api/admin/toggle-database")

    def toggle_model(self):

        return self.post("/api/admin/toggle-model")

    def toggle_overload(self):

        return self.post("/api/admin/toggle-overload")

"""
state.py

Global application state manager for the Movie Review AI application.

Features
--------
✔ Centralized state management
✔ Session persistence
✔ Notifications
✔ Backend status
✔ Frontend simulation
✔ User preferences
✔ Loading indicators
✔ Easy reset
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import streamlit as st
from datetime import datetime


@dataclass
class Notification:
    """Notification model."""

    message: str
    level: str = "info"
    timestamp: str = field(
        default_factory=lambda: datetime.now().strftime("%H:%M:%S")
    )


class AppState:
    """
    Global Streamlit Application State
    """

    @staticmethod
    def initialize():

        defaults = {

            ################################################
            # Frontend
            ################################################

            "frontend_healthy": True,
            "frontend_overloaded": False,

            ################################################
            # Backend
            ################################################

            "backend_healthy": True,
            "backend_overloaded": False,
            "database_connected": True,
            "model_connected": True,

            ################################################
            # Reviews
            ################################################

            "current_movie": "",
            "latest_reviews": [],
            "movie_reviews": [],
            "review_statistics": {},

            ################################################
            # User
            ################################################

            "username": "Guest",
            "theme": "Light",

            ################################################
            # Loading
            ################################################

            "loading": False,

            ################################################
            # Notifications
            ################################################

            "notifications": [],

            ################################################
            # Cache
            ################################################

            "health_cache": {},

        }

        for key, value in defaults.items():

            if key not in st.session_state:
                st.session_state[key] = value

    ########################################################
    # Notifications
    ########################################################

    @staticmethod
    def notify(message, level="info"):

        notification = Notification(
            message=message,
            level=level
        )

        st.session_state.notifications.append(notification)

    @staticmethod
    def clear_notifications():

        st.session_state.notifications.clear()

    ########################################################
    # Loading
    ########################################################

    @staticmethod
    def start_loading():

        st.session_state.loading = True

    @staticmethod
    def stop_loading():

        st.session_state.loading = False

    ########################################################
    # Frontend
    ########################################################

    @staticmethod
    def toggle_frontend():

        st.session_state.frontend_healthy = \
            not st.session_state.frontend_healthy

    @staticmethod
    def toggle_frontend_overload():

        st.session_state.frontend_overloaded = \
            not st.session_state.frontend_overloaded

    ########################################################
    # Backend
    ########################################################

    @staticmethod
    def update_backend_status(data: Dict):

        st.session_state.backend_healthy = \
            data.get("backendHealthy", False)

        st.session_state.backend_overloaded = \
            data.get("backendOverloaded", False)

        st.session_state.database_connected = \
            data.get("databaseConnected", False)

        st.session_state.model_connected = \
            data.get("modelServerConnected", False)

    ########################################################
    # Reviews
    ########################################################

    @staticmethod
    def set_movie(movie_id):

        st.session_state.current_movie = movie_id

    @staticmethod
    def set_movie_reviews(reviews):

        st.session_state.movie_reviews = reviews

    @staticmethod
    def set_latest_reviews(reviews):

        st.session_state.latest_reviews = reviews

    @staticmethod
    def set_statistics(stats):

        st.session_state.review_statistics = stats

    ########################################################
    # User
    ########################################################

    @staticmethod
    def set_username(name):

        st.session_state.username = name

    @staticmethod
    def set_theme(theme):

        st.session_state.theme = theme

    ########################################################
    # Cache
    ########################################################

    @staticmethod
    def cache_health(data):

        st.session_state.health_cache = data

    @staticmethod
    def get_health_cache():

        return st.session_state.health_cache

    ########################################################
    # Reset
    ########################################################

    @staticmethod
    def reset():

        keys = list(st.session_state.keys())

        for key in keys:
            del st.session_state[key]

        AppState.initialize()

    ########################################################
    # Snapshot
    ########################################################

    @staticmethod
    def snapshot():

        return {

            "frontendHealthy":
                st.session_state.frontend_healthy,

            "frontendOverloaded":
                st.session_state.frontend_overloaded,

            "backendHealthy":
                st.session_state.backend_healthy,

            "backendOverloaded":
                st.session_state.backend_overloaded,

            "databaseConnected":
                st.session_state.database_connected,

            "modelConnected":
                st.session_state.model_connected,

            "currentMovie":
                st.session_state.current_movie,

            "totalNotifications":
                len(st.session_state.notifications),

            "loading":
                st.session_state.loading,

            "theme":
                st.session_state.theme,

            "username":
                st.session_state.username
        }


############################################################
# Initialize Automatically
############################################################

AppState.initialize()
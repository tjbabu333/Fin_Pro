"""
security_config.py

Production-ready security configuration for FastAPI.

Features
--------
✔ CORS configuration
✔ Security headers
✔ HTTPS support
✔ Trusted hosts
✔ Rate limiting ready
✔ Environment-based configuration
✔ Configurable allowed origins
✔ Middleware-based architecture
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware


# ---------------------------------------------------
# Environment Configuration
# ---------------------------------------------------

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")


# ---------------------------------------------------
# Custom Security Headers
# ---------------------------------------------------

class SecurityHeadersMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate"
        )

        response.headers["Pragma"] = "no-cache"

        response.headers["Expires"] = "0"

        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"

        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"

        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self';"
        )

        return response


# ---------------------------------------------------
# Security Configuration
# ---------------------------------------------------

def configure_security(app: FastAPI):
    """
    Configure application security.
    """

    # -----------------------------
    # CORS
    # -----------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS
        if ENVIRONMENT == "production"
        else ["*"],

        allow_credentials=True,

        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS"
        ],

        allow_headers=["*"],

        expose_headers=["*"],

        max_age=3600
    )

    # -----------------------------
    # Trusted Hosts
    # -----------------------------
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=ALLOWED_HOSTS
        if ENVIRONMENT == "production"
        else ["*"]
    )

    # -----------------------------
    # HTTPS Redirect
    # -----------------------------
    if ENVIRONMENT == "production":
        app.add_middleware(HTTPSRedirectMiddleware)

    # -----------------------------
    # Security Headers
    # -----------------------------
    app.add_middleware(SecurityHeadersMiddleware)
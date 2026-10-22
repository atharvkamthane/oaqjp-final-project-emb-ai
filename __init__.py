"""Application package initialization and security headers."""

from flask import Flask
from flask_talisman import Talisman


def init_security(app: Flask) -> None:
    """Apply common HTTP security headers to a Flask application.

    Enable HTTPS enforcement in production by setting TALISMAN_FORCE_HTTPS=1.
    """
    import os

    force_https = os.getenv("TALISMAN_FORCE_HTTPS", "0") == "1"
    Talisman(
        app,
        force_https=force_https,
        strict_transport_security=True,
        content_security_policy={
            "default-src": ["'self'"],
            "object-src": ["'none'"],
            "frame-ancestors": ["'none'"],
        },
        content_security_policy_nonce_in=["script-src"],
        session_cookie_secure=force_https,
        session_cookie_http_only=True,
        session_cookie_samesite="Lax",
    )

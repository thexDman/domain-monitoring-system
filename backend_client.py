import os
import requests
from flask import session

# Backend base URL (env-driven, container-friendly)
BACKEND_BASE_URL = os.environ.get(
    "BACKEND_BASE_URL",
    "http://localhost:8080"
)

# Shared request settings
DEFAULT_TIMEOUT = 5


# ---------------------------
# Internal helpers
# ---------------------------

def _auth_headers():
    """
    Build authentication headers for backend requests.
    Identity is propagated ONLY via headers.
    """
    headers = {}

    username = session.get("username")
    if username:
        headers["X-Username"] = username

    return headers


def _full_url(path: str) -> str:
    """
    Normalize backend URL paths.
    Ensures '/api/...' format.
    """
    if not path.startswith("/"):
        path = "/" + path
    return f"{BACKEND_BASE_URL}{path}"


def _handle_response(response):
    """
    Safely parse backend responses.
    Always return (json, status_code).
    """
    try:
        data = response.json()
    except ValueError:
        data = {
            "ok": False,
            "error": "Invalid response from backend"
        }

    return data, response.status_code


# ---------------------------
# Public API
# ---------------------------

def backend_get(path):
    try:
        response = requests.get(
            _full_url(path),
            headers=_auth_headers(),
            timeout=DEFAULT_TIMEOUT
        )
        return _handle_response(response)

    except requests.RequestException as e:
        return {
            "ok": False,
            "error": f"Backend connection failed: {str(e)}"
        }, 503


def backend_post(path, json=None, files=None):
    try:
        response = requests.post(
            _full_url(path),
            headers=_auth_headers(),
            json=json,
            files=files,
            timeout=DEFAULT_TIMEOUT
        )
        return _handle_response(response)

    except requests.RequestException as e:
        return {
            "ok": False,
            "error": f"Backend connection failed: {str(e)}"
        }, 503


def backend_delete(path, json=None):
    try:
        response = requests.delete(
            _full_url(path),
            headers=_auth_headers(),
            json=json,
            timeout=DEFAULT_TIMEOUT
        )
        return _handle_response(response)

    except requests.RequestException as e:
        return {
            "ok": False,
            "error": f"Backend connection failed: {str(e)}"
        }, 503

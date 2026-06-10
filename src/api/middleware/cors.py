"""CORS middleware settings for the FastAPI application."""

CORS_SETTINGS: dict = {
    "allow_origins": ["*"],  # Restrict in production
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["*"],
}

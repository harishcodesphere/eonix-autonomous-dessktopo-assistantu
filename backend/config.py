"""
EONIX Configuration — Central settings and environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── AI Brain Settings ──────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"

# ── Compatibility Settings ─────────────────────────────────────
# This class mimics the `settings` object expected by some legacy imports
class Settings:
    OLLAMA_HOST = OLLAMA_URL
    OLLAMA_MODEL = OLLAMA_MODEL
    GEMINI_API_KEY = GOOGLE_API_KEY
    GEMINI_MODEL = GEMINI_MODEL

settings = Settings()

# ── System Settings ────────────────────────────────────────────
# Set to True to require user confirmation for destructive actions
REQUIRE_CONFIRMATION = os.getenv("REQUIRE_CONFIRMATION", "False").lower() == "true"

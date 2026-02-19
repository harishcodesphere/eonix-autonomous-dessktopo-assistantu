"""
EONIX Configuration — Central settings and environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── AI Brain Settings ──────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240620")

# ── Compatibility Settings ─────────────────────────────────────
# This class mimics the `settings` object expected by some legacy imports
class Settings:
    OLLAMA_HOST = OLLAMA_URL
    OLLAMA_MODEL = OLLAMA_MODEL
    GEMINI_API_KEY = GOOGLE_API_KEY
    GEMINI_MODEL = GEMINI_MODEL

settings = Settings()

# ── Database Settings ──────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "memory", "eonix.db")

# ── System Settings ────────────────────────────────────────────
# Set to True to require user confirmation for destructive actions
REQUIRE_CONFIRMATION = os.getenv("REQUIRE_CONFIRMATION", "False").lower() == "true"

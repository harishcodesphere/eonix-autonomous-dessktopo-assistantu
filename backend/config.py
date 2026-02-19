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

# ── Default brain routing ──────────────────────────────────────
# "local" | "gemini" | "auto"
DEFAULT_BRAIN = os.getenv("DEFAULT_BRAIN", "auto")

# ── Complexity threshold for routing ──────────────────────────
COMPLEXITY_THRESHOLD = 0.6

# ── Database ───────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "eonix_memory.db")

# ── Tool settings ──────────────────────────────────────────────
TYPING_DELAY = 0.04
APP_LAUNCH_WAIT = 2.5
COMMAND_TIMEOUT = 30

# ── Server ─────────────────────────────────────────────────────
HOST = "127.0.0.1"
PORT = 8000

# ── Voice ──────────────────────────────────────────────────────
ENABLE_VOICE = os.getenv("ENABLE_VOICE", "true").lower() == "true"
VOICE_RATE = int(os.getenv("VOICE_RATE", "175"))
VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "0.9"))

# ── Safety ─────────────────────────────────────────────────────
REQUIRE_CONFIRMATION = os.getenv("REQUIRE_CONFIRMATION", "false").lower() == "true"

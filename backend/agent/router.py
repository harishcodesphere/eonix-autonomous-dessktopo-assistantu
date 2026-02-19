"""
EONIX Router — Decides which AI brain to use for each request.
"""
import re
from typing import Optional, Tuple

COMPLEX_KEYWORDS = [
    "prepare", "organize", "optimize", "set up", "setup",
    "environment", "workflow", "configure", "analyze",
    "and then", "after that", "also", "multiple", "all of",
    "every", "create a script", "write code", "generate",
    "explain", "summarize", "compare", "research"
]

VISUAL_KEYWORDS = [
    "screen", "screenshot", "image", "see", "look at",
    "what is on", "read this", "analyze this", "what do you see",
    "what's on screen", "capture"
]

SIMPLE_PATTERNS = [
    r"^open \w+$",
    r"^close \w+$",
    r"^search .+$",
    r"^type .+$",
    r"^what (is|are) (my )?(cpu|ram|memory|battery|disk)",
    r"^(how much|show) (ram|memory|cpu|disk|battery)",
    r"^show (running )?processes$",
    r"^(what time|what date)",
    r"^(open|go to) .+ (and|then) (search|go to|open|type)",
]


def route(user_input: str, forced: Optional[str] = None, ollama_available: bool = True,
          gemini_available: bool = True) -> str:
    """
    Decide which brain to use.
    Returns: "local" | "gemini"
    """
    # Handle forced brain prefix
    if forced:
        forced = forced.lower()
        if forced in ("local", "ollama"):
            return "local"
        if forced in ("gemini", "google"):
            return "gemini"

    # If Ollama is down, use Gemini
    if not ollama_available:
        return "gemini" if gemini_available else "local"

    text = user_input.lower().strip()

    # Visual/screen tasks → Gemini
    for kw in VISUAL_KEYWORDS:
        if kw in text:
            return "gemini" if gemini_available else "local"

    # Check simple patterns → local
    for pattern in SIMPLE_PATTERNS:
        if re.match(pattern, text, re.IGNORECASE):
            return "local"

    # Complex keywords → Gemini
    for kw in COMPLEX_KEYWORDS:
        if kw in text:
            return "gemini" if gemini_available else "local"

    # Word count heuristic
    word_count = len(text.split())
    if word_count <= 8:
        return "local"
    elif word_count >= 15:
        return "gemini" if gemini_available else "local"

    # Default: local (fast, free, offline)
    return "local"


def parse_brain_prefix(user_input: str) -> Tuple[Optional[str], str]:
    """
    Parse @local, @gemini, @claude prefix from input.
    Returns: (forced_brain, clean_input)
    """
    prefixes = {
        "@local": "local",
        "@ollama": "local",
        "@gemini": "gemini",
        "@gemini": "gemini",
        "@google": "gemini",
        "@claude": "claude",
        "@anthropic": "claude",
    }
    for prefix, brain in prefixes.items():
        if user_input.lower().startswith(prefix):
            return brain, user_input[len(prefix):].strip()  # type: ignore[index]
    return None, user_input

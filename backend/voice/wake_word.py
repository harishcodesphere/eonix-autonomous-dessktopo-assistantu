"""
Eonix Wake Word Detection
Detects wake words like "Hey Eonix" or "Jarvis" from audio stream.
"""
import asyncio
from loguru import logger


class WakeWordDetector:
    """Detects wake words from microphone audio stream."""

    WAKE_WORDS = ["eonix", "hey eonix", "jarvis", "hey jarvis"]

    def __init__(self):
        self._running = False
        self._callback = None
        self._available = self._check_audio()

    def _check_audio(self) -> bool:
        """Check if audio input is available."""
        try:
            import sounddevice  # noqa
            return True
        except (ImportError, Exception):
            logger.warning("sounddevice not installed. Wake word detection disabled.")
            return False

    async def start(self, on_wake: callable = None):
        """Start listening for wake words."""
        if not self._available:
            logger.warning("Audio not available. Wake word detector not started.")
            return

        self._running = True
        self._callback = on_wake
        logger.info(f"Wake word detector started. Listening for: {self.WAKE_WORDS}")

        # In production: a continuous audio stream would be processed here
        # For now, we provide the structure for integration
        while self._running:
            await asyncio.sleep(1)

    async def stop(self):
        """Stop listening."""
        self._running = False
        logger.info("Wake word detector stopped")

    async def _on_detected(self, word: str):
        """Handle wake word detection."""
        logger.info(f"Wake word detected: {word}")
        if self._callback:
            if asyncio.iscoroutinefunction(self._callback):
                await self._callback(word)
            else:
                self._callback(word)

    @property
    def is_available(self) -> bool:
        return self._available

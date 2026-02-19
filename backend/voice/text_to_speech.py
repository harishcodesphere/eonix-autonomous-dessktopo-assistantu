"""
Eonix Text-to-Speech
Piper TTS wrapper for local voice synthesis.
"""
import subprocess
import tempfile
import os
from loguru import logger


class TextToSpeech:
    """Generates speech from text using Piper TTS (local)."""

    def __init__(self, model_path: str = None, voice: str = "en_US-amy-medium"):
        self.voice = voice
        self.model_path = model_path
        self._available = self._check_piper()

    def _check_piper(self) -> bool:
        """Check if Piper TTS is available."""
        try:
            result = subprocess.run(
                ["piper", "--help"],
                capture_output=True, text=True, timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("Piper TTS not found. TTS will be unavailable.")
            return False

    async def synthesize(self, text: str, output_path: str = None) -> dict:
        """
        Convert text to speech.
        Returns: {"audio_path": str, "duration": float}
        """
        if not self._available:
            return {"audio_path": "", "error": "TTS not available"}

        if not output_path:
            fd, output_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)

        try:
            cmd = [
                "piper",
                "--model", self.voice,
                "--output_file", output_path,
            ]
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            _, stderr = process.communicate(input=text.encode())

            if process.returncode != 0:
                logger.error(f"Piper TTS failed: {stderr.decode()}")
                return {"audio_path": "", "error": stderr.decode()}

            logger.info(f"TTS generated: {output_path}")
            return {"audio_path": output_path}
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            return {"audio_path": "", "error": str(e)}

    @property
    def is_available(self) -> bool:
        return self._available

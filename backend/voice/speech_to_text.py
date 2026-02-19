"""
Eonix Speech-to-Text
Whisper-based voice recognition with graceful fallback.
"""
from loguru import logger

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning("faster-whisper not installed. STT will be unavailable.")


class SpeechToText:
    """Transcribes audio to text using OpenAI Whisper (local)."""

    def __init__(self, model_size: str = "base"):
        self.model = None
        if WHISPER_AVAILABLE:
            try:
                self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
                logger.info(f"Whisper model loaded: {model_size}")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")

    async def transcribe(self, audio_path: str, language: str = "en") -> dict:
        """
        Transcribe an audio file to text.
        Returns: {"text": str, "language": str, "segments": list}
        """
        if not self.model:
            return {"text": "", "language": language, "segments": [], "error": "STT model not available"}

        try:
            segments, info = self.model.transcribe(audio_path, language=language)
            text_parts = []
            segment_list = []
            for seg in segments:
                text_parts.append(seg.text)
                segment_list.append({
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text,
                })

            full_text = " ".join(text_parts).strip()
            logger.info(f"Transcribed: {full_text[:80]}...")

            return {
                "text": full_text,
                "language": info.language,
                "segments": segment_list,
            }
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return {"text": "", "language": language, "segments": [], "error": str(e)}

    @property
    def is_available(self) -> bool:
        return self.model is not None

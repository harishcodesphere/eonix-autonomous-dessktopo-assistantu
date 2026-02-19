"""
EONIX Voice System — Input (STT) + Wake Word
Handles microphone listening, wake word detection, and transcription.
"""
import os
import time
import threading
import asyncio
from typing import Any, Optional, Callable
from asyncio import AbstractEventLoop

# Optional imports — guarded so the rest of the app works even if not installed
try:
    import speech_recognition as sr  # type: ignore[import-untyped]
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False
    sr = None  # type: ignore[assignment]

# WhisperModel is typed as Optional[Any] so that assigning None is valid
_WhisperModelClass: Optional[Any] = None
try:
    from faster_whisper import WhisperModel as _WhisperModelClass  # type: ignore[no-redef]
    _WHISPER_AVAILABLE = True
except ImportError:
    _WHISPER_AVAILABLE = False

# voice_engine is Optional[Any] — None when not available
try:
    from tools.voice_engine import voice_engine
except ImportError:
    voice_engine = None

# Configuration
WAKE_WORDS = ["hey eonix", "eonix", "hi eonix", "okay eonix"]
MODEL_SIZE = "tiny"   # 'tiny', 'base', 'small', 'medium', 'large'
COMPUTE_TYPE = "int8"  # 'float16' for GPU, 'int8' for CPU


class VoiceSystem:
    def __init__(self) -> None:
        # These are None until sr is available / model is loaded
        self.recognizer: Optional[object] = sr.Recognizer() if _SR_AVAILABLE and sr else None
        
        # sr.Microphone() requires PyAudio; if it's missing, don't crash the whole backend.
        self.microphone: Optional[object] = None
        if _SR_AVAILABLE and sr:
            try:
                self.microphone = sr.Microphone()
            except Exception:
                self.microphone = None
                
        self.is_listening: bool = False
        self.callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        self.loop: Optional[AbstractEventLoop] = None
        self.state: str = "idle"      # idle, listening, processing, speaking
        self.manual_trigger: bool = False
        self.thread: Optional[threading.Thread] = None

        # Load Whisper (lazy load to speed up startup)
        self.audio_model: Optional[object] = None

    def _load_model(self) -> None:
        if not self.audio_model and _WHISPER_AVAILABLE and _WhisperModelClass:
            print("Loading Whisper AI model...")
            try:
                self.audio_model = _WhisperModelClass(MODEL_SIZE, device="cpu", compute_type=COMPUTE_TYPE)
                print("OK: Whisper AI loaded")
            except Exception as e:
                print(f"ERROR loading Whisper: {e}")

    def set_callback(self, callback_func: Callable) -> None:
        """Set the function to call when a command is transcribed."""
        self.callback = callback_func

    def set_status_callback(self, callback_func: Callable) -> None:
        """Set the function to call when voice state changes."""
        self.status_callback = callback_func

    def _set_state(self, state: str) -> None:
        self.state = state
        # print(f"Voice State: {state}")  # noisy

        # Broadcast state
        if self.status_callback is not None:
            cb = self.status_callback
            try:
                # If we are in the listener thread, schedule on the main loop
                current_loop = self.loop
                if current_loop is not None and current_loop.is_running():
                    asyncio.run_coroutine_threadsafe(cb(state), current_loop)
            except Exception as e:
                print(f"State Broadcast Error: {e}")

    def trigger(self) -> None:
        """Manually trigger listening (bypass wake word)."""
        self.manual_trigger = True

    def start(self) -> None:
        """Start the background listening loop."""
        if self.is_listening:
            return

        if not _SR_AVAILABLE:
            print("WARNING: speech_recognition not installed — voice input disabled.")
            return
        if self.microphone is None or self.recognizer is None:
            print("WARNING: Microphone/PyAudio not available — voice input disabled.")
            return

        # Capture connection to main event loop
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()

        self._load_model()
        self.is_listening = True

        # Start thread
        t = threading.Thread(target=self._run_listener, daemon=True)
        self.thread = t
        t.start()
        print("OK: EONIX Voice System: ONLINE (Listening for 'Hey Eonix')")

    def stop(self) -> None:
        self.is_listening = False
        t = self.thread
        if t is not None and t.is_alive():
            t.join(timeout=2)

    def _run_listener(self) -> None:
        """Main listening loop."""
        if not self.microphone or not self.recognizer:
            return

        mic = self.microphone
        rec = self.recognizer
        # type: ignore[union-attr]
        rec.pause_threshold = 0.8  # type: ignore[union-attr]

        try:
            with mic as source:  # type: ignore[union-attr]
                rec.adjust_for_ambient_noise(source, duration=1)  # type: ignore[union-attr]
                rec.dynamic_energy_threshold = True  # type: ignore[union-attr]
        except Exception:
            pass

        while self.is_listening:
            # If system is speaking, pause listening to avoid self-trigger
            if voice_engine and voice_engine.is_speaking:
                self._set_state("speaking")
                time.sleep(0.5)
                continue
                
            if self.state == "speaking": # Legacy check
                self._set_state("idle")

            # Check manual trigger
            if self.manual_trigger:
                self.manual_trigger = False
                self._handle_active_listening()
                continue

            try:
                self._set_state("idle")
                with mic as source:  # type: ignore[union-attr]
                    # Listen for wake word phrase (short timeout)
                    # We use speech_recognition's listen which blocks until silence
                    try:
                        # Listen for a short burst
                        audio = rec.listen(source, timeout=1.0, phrase_time_limit=3.0)  # type: ignore[union-attr]
                    except Exception:
                        continue  # No speech / WaitTimeoutError

                self._set_state("processing")
                # Quick check for wake word using Google (fast fallback)
                try:
                    text = rec.recognize_google(audio).lower()  # type: ignore[union-attr]
                    # Check for wake words
                    if any(w in text for w in WAKE_WORDS):
                        self._handle_active_listening()
                except Exception:
                    pass # Not understood or network error

            except Exception as e:
                # print(f"Voice Loop Error: {e}")
                time.sleep(1)

    def _handle_active_listening(self) -> None:
        """Triggered when wake word is detected or manual trigger."""
        print("🔔 Wake Word Detected!")
        self._set_state("listening_active")

        # Play sound? (Optional)
        
        if not self.microphone or not self.recognizer:
            return

        mic = self.microphone
        rec = self.recognizer

        # Record actual command
        try:
            with mic as source:  # type: ignore[union-attr]
                # print("🎤 Recording command...")
                # Listen longer for the actual command
                audio = rec.listen(source, timeout=5.0, phrase_time_limit=10.0)  # type: ignore[union-attr]

            self._set_state("processing")
            print("🧠 Transcribing...")

            # 1. Try Whisper if available (Local, better)
            transcription = ""
            
            if self.audio_model:
                # Save to temp file for Whisper
                temp_wav = "temp_command.wav"
                try:
                    with open(temp_wav, "wb") as f:
                        f.write(audio.get_wav_data())
                    
                    segments, _ = self.audio_model.transcribe(temp_wav, beam_size=5)  # type: ignore[union-attr]
                    transcription = " ".join([segment.text for segment in segments]).strip()
                except Exception as e:
                    print(f"Whisper Error: {e}")
                finally:
                    if os.path.exists(temp_wav):
                        os.remove(temp_wav)

            # 2. Fallback to Google if Whisper failed or not loaded
            if not transcription:
                try:
                    transcription = rec.recognize_google(audio)  # type: ignore[union-attr]
                except Exception:
                    pass

            if transcription:
                print(f"User: {transcription}")

                # Send to orchestrator via callback
                cb = self.callback
                if cb:
                    # We need to run this on the main loop
                    current_loop = self.loop
                    if current_loop is not None and current_loop.is_running():
                         asyncio.run_coroutine_threadsafe(cb(transcription), current_loop)
                    else:
                        print("Warning: No event loop to send command to")
            else:
                print("ERROR: No speech detected")
                if voice_engine:
                    # voice_engine.speak("I didn't hear anything.")
                    pass

        except Exception as e:
            print(f"Command Error: {e}")

        self._set_state("idle")


# Global instance
voice_system = VoiceSystem()

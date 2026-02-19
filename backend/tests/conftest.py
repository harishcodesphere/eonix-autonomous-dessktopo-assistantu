import pytest
import sys
import os
from unittest.mock import MagicMock

# Mock heavy dependencies to avoid installation requirement for tests
sys.modules["chromadb"] = MagicMock()
sys.modules["chromadb.PersistentClient"] = MagicMock()
sys.modules["pygame"] = MagicMock()
sys.modules["pyttsx3"] = MagicMock()
sys.modules["pyaudio"] = MagicMock()
sys.modules["speech_recognition"] = MagicMock()
sys.modules["playwright"] = MagicMock()
sys.modules["playwright.async_api"] = MagicMock()
sys.modules["edge_tts"] = MagicMock()
sys.modules["faster_whisper"] = MagicMock()
sys.modules["google"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()

# Add backend to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def client():
    from main import app
    return TestClient(app)


@pytest.fixture
def mock_orchestrator(mocker):
    # Lazy import to avoid triggering app startup
    from agent.orchestrator import AgentOrchestrator
    
    mock = mocker.Mock(spec=AgentOrchestrator)
    mock.process.return_value = {
        "reply": "Test response",
        "brain": "local",
        "actions": [],
        "duration_ms": 100,
        "success": True
    }
    return mock


@pytest.fixture
def context_manager():
    # Helper mock if needed
    return MagicMock()

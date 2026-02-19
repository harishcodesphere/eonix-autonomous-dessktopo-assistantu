import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add backend to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from core.orchestrator import Orchestrator
from core.context_manager import ContextManager

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_orchestrator(mocker):
    mock = mocker.Mock(spec=Orchestrator)
    # Mock return values for common methods
    mock.process_command.return_value = {
        "response": "Test response",
        "intent": "general_query",
        "actions": []
    }
    return mock

@pytest.fixture
def context_manager():
    return ContextManager()

"""
Tests for AI components — IntentClassifier and TaskPlanner.
"""
import pytest
import sys
import os
from unittest.mock import AsyncMock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.asyncio
async def test_intent_classifier_returns_dict():
    """IntentClassifier.classify() should return a dict with intent/action/entities."""
    with patch("ai.ollama_client.OllamaClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.generate_response = AsyncMock(return_value='{"intent": "general_query", "action": "conversation", "entities": {}, "confidence": 0.9}')

        from ai.intent_classifier import IntentClassifier
        classifier = IntentClassifier()
        classifier.ai = mock_instance

        result = await classifier.classify("What is machine learning?")
        assert isinstance(result, dict)
        assert "intent" in result


@pytest.mark.asyncio
async def test_intent_classifier_fallback():
    """Should use fallback when LLM returns garbage."""
    with patch("ai.ollama_client.OllamaClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.generate_response = AsyncMock(return_value="not json at all")

        from ai.intent_classifier import IntentClassifier
        classifier = IntentClassifier()
        classifier.ai = mock_instance

        result = await classifier.classify("open chrome")
        assert isinstance(result, dict)
        assert "intent" in result


@pytest.mark.asyncio
async def test_task_planner_returns_plan():
    """TaskPlanner.plan() should return a dict with steps."""
    with patch("ai.ollama_client.OllamaClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.generate_response = AsyncMock(
            return_value='{"tasks": [{"step": 1, "action": "test", "tool": "test_tool", "args": {}}], "estimated_time": "1s"}'
        )

        from ai.task_planner import TaskPlanner
        planner = TaskPlanner()
        planner.ai = mock_instance

        result = await planner.plan("test command", {"intent": "test"})
        assert isinstance(result, dict)

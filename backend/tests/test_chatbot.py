"""
Tests for the Smart Chatbot Engine.
"""
import pytest
import sys
import os
from unittest.mock import AsyncMock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_conversation_memory():
    """ConversationMemory should maintain sliding window of messages."""
    from ai.chatbot import ConversationMemory

    mem = ConversationMemory(max_turns=3)

    # Add some messages
    mem.add("user", "Hello")
    mem.add("assistant", "Hi there!")
    mem.add("user", "How are you?")

    assert mem.turn_count == 2
    assert len(mem.get_messages()) == 3

    # Check context summary
    summary = mem.get_context_summary()
    assert "Hello" in summary
    assert "Hi there!" in summary


def test_conversation_memory_sliding_window():
    """Memory should respect max_turns limit."""
    from ai.chatbot import ConversationMemory

    mem = ConversationMemory(max_turns=2)

    # Add more messages than the window allows
    for i in range(10):
        mem.add("user", f"Message {i}")
        mem.add("assistant", f"Reply {i}")

    # Should only keep the last max_turns * 2 messages
    messages = mem.get_messages()
    assert len(messages) <= 4  # max_turns=2, so 2*2=4 messages max


def test_conversation_memory_clear():
    """Clear should reset the conversation."""
    from ai.chatbot import ConversationMemory

    mem = ConversationMemory()
    mem.add("user", "Hello")
    mem.add("assistant", "Hi!")

    mem.clear()
    assert mem.turn_count == 0
    assert len(mem.get_messages()) == 0


@pytest.mark.asyncio
async def test_chatbot_chat():
    """Chatbot.chat() should return a dict with reply, brain, mood."""
    with patch("ai.ollama_client.OllamaClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.chat = AsyncMock(return_value="Hello! I'm Eonix, your assistant!")

        from ai.chatbot import Chatbot
        bot = Chatbot()
        bot.ollama = mock_instance

        result = await bot.chat("Hello")

        assert isinstance(result, dict)
        assert "reply" in result
        assert "brain" in result
        assert "mood" in result
        assert result["reply"] == "Hello! I'm Eonix, your assistant!"


@pytest.mark.asyncio
async def test_chatbot_builtin_fallback():
    """When both LLMs fail, chatbot should use built-in responses."""
    with patch("ai.ollama_client.OllamaClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.chat = AsyncMock(return_value="❌ Error: not available")

        from ai.chatbot import Chatbot
        bot = Chatbot()
        bot.ollama = mock_instance
        bot._gemini = None

        result = await bot.chat("hello")

        assert isinstance(result, dict)
        assert "reply" in result
        assert result["brain"] == "fallback"
        assert "eonix" in result["reply"].lower() or "hey" in result["reply"].lower()


def test_chatbot_reset():
    """Reset should clear conversation memory."""
    from ai.chatbot import Chatbot

    bot = Chatbot()
    bot.memory.add("user", "test")
    bot.reset_conversation()

    assert bot.memory.turn_count == 0


def test_chatbot_stats():
    """get_conversation_stats() should return valid stats."""
    from ai.chatbot import Chatbot

    bot = Chatbot()
    stats = bot.get_conversation_stats()

    assert "total_turns" in stats
    assert "messages" in stats
    assert "current_mood" in stats

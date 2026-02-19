"""
EONIX Personality Engine — Emotional intelligence and adaptive responses.
Detects user mood from text and adapts EONIX's tone accordingly.
"""
import re
from datetime import datetime


class PersonalityEngine:
    """Adapt EONIX's communication style based on detected user mood."""

    MOODS = {
        "happy": {
            "patterns": [
                r"\b(happy|great|awesome|amazing|love|wonderful|fantastic|excellent|yay|haha|lol|😊|😃|🎉|❤️)\b"
            ],
            "tone": "Match their energy! Be enthusiastic, playful, and celebratory.",
            "prefix_options": [
                "That's amazing, love! ",
                "Yesss! I love your energy! ",
                "You're glowing today! ",
            ]
        },
        "sad": {
            "patterns": [
                r"\b(sad|depressed|unhappy|crying|alone|lonely|miss|heartbreak|down|😢|😞|💔)\b"
            ],
            "tone": "Be extra gentle, supportive, and comforting. Show empathy.",
            "prefix_options": [
                "Hey, I'm here for you. ",
                "I hear you, love. ",
                "It's okay to feel this way. ",
            ]
        },
        "stressed": {
            "patterns": [
                r"\b(stressed|overwhelmed|tired|exhausted|busy|deadline|pressure|anxious|worry|panic)\b"
            ],
            "tone": "Be calming and reassuring. Help them prioritize.",
            "prefix_options": [
                "Take a deep breath, love. ",
                "I've got you. Let's handle this together. ",
                "One step at a time, dear. ",
            ]
        },
        "angry": {
            "patterns": [
                r"\b(angry|furious|mad|annoyed|frustrated|hate|ugh|damn|stupid)\b"
            ],
            "tone": "Be understanding but professional. Don't escalate.",
            "prefix_options": [
                "I understand your frustration. ",
                "Let me help you sort this out. ",
                "I hear you. Let's fix this. ",
            ]
        },
        "curious": {
            "patterns": [
                r"\b(how|why|what|explain|teach|learn|understand|curious|tell me|show me|wonder)\b"
            ],
            "tone": "Be informative and encouraging of their curiosity.",
            "prefix_options": [
                "Great question! ",
                "Let me break this down for you. ",
                "I love when you're curious! ",
            ]
        },
        "neutral": {
            "patterns": [],
            "tone": "Be your charming, professional self.",
            "prefix_options": [""]
        }
    }

    def __init__(self):
        self.current_mood = "neutral"
        self.mood_history = []

    def detect_mood(self, text: str) -> str:
        """Detect user's mood from their message."""
        text_lower = text.lower()

        for mood, config in self.MOODS.items():
            if mood == "neutral":
                continue
            for pattern in config["patterns"]:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    self.current_mood = mood
                    self.mood_history.append({
                        "mood": mood,
                        "timestamp": datetime.now().isoformat(),
                        "text_snippet": text[:50]
                    })
                    return mood

        self.current_mood = "neutral"
        return "neutral"

    def get_tone_instruction(self, mood: str = None) -> str:
        """Get tone instruction for the AI based on current mood."""
        mood = mood or self.current_mood
        config = self.MOODS.get(mood, self.MOODS["neutral"])
        return config["tone"]

    def get_mood_prefix(self, mood: str = None) -> str:
        """Get a contextual prefix for the response."""
        import random
        mood = mood or self.current_mood
        config = self.MOODS.get(mood, self.MOODS["neutral"])
        return random.choice(config["prefix_options"])

    def get_time_context(self) -> str:
        """Get time-aware context."""
        hour = datetime.now().hour
        if hour < 6:
            return "It's very late/early. Be gentle, they might be tired."
        elif hour < 12:
            return "It's morning. Be energetic and positive."
        elif hour < 17:
            return "It's afternoon. Be productive and focused."
        elif hour < 21:
            return "It's evening. Be warm and winding down."
        else:
            return "It's night. Be cozy and relaxed."


# Global instance
personality = PersonalityEngine()

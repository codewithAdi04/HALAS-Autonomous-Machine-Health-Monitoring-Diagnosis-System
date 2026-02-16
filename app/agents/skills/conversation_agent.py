import random


class ConversationSkill:
    """
    Conversational fallback skill
    """

    RESPONSES = [
        "Hello! I am HALAS 🤖. How can I assist you today?",
        "All systems are functioning normally.",
        "I'm analyzing your request.",
        "Please provide more details."
    ]

    def execute(self, perception_data: dict) -> dict:
        return {
            "status": "success",
            "response": random.choice(self.RESPONSES)
        }
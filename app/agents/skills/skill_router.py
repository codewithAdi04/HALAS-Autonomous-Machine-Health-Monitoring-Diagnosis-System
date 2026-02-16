from app.core.logger import logger
from app.agents.skills.conversation_agent import ConversationSkill
from app.agents.skills.diagnosis_agent import DiagnosisAgent


class SkillRouter:
    """
    Routes planner intent to appropriate skill
    """

    def __init__(self):
        self.skill_registry = {
            "conversation": ConversationSkill(),
            "diagnosis": DiagnosisAgent(),
        }

    def route(self, intent: str, perception_data: dict) -> dict:
        logger.info(f"[SkillRouter] Routing intent: {intent}")

        skill = self.skill_registry.get(intent)

        if not skill:
            logger.warning("[SkillRouter] Unknown intent, using conversation fallback")
            skill = self.skill_registry["conversation"]

        return skill.execute(perception_data)
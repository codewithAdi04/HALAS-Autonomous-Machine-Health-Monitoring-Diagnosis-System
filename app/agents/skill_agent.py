from typing import Dict
from app.core.logger import logger

from app.agents.skills.conversation_skill import ConversationSkill
from app.agents.skills.diagnosis_skill import DiagnosisSkill


class SkillRouter:
    """
    Industry-grade Skill Router
    Responsible only for routing top-level intents to skills
    """

    def __init__(self):
        self.skill_registry = {
            "conversation": ConversationSkill(),
            "diagnosis": DiagnosisSkill(),
        }

    def route(self, intent: str, perception_data: Dict) -> Dict:
        logger.info(f"[SkillRouter] Routing intent: {intent}")

        skill = self.skill_registry.get(intent)

        #  Fallback safety
        if not skill:
            logger.warning(
                f"[SkillRouter] Unknown intent '{intent}', falling back to conversation"
            )
            intent = "conversation"
            skill = self.skill_registry[intent]

        # Execute skill
        result = skill.execute(perception_data)

        #  Result validation (CRITICAL)
        if not isinstance(result, dict):
            logger.error("[SkillRouter] Skill returned invalid result type")
            return {
                "status": "fail",
                "response": "Skill execution failed.",
                "skill": intent,
                "routed_by": "SkillRouter"
            }

        # 🔒 Normalize output
        result.setdefault("status", "success")
        result.setdefault("response", "HALAS completed the task.")
        result["skill"] = intent
        result["routed_by"] = "SkillRouter"

        return result
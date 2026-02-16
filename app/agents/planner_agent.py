from app.core.logger import logger


class PlannerAgent:
    """
    Research-grade Health-aware Planner Agent

    Responsibilities:
    - Decide high-level intent (diagnosis / conversation)
    - Prioritize safety-critical health conditions
    - Provide confidence score for RL & evaluation
    """

    def plan(self, perception_data: dict) -> dict:
        signals = perception_data.get("signals", {})

        temperature = signals.get("temperature")
        error_detected = signals.get("error_detected", False)
        severity_hint = signals.get("severity", "normal")
        noise = signals.get("noise", False)

        if noise:
            logger.warning("[Planner] Noisy input detected → conversation fallback")
            return {
                "intent": "conversation",
                "confidence": 0.4
            }

        if temperature is not None:
            if temperature >= 90:
                logger.info("[Planner] Critical temperature → diagnosis")
                return {
                    "intent": "diagnosis",
                    "confidence": 0.98
                }

            if temperature >= 75:
                logger.info("[Planner] Elevated temperature → diagnosis")
                return {
                    "intent": "diagnosis",
                    "confidence": 0.9
                }

        if error_detected:
            logger.info("[Planner] Error keyword detected → diagnosis")
            return {
                "intent": "diagnosis",
                "confidence": 0.85
            }

        if severity_hint in ["medium", "high"]:
            logger.info("[Planner] Severity hint elevated → diagnosis")
            return {
                "intent": "diagnosis",
                "confidence": 0.8
            }

        logger.info("[Planner] No health risk → conversation")
        return {
            "intent": "conversation",
            "confidence": 0.75
        }
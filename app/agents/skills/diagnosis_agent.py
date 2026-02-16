from typing import Dict
from app.core.logger import logger


class DiagnosisAgent:
    """
    Advanced Machine Health Diagnosis Agent

    Responsibilities:
    - Analyze structured health signals
    - Assess severity level
    - Decide operational safety
    - Recommend actions (shutdown / maintenance)
    """

    # Industry thresholds
    CRITICAL_TEMP = 95
    HIGH_TEMP = 90

    def execute(self, perception_data: Dict) -> Dict:
        signals = perception_data.get("signals", {})

        temperature = signals.get("temperature")
        error_detected = signals.get("error_detected")
        severity_hint = signals.get("severity_hint", "low")

        logger.info(
            f"[Diagnosis] Signals received | Temp={temperature}, Error={error_detected}, Hint={severity_hint}"
        )

        # Default outputs
        diagnosis = "System Normal"
        severity = "low"
        recommendation = "Continue normal operation"
        safe_to_operate = True

        if temperature and temperature >= self.CRITICAL_TEMP:
            diagnosis = "Critical Overheating Detected"
            severity = "critical"
            recommendation = (
                "Immediate shutdown required. Risk of permanent damage."
            )
            safe_to_operate = False

        elif temperature and temperature >= self.HIGH_TEMP and error_detected:
            diagnosis = "Severe System Fault with Overheating"
            severity = "high"
            recommendation = (
                "Emergency maintenance required. Stop operation immediately."
            )
            safe_to_operate = False

     
        elif error_detected:
            diagnosis = "System Error Detected"
            severity = "medium"
            recommendation = (
                "Maintenance recommended. Monitor system closely."
            )
            safe_to_operate = True

        result = {
            "status": "success",
            "response": diagnosis,
            "severity": severity,
            "temperature": temperature,
            "safe_to_operate": safe_to_operate,
            "recommendation": recommendation
        }

        logger.info(f"[Diagnosis] Final assessment: {result}")

        return result
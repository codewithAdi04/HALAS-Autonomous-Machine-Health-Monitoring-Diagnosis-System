class HealthEvaluator:
    """
    Evaluates health diagnosis quality
    Provides reward signal to RL
    """

    def evaluate(self, diagnosis_result: dict) -> float:
        severity = diagnosis_result.get("severity", "low")
        temperature = diagnosis_result.get("temperature", 0)

        if severity == "high" or (temperature and temperature > 90):
            return 1.0

        if severity == "medium":
            return 0.6

        return 0.2
import re
from typing import Dict, Optional


class TextModel:
    """
    Health Perception Layer (Research / Industry Grade)

    Responsibilities:
    - Clean & normalize input
    - Extract health-related signals
    - Detect ambiguity / noise
    - Provide structured perception output for downstream agents
    """

    def _extract_temperature(self, text: str) -> Optional[int]:
        """
        Extract temperature value from text (e.g. 95c, 95 C, 95°C)
        """
        match = re.search(r"(\d{2,3})\s?°?\s?c", text)
        if match:
            return int(match.group(1))
        return None

    def _detect_errors(self, text: str) -> bool:
        """
        Detect system error keywords
        """
        error_keywords = [
            "error", "failure", "critical",
            "overheat", "fault", "shutdown", "alarm"
        ]
        return any(word in text for word in error_keywords)

    def _detect_noise(self, text: str) -> bool:
        """
        Detect meaningless / noisy input (e.g. ????)
        """
        if len(text.strip()) < 3:
            return True

        if re.fullmatch(r"[^\w\s]+", text):
            return True

        return False

    def _estimate_severity(
        self,
        temperature: Optional[int],
        error_detected: bool
    ) -> str:
        """
        Severity estimation logic
        """
        if temperature is not None:
            if temperature >= 90:
                return "critical"
            elif temperature >= 75:
                return "warning"

        if error_detected:
            return "warning"

        return "normal"

    def process(self, text: str) -> Dict:
        """
        Main perception pipeline
        """

        normalized_text = text.lower().strip()

        # Noise detection
        is_noise = self._detect_noise(normalized_text)

        temperature = self._extract_temperature(normalized_text)
        error_detected = self._detect_errors(normalized_text)
        severity = self._estimate_severity(temperature, error_detected)

        return {
            "raw_text": text,
            "processed_text": normalized_text,
            "signals": {
                "temperature": temperature,
                "error_detected": error_detected,
                "severity": severity,
                "noise": is_noise
            }
        }
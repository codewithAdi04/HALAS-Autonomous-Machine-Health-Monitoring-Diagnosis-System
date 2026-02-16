import re
from typing import Dict


class HealthSignalExtractor:
    """
    Extract structured health signals from raw text input.
    """

    def extract(self, text: str) -> Dict:
        text = text.lower()

        signals = {
            "temperature": None,
            "error_detected": False,
            "critical_flag": False
        }

        # Temperature extraction (e.g., 95c)
        temp_match = re.search(r"(\d+)\s?c", text)
        if temp_match:
            signals["temperature"] = int(temp_match.group(1))

        # Error detection
        if any(word in text for word in ["error", "failure", "fault"]):
            signals["error_detected"] = True

        # Critical condition detection
        if any(word in text for word in ["critical", "overheat", "emergency"]):
            signals["critical_flag"] = True

        return signals
    
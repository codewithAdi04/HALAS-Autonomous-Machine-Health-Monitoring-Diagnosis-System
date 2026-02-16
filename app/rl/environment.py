class HALASEnvironment:

    def get_state(self, intent, confidence, latency):
        return f"{intent}_{round(confidence,2)}"

    def calculate_reward(self, result, latency, confidence):
        if result.get("status") != "success":
            return -0.5

        reward = 0.5

        if latency < 1.0:
            reward += 0.3

        reward += confidence * 0.2
        return reward
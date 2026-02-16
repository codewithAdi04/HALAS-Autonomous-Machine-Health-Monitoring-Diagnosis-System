import random
import json
import os
from collections import defaultdict
from app.config import settings
from app.core.logger import logger


class RLTrainer:
    """
    Industrial Q-Learning Trainer
    - Stable action selection
    - Safe persistence
    - Controlled epsilon decay
    """

    def __init__(self):

        self.alpha = settings.rl.learning_rate
        self.gamma = settings.rl.discount_factor
        self.epsilon = settings.rl.exploration_rate

        self.min_epsilon = 0.05
        self.epsilon_decay = 0.995

        self.q_table = defaultdict(lambda: defaultdict(float))
        self.q_file = "halas_q_table.json"

        self.load_q_table()


    # Action Selection
    def choose_action(self, state: str, actions: list) -> str:

        # Ensure all actions exist in Q-table
        for action in actions:
            if action not in self.q_table[state]:
                self.q_table[state][action] = 0.0

        # Exploration
        if random.random() < self.epsilon:
            action = random.choice(actions)
            logger.info(f"[RL] Exploration → {action}")
            return action

        # Exploitation (choose best among AVAILABLE actions only)
        best_action = max(
            actions,
            key=lambda a: self.q_table[state][a]
        )

        logger.info(f"[RL] Exploitation → {best_action}")
        return best_action


    # Q-Update
    def update(self, state: str, action: str, reward: float, next_state: str):

        old_value = self.q_table[state][action]

        next_max = max(
            self.q_table[next_state].values(),
            default=0
        )

        new_value = old_value + self.alpha * (
            reward + self.gamma * next_max - old_value
        )

        self.q_table[state][action] = new_value

        logger.info(
            f"[RL] Update | State: {state} | Action: {action} | "
            f"Old: {old_value:.4f} | New: {new_value:.4f}"
        )

        self.decay_epsilon()
        self.save_q_table()

    # Epsilon Decay
    def decay_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay

    # Persistence
    def save_q_table(self):
        serializable_q = {
            state: dict(actions)
            for state, actions in self.q_table.items()
        }

        with open(self.q_file, "w") as f:
            json.dump(serializable_q, f, indent=4)

    def load_q_table(self):
        if os.path.exists(self.q_file):
            with open(self.q_file, "r") as f:
                data = json.load(f)
                for state, actions in data.items():
                    for action, value in actions.items():
                        self.q_table[state][action] = value
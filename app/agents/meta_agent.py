import time

from app.perception.text_model import TextModel
from app.agents.planner_agent import PlannerAgent
from app.agents.skills.skill_router import SkillRouter
from app.core.logger import logger

from app.rl.environment import HALASEnvironment
from app.rl.trainer import RLTrainer
from app.evaluation.health_evaluator import HealthEvaluator


class MetaAgent:
    """
    HALAS MetaAgent
    Perception → Planning → (Rule + RL) → Skill → Learning
    """

    def __init__(self):
        self.text_model = TextModel()
        self.planner = PlannerAgent()
        self.router = SkillRouter()

        self.env = HALASEnvironment()
        self.rl_trainer = RLTrainer()
        self.health_evaluator = HealthEvaluator()

    def run(self, user_input: str) -> dict:
        logger.info(f"[HALAS] Input: {user_input}")
        start_time = time.time()

        try:
           
            perception_data = self.text_model.process(user_input)

            intent_data = self.planner.plan(perception_data)
            intent = intent_data.get("intent", "conversation")
            confidence = intent_data.get("confidence", 0.5)

        
            if intent == "diagnosis":
                logger.info("[MetaAgent] Diagnosis intent → bypass RL")
                action = "diagnosis"
                state = self.env.get_state(intent, confidence, 0.0)
            else:
                state = self.env.get_state(intent, confidence, 0.0)
                actions = list(self.router.skill_registry.keys())
                action = self.rl_trainer.choose_action(state, actions)

            
            result = self.router.route(action, perception_data)

            if not isinstance(result, dict):
                raise ValueError("Skill returned invalid output")

            latency = time.time() - start_time

            if intent == "diagnosis":
                reward = self.health_evaluator.evaluate(result)
            else:
                reward = self.env.calculate_reward(result, latency, confidence)

            next_state = self.env.get_state(intent, confidence, latency)

            if intent != "diagnosis":
                self.rl_trainer.update(state, action, reward, next_state)

            return {
                "response": result.get("response", "Processed"),
                "reward": reward,
                "latency": latency
            }

        except Exception as e:
            logger.exception("[HALAS] MetaAgent failed")
            return {
                "response": "HALAS encountered an internal error",
                "reward": 0.0,
                "latency": 0.0
            }
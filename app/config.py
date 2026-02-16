from dataclasses import dataclass
import os


@dataclass
class ModelConfig:
    llm_model_name: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 512


@dataclass
class PlannerConfig:
    diagnosis_threshold: float = 0.9
    default_confidence: float = 0.75


@dataclass
class RLConfig:
    learning_rate: float = 0.01
    discount_factor: float = 0.95
    exploration_rate: float = 0.1


@dataclass
class LoggingConfig:
    log_level: str = "INFO"
    log_file: str = "halas.log"


@dataclass
class SecurityConfig:
    secret_key: str = os.getenv("HALAS_SECRET_KEY", "dev-secret-key")
    token_expiry_minutes: int = 60


class Settings:
    """
    Central configuration object for HALAS.
    """

    def __init__(self):
        self.model = ModelConfig()
        self.planner = PlannerConfig()
        self.rl = RLConfig()
        self.logging = LoggingConfig()
        self.security = SecurityConfig()


# Global settings instance
settings = Settings()
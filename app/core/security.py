import hashlib
import hmac
import secrets
import time
from typing import Optional
from app.config import settings


class SecurityManager:
    """
    Core security utilities for HALAS system.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == hashed

    @staticmethod
    def generate_api_key() -> str:
        return secrets.token_hex(32)

    @staticmethod
    def generate_token(user_id: str) -> str:
        timestamp = str(int(time.time()))
        message = user_id + timestamp
        signature = hmac.new(
            settings.security.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        return f"{user_id}:{timestamp}:{signature}"

    @staticmethod
    def verify_token(token: str) -> bool:
        try:
            user_id, timestamp, signature = token.split(":")
            message = user_id + timestamp

            expected_signature = hmac.new(
                settings.security.secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_signature):
                return False

            # Token expiry check
            if int(time.time()) - int(timestamp) > settings.security.token_expiry_minutes * 60:
                return False

            return True

        except Exception:
            return False
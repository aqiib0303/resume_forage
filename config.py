import os

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB POST limit (form JSON)

CONFIG = BaseConfig
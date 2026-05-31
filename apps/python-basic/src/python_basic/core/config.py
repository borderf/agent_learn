from pathlib import Path
import logging
import os

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

# 尝试使用 python-dotenv 在创建 Settings 之前将 .env 加载到进程环境中，避免在 BaseSettings 中使用非注解类属性
env_path = Path(__file__).parent.parent.parent.parent / ".env"
try:
    from dotenv import load_dotenv

    if env_path.exists():
        # 强制用 .env 覆盖进程环境变量（如果你确实想优先使用 .env）
        try:
            load_dotenv(env_path, override=True)
            logger.info("Loaded .env from: %s (overriding existing env vars)", env_path)
        except TypeError:
            # 旧版本 python-dotenv 可能不支持 override 参数；回退到默认行为
            load_dotenv(env_path)
            logger.info(
                "Loaded .env from: %s (no override support in this dotenv version)",
                env_path,
            )
    else:
        logger.info(".env not found at: %s", env_path)
except Exception:
    logger.info("python-dotenv not available; relying on environment variables only")


class Settings(BaseSettings):
    openai_api_key: str
    openai_base_url: str = "https://api.deepseek.com"
    default_model: str = "deepseek-v4-flash"
    database_url: str = "mysql://root:123456@localhost:3306/ai_agent"


# 记录是否存在进程环境变量（会覆盖 .env）
if os.environ.get("OPENAI_API_KEY"):
    logger.info("Environment variable OPENAI_API_KEY is set (overrides .env)")
else:
    logger.info(
        "Environment variable OPENAI_API_KEY is not set; will read from .env if present"
    )

settings = Settings()
# 创建后记录已解析的 key（只显示前 8 个字符以避免泄露完整密钥）
if settings.openai_api_key:
    logger.info("Loaded OPENAI_API_KEY (masked): %s...", settings.openai_api_key[:8])
else:
    logger.warning("No OPENAI_API_KEY was loaded")

"""全局配置：从环境变量 / .env 读取，支持多环境切换。"""
import os

from dotenv import load_dotenv

load_dotenv()

# 多环境：dev / test / prod，默认 test
ENV = os.getenv("ENV", "test")

# 被测系统地址（默认用公开测试 API httpbin.org，无需密钥、无需自建服务即可跑通）
BASE_URL = os.getenv("BASE_URL", "https://httpbin.org")

# 请求超时（秒）
TIMEOUT = int(os.getenv("TIMEOUT", "10"))


class Context:
    """用例间共享上下文，典型用途：登录后存 token，后续接口自动携带。"""

    token: str | None = None


# 全局单例上下文
context = Context()

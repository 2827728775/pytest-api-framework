"""请求封装：自动拼接 base_url、统一超时、自动注入 token 鉴权。"""
import requests

from common.logger import logger
from config.settings import BASE_URL, TIMEOUT, context


class RequestsClient:
    """对 requests.Session 的轻封装，业务层只关心 method / path / 参数。"""

    def __init__(self) -> None:
        self.session = requests.Session()

    def send(self, method: str, path: str, **kwargs):
        url = f"{BASE_URL}{path}"

        # 若已登录拿到 token，自动带上鉴权头
        if context.token:
            headers = kwargs.get("headers") or {}
            headers["Authorization"] = f"Bearer {context.token}"
            kwargs["headers"] = headers

        kwargs.setdefault("timeout", TIMEOUT)

        logger.info("-> %s %s", method.upper(), url)
        resp = self.session.request(method, url, **kwargs)
        logger.info("<- %s", resp.status_code)
        return resp

"""pytest 全局配置：fixture 与公共钩子。"""
import pytest

from common.request import RequestsClient
from config.settings import context


@pytest.fixture(scope="session")
def client():
    """整个测试会话共用一个 HTTP 客户端（复用连接、会话级 token）。"""
    return RequestsClient()


@pytest.fixture(autouse=True)
def _reset_context():
    """每个用例前清空上下文，避免用例间 token 串味。"""
    context.token = None
    yield

"""接口用例示例：GET / POST / token 鉴权 / 状态码校验。"""
import allure

from api.demo_api import login, get_resource, bearer_call, status
from common.assert_utils import assert_status, assert_contains
from config.settings import context

# 模拟登录后由服务端下发的 token（真实项目从登录响应里取）
FAKE_TOKEN = "jwt.demo.token"


@allure.feature("接口示例")
class TestDemo:

    @allure.story("GET 请求正常返回")
    def test_get(self, client):
        resp = get_resource(client, "/get")
        assert_status(resp, 200)
        assert_contains(resp, "url")

    @allure.story("POST 请求回显请求体")
    def test_post_echo(self, client):
        resp = login(client, "student@example.com", "pwd123")
        assert_status(resp, 200)
        body = resp.json()
        assert body["json"]["email"] == "student@example.com"

    @allure.story("携带 token 访问鉴权接口")
    def test_bearer_auth(self, client):
        # 先模拟拿到 token 并存入上下文
        context.token = FAKE_TOKEN
        resp = bearer_call(client)
        assert_status(resp, 200)
        data = resp.json()
        assert data["authenticated"] is True
        assert data["token"] == FAKE_TOKEN

    @allure.story("未带 token 访问鉴权接口应 401")
    def test_bearer_no_token(self, client):
        # autouse fixture 已清空 context.token，这里直接调用即为未鉴权
        resp = bearer_call(client)
        assert_status(resp, 401)

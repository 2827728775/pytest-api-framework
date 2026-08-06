"""业务接口封装层：把"哪个接口、传什么"收口到一处，用例只调用语义化方法。
这里以公开测试服务 httpbin.org 为例，覆盖 GET / POST / 鉴权 / 状态码等典型场景。
"""
from common.request import RequestsClient


def login(client: RequestsClient, email: str, password: str):
    """模拟登录：httpbin 原样回显请求体，真实项目里这里通常返回 token。"""
    return client.send("POST", "/post", json={"email": email, "password": password})


def get_resource(client: RequestsClient, path: str = "/get"):
    """通用 GET 资源。"""
    return client.send("GET", path)


def bearer_call(client: RequestsClient):
    """需要鉴权的接口：httpbin /bearer 会校验 Authorization: Bearer <token> 并回显。"""
    return client.send("GET", "/bearer")


def status(client: RequestsClient, code: int):
    """指定状态码接口，常用于数据驱动校验（如 /status/200、/status/404）。
    allow_redirects=False：拿到真实状态码，避免 3xx 被 requests 自动跟随成 200。
    """
    return client.send("GET", f"/status/{code}", allow_redirects=False)

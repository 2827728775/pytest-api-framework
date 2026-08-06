"""断言封装：把常用校验收口，用例里只写一行。"""


def assert_status(resp, expected: int) -> None:
    assert resp.status_code == expected, (
        f"状态码期望 {expected}，实际 {resp.status_code}，body={resp.text}"
    )


def assert_field(resp, field: str, expected) -> None:
    body = resp.json()
    actual = body.get(field)
    assert actual == expected, f"字段 {field} 期望 {expected}，实际 {actual}"


def assert_contains(resp, field: str) -> None:
    body = resp.json()
    assert field in body, f"响应缺少字段 {field}，body={body}"


def assert_schema_has(resp, fields: list) -> None:
    body = resp.json()
    missing = [f for f in fields if f not in body]
    assert not missing, f"响应缺少字段 {missing}，body={body}"

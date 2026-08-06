"""Excel 数据驱动用例：与 test_data_driven.py 思路一致，只是数据源换成 Excel。
演示企业里最常见的"用例与代码分离"——测试同学维护 Excel，开发/测试开发只维护框架。
"""
import os

import pytest

from api.demo_api import status, bearer_call
from common.assert_utils import assert_status
from common.data_loader import load_excel
from config.settings import context

_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "user_cases.xlsx")
_cases = load_excel(_data_path, sheet="Sheet1")


@pytest.mark.parametrize("case", _cases, ids=lambda c: c["case_id"])
def test_excel_data_driven(client, case):
    scenario = str(case["scenario"]).strip().lower()

    if scenario == "status":
        code = int(case["expect_status"])
        resp = status(client, code)
        assert_status(resp, code)

    elif scenario == "auth":
        if str(case["token"]).strip().lower() == "yes":
            context.token = "fake-jwt-token-for-demo"   # 模拟登录后拿到的 token
            resp = bearer_call(client)
            assert_status(resp, 200)
        else:
            context.token = None                        # 不带 token
            resp = bearer_call(client)
            assert_status(resp, 401)

    else:
        pytest.fail(f"未知 scenario: {scenario}")

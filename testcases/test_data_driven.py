"""数据驱动用例：从 YAML 读取多组状态码，批量校验接口返回。"""
import os

import pytest

from api.demo_api import status
from common.assert_utils import assert_status
from common.data_loader import load_yaml

_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "status_cases.yaml")
_cases = load_yaml(_data_path)


@pytest.mark.parametrize("case", _cases, ids=lambda c: f"status={c['code']}")
def test_status_data_driven(client, case):
    resp = status(client, case["code"])
    assert_status(resp, case["expect_status"])

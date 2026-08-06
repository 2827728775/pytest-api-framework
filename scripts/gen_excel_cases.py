"""一次性脚本：生成 Excel 数据驱动用例文件 data/user_cases.xlsx。
列说明：
  case_id      用例编号
  scenario     status=状态码校验用例；auth=鉴权用例
  token        仅 auth 用例使用：yes=带 token 期望 200；no=不带 token 期望 401
  expect_status 期望的 HTTP 状态码
"""
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Sheet1"
ws.append(["case_id", "scenario", "token", "expect_status"])
ws.append(["C01", "status", "", "200"])
ws.append(["C02", "status", "", "404"])
ws.append(["C03", "auth", "yes", "200"])
ws.append(["C04", "auth", "no", "401"])

out = r"D:\新建文件夹\2026-08-04-10-25-04\pytest-api-framework\data\user_cases.xlsx"
wb.save(out)
print("saved:", out)

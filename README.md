# pytest 接口自动化测试框架（测开求职项目）

![API Tests](https://github.com/2827728775/pytest-api-framework/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![pytest](https://img.shields.io/badge/pytest-passing-brightgreen)

一个**能直接跑、能演示、能写进简历**的接口自动化测试框架脚手架，覆盖测试开发校招最看重的几项能力：
请求封装、token 鉴权、断言收口、数据驱动、Allure 报告、多环境配置。

> 默认对接公开测试服务 [httpbin.org](https://httpbin.org)，**无需密钥、无需自建服务即可运行**。

## 目录结构

```
pytest-api-framework/
├── config/            # 全局配置（多环境 / base_url / 上下文）
│   └── settings.py
├── common/            # 公共能力层
│   ├── request.py     #   请求封装（自动拼接 base_url + token 注入）
│   ├── assert_utils.py#   断言封装
│   ├── logger.py      #   日志
│   └── data_loader.py #   数据驱动（YAML / Excel）
├── api/               # 业务封装层（接口语义化方法）
│   └── demo_api.py
├── testcases/         # 测试用例层（pytest + parametrize）
│   ├── test_demo.py
│   ├── test_data_driven.py
│   └── test_excel_driven.py
├── data/              # 数据文件（用例与代码分离）
│   ├── status_cases.yaml
│   └── user_cases.xlsx
├── scripts/           # 工具脚本（如生成 Excel 用例）
│   └── gen_excel_cases.py
├── .github/workflows/ # CI：push/PR 自动跑测试 + 出报告
│   └── ci.yml
├── reports/           # Allure 结果（git 忽略）
├── conftest.py        # fixture / 钩子
├── pytest.ini
├── requirements.txt
└── .env.example
```

## 快速开始

```bash
# 1. 准备虚拟环境（推荐）
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置（可选，默认已指向 httpbin.org）
cp .env.example .env

# 4. 运行
pytest

# 5. 查看 Allure 报告（需另装 allure 命令行）
pytest            # 先生成 reports/allure-results
allure serve reports/allure-results
```

## 数据驱动：YAML 与 Excel 两种来源

用例与数据分离，改数据即加用例，**不用动代码**。框架在 `common/data_loader.py` 同时支持两种格式，`load()` 按扩展名自动识别。

**YAML（`data/status_cases.yaml`）**——适合开发/测试开发维护：

```python
from common.data_loader import load_yaml
cases = load_yaml("data/status_cases.yaml")
```

**Excel（`data/user_cases.xlsx`，Sheet1）**——适合测试同学维护，企业里最常见：

```python
from common.data_loader import load_excel
cases = load_excel("data/user_cases.xlsx", sheet="Sheet1")  # 首行表头，其余行转 dict 列表
```

列设计（`user_cases.xlsx`）：`case_id` / `scenario`(status|auth) / `token`(yes|no) / `expect_status`。
需要改用例？直接在 Excel 里增删行、改期望值，重跑 `pytest` 即可，代码一行不用动。

> 生成示例 Excel 见 `scripts/gen_excel_cases.py`（`python scripts/gen_excel_cases.py`）。

## CI 自动化（GitHub Actions）

`.github/workflows/ci.yml` 已配好：**push 到 main/master 或提 PR 时自动**安装依赖 → 跑 pytest → 生成 Allure 报告 → 把报告作为产物（artifact）上传。

- 跑完在仓库 `Actions` 标签页点进本次运行，右侧 `Artifacts` 里下载 `allure-report`，本地双击 `index.html` 即可看可视化报告；`allure-results` 也可用 `allure serve` 打开。
- 想让报告**直接有在线链接**？在仓库 `Settings → Pages` 把 Source 设为 `GitHub Actions`，并把上面的上传产物步骤换成官方的 Pages 部署步骤即可（本报告已生成静态 HTML，部署零改造）。

## 设计要点（面试能讲的点）

- **分层**：用例只调语义化方法（如 `bearer_call(...)`），接口地址/参数收口在 `api/`，通用能力在 `common/`。
- **鉴权上下文**：登录后 token 存入 `Context`，后续请求自动带 `Authorization` 头，模拟真实鉴权链路。
- **数据驱动**：用例与数据分离，YAML/Excel 改数据即加用例，不用动代码。
- **可观测**：统一日志 + Allure 报告 + `--alluredir` 持续产出。

## 进阶路线（9 月后加 AI 增强）

- 用大模型根据 OpenAPI 文档 / 需求自动生成测试用例（填充 `data/`）。
- 失败日志智能归因：把 Allure 失败用例的 traceback 喂给模型，给出可能原因与复现建议。
- GitHub Actions 已接好（见上）：push 即跑，报告自动上传产物。

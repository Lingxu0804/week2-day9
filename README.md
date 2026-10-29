
# Week 2 Day 9–10：FastAPI + Pydantic 计算器

这是一个用于学习 FastAPI、Pydantic、HTTP 请求处理和 pytest 自动化测试的 Python 项目。

## 技术栈

- Python 3.12+
- uv：Python 项目与依赖管理
- FastAPI：构建 HTTP API
- Pydantic：请求数据验证与响应模型
- pytest、HTTPX：自动化接口测试

## 环境配置

在项目根目录运行：

```powershell
uv sync --dev
```

## 启动 API

推荐使用 Uvicorn 启动开发服务器：

```powershell
uv run uvicorn week2_day9.main:app --reload
```

也可以使用项目命令：

```powershell
uv run week2-day9
```

启动后访问：

http://127.0.0.1:8000/docs

通过 Swagger UI 查看接口并发送测试请求。

## API 接口

### POST /calculate

请求体示例：

```json
{
  "a": 10,
  "b": 2,
  "operation": "divide"
}
```

支持的运算：

- `add`：加法
- `multiply`：乘法
- `divide`：除法

请求模型限制 `a` 和 `b` 的范围为 -10000 至 10000。`operation` 默认值为 `add`。

成功响应包含 `id`、`input`、`result` 和 `message`。响应模型会过滤未声明的额外字段。

### GET /calculations/{record_id}

查询已有计算记录。

例如：

```text
GET /calculations/1?verbose=true
```

`record_id` 必须大于等于 1。`verbose` 默认为 `false`，设置为 `true` 时会返回详细说明。

## HTTP 状态码

| 状态码 | 含义 |
|---|---|
| 200 | 请求成功 |
| 400 | 除法运算的除数为零 |
| 404 | 计算记录不存在 |
| 422 | 请求参数或请求模型验证失败 |

## 运行测试

在项目根目录执行：

```powershell
uv run pytest -q
```

当前测试覆盖正常计算、输入验证失败、除零、缺少必填字段和记录不存在等场景。

## 项目结构

```text
week2-day9/
├── src/
│   ├── week2_day9/
│   │   ├── __init__.py
│   │   └── main.py
│   └── day9_review.py
├── tests/
│   └── test_main.py
├── .gitignore
├── pyproject.toml
├── README.md
└── uv.lock
```

## 当前限制

计算记录保存在 Python 进程的内存字典中，服务重启后记录会清空。本项目用于学习 API 设计、请求验证和自动化测试，尚未接入数据库或身份认证。

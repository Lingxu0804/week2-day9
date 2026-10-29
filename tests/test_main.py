
import pytest
from fastapi.testclient import TestClient

from week2_day9.main import app, records


# 创建测试客户端
client = TestClient(app)


# 每个测试开始前和结束后清理内存记录
@pytest.fixture(autouse=True)
def reset_records():
    records.clear()
    yield
    records.clear()


# 测试1：正常计算，并检查响应模型过滤
def test_calculate_success():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "b": 2,
            "operation": "divide"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["result"] == 5.0
    assert data["input"]["operation"] == "divide"
    assert data["message"] == "计算成功"
    assert "internal_note" not in data


# 测试2：字段超出范围，返回422
def test_out_of_range_returns_422():
    response = client.post(
        "/calculate",
        json={
            "a": 20000,
            "b": 2,
            "operation": "add"
        }
    )

    assert response.status_code == 422


# 测试3：除数为零，返回400
def test_divide_by_zero_returns_400():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "b": 0,
            "operation": "divide"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "除数不能为0"


# 测试4：缺少必填字段b，返回422
def test_missing_field_returns_422():
    response = client.post(
        "/calculate",
        json={
            "a": 10,
            "operation": "add"
        }
    )

    assert response.status_code == 422


# 测试5：记录不存在，返回404
def test_missing_record_returns_404():
    response = client.get("/calculations/99")

    assert response.status_code == 404
    assert response.json()["detail"] == "计算记录不存在"


from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="Day 9 Pydantic Calculator",
    description="使用 Pydantic 验证 API 请求数据",
    version="0.1.0",
)


# 1. 定义请求数据模型
class CalculationRequest(BaseModel):

    a: float = Field(
        ge=-10000,
        le=10000,
        description="第一个数字",
    )

    b: float = Field(
        ge=-10000,
        le=10000,
        description="第二个数字",
    )

    operation: Literal[
        "add", "multiply", "divide"
    ] = "add"


# 2. 定义计算接口
@app.post("/calculate")
def calculate(data: CalculationRequest):

    if data.operation == "add":
        result = data.a + data.b

    elif data.operation == "multiply":
        result = data.a * data.b

    elif data.operation == "divide":

        if data.b == 0:
            raise HTTPException(
                status_code=400,
                detail="除数不能为0",
            )

        result = data.a / data.b

    return {
        "input": data.model_dump(),
        "result": result,
    }


# 3. 健康检查
@app.get("/health")
def health():
    return {"status": "ok"}

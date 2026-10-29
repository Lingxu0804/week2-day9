
from typing import Literal

from fastapi import (
    FastAPI,
    HTTPException,
    Path,
    Query,
    Body,
)
from pydantic import BaseModel, Field


# ========== 模块1：创建 FastAPI 应用 ==========

app = FastAPI(title="Day10 计算器 API")


# ========== 模块2：定义输入模型 ==========

class CalculationRequest(BaseModel):

    a: float = Field(ge=-10000, le=10000)

    b: float = Field(ge=-10000, le=10000)

    operation: Literal[
        "add", "multiply", "divide"
    ] = "add"


# ========== 模块3：定义输出模型 ==========

class CalculationResponse(BaseModel):

    id: int

    input: CalculationRequest

    result: float

    message: str


# ========== 模块4：临时存储计算记录 ==========

records: dict[int, dict] = {}


# ========== 模块5：计算函数 ==========

def calculate_result(data: CalculationRequest) -> float:

    if data.operation == "add":
        return data.a + data.b

    if data.operation == "multiply":
        return data.a * data.b

    if data.b == 0:
        raise HTTPException(
            status_code=400,
            detail="除数不能为0"
        )

    return data.a / data.b


# ========== 模块6：POST 创建计算记录 ==========

@app.post(
    "/calculate",
    response_model=CalculationResponse
)
def calculate(
    data: CalculationRequest = Body(...)
):

    result = calculate_result(data)

    record_id = len(records) + 1

    record = {
        "id": record_id,
        "input": data.model_dump(),
        "result": result,
        "message": "计算成功"
    }

    records[record_id] = record

    return {
        **record,
        "internal_note": "演示响应模型的字段过滤"
    }


# ========== 模块7：GET 查询计算记录 ==========

@app.get(
    "/calculations/{record_id}",
    response_model=CalculationResponse
)
def get_calculation(
    record_id: int = Path(
        ge=1,
        description="计算记录ID，最小为1"
    ),
    verbose: bool = Query(
        default=False,
        description="是否显示详细说明"
    )
):

    if record_id not in records:
        raise HTTPException(
            status_code=404,
            detail="计算记录不存在"
        )

    record = records[record_id].copy()

    if verbose:
        record["message"] = (
            f"已找到编号为 {record_id} 的计算记录"
        )

    return record

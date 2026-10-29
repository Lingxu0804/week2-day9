from typing import Literal
from pydantic import BaseModel, Field, ValidationError


class TaskInput(BaseModel):
    prompt: str = Field(..., min_length=3)
    retries: int = Field(default=2, ge=0)
    priority: Literal["low", "high"] = "low"


# 实验一：正常输入
task1 = TaskInput(
    prompt="查询北京天气",
    priority="high"
)

print("实验一：", task1)
print("任务内容：", task1.prompt)
print("重试次数：", task1.retries)


# 实验二：查看类型
print("实验二：", type(task1))
print("是否为模型实例：", isinstance(task1, TaskInput))


# 实验三：转换为字典和 JSON
data = task1.model_dump()
json_text = task1.model_dump_json()

print("字典：", data)
print("字典类型：", type(data))
print("JSON：", json_text)
print("JSON类型：", type(json_text))


# 实验四：允许的类型转换
task2 = TaskInput(
    prompt="查询上海天气",
    retries="3"
)

print("实验四：", task2.retries)
print("转换后类型：", type(task2.retries))


# 实验五：异常输入
try:
    task3 = TaskInput(
        prompt="查",
        retries=-1,
        priority="urgent"
    )
except ValidationError as error:
    print("实验五：验证失败")
    print(error.errors())
# 模型
# 1.ORM模型
# 2. Pydantic模型: Schema

from pydantic import BaseModel
from datetime import datetime
from typing import List  # noqa: UP035

# 定义响应数据列表模型
class ApiResponseDataList(BaseModel):
    total: int | None
    list: List[dict] = []
    page: int | None
    limit: int | None

# 定义响应模型
class ApiResponse(BaseModel):
    code: int
    message: str
    data: ApiResponseDataList = {}


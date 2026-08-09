# 模型
# 1.ORM模型
# 2. Pydantic模型: Schema

from pydantic import BaseModel
from datetime import datetime
from typing import List  # noqa: UP035

# 定义响应数据列表模型
class ApiResponse(BaseModel):
    total: int | None
    list: List
    page: int | None
    limit: int | None

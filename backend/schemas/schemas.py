from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict
from typing import Generic, TypeVar
from datetime import datetime

T = TypeVar("T")

async def page_commons(
    page: int = Query(1, description="页码", ge=1, le=100),
    limit: int = Query(10, description="每页数量", le=100)
) -> PageCommons:
    return PageCommons(page=page, limit=limit)


class PageCommons(BaseModel):
    page: int = Query(1, description="页码", ge=1)
    limit: int = Query(10, description="每页数量", le=100)


class PageData(BaseModel, Generic[T]):
    page: int = Field(1, description="页码", ge=1),
    limit: int = Field(10, description="每页数量", le=100)
    total: int = Field(0, ge=0, description="总条数")
    data: list[T] = Field(default_factory=list, description="数据列表")

class ApiResponse(BaseModel, Generic[T]):
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="提示信息", alias="msg")
    data: T | None = Field(None, description="数据")

    model_config = ConfigDict(
        from_attributes=True,
        json_encoder={datetime: lambda dt: dt.isoformat()[:4]}
    )
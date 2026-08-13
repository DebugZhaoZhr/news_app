from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List
from schemas.news_response import NewsItem

class HistoryRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    
# 定义历史记录 响应数据模型
class HistoryResponse(BaseModel):
    id: int = Field(..., description="历史记录ID")
    user_id: int = Field(..., alias="userId", description="用户ID")
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    created_at: datetime = Field(..., alias="createdAt", description="创建时间")
    updated_at: datetime = Field(..., alias="updatedAt", description="更新时间")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# 定义历史记录项 请求数据模型
class HistoryItemRequest(NewsItem):
    view_time: datetime = Field(..., alias="viewTime", description="查看时间")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

# 定义收藏列表 响应数据模型
class HistoryListResponse(BaseModel):
    list: List[HistoryItemRequest] = Field(..., alias="list", description="收藏列表")
    page: int = Field(..., description="页码")
    limit: int = Field(..., description="每页数量")
    total: int = Field(..., description="总条数")
    has_more: bool = Field(..., description="是否有更多数据", alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
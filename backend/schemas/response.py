# 模型
# 1.ORM模型
# 2. Pydantic模型: Schema

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List



# 定义分类 响应数据模型
class CategoryResponse(BaseModel):
    id: int = Field(..., description="分类ID")
    name: str = Field(..., description="分类名称")
    sort_order: int = Field(..., description="排序顺序")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)

# 定义分类列表 响应数据模型
class CategoryListResponse(BaseModel):
    page: int = Field(..., description="页码")
    limit: int = Field(..., description="每页数量")
    total: int = Field(..., description="总条数")
    list: List[CategoryResponse] = Field(default_factory=list, description="分类列表")

    model_config = ConfigDict(from_attributes=True)


# 定义新闻 响应数据模型
class NewsItem(BaseModel):
    id: int = Field(..., description="新闻ID")
    title: str = Field(..., description="新闻标题")
    description: str = Field(..., description="新闻描述")
    image: str = Field(..., description="新闻图片")
    author: str = Field(..., description="作者名称")
    views: int = Field(..., description="浏览量")
    category_id: int | None = Field(None, description="分类ID", alias="categoryId")
    publish_time: datetime = Field(..., description="发布时间", alias="publishTime")
    created_at: datetime = Field(..., description="创建时间", alias="createdAt")
    updated_at: datetime = Field(..., description="更新时间", alias="updatedAt")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


# 定义新闻详情 响应数据模型
class NewsDetailItem(NewsItem):
    content: str = Field(..., description="新闻内容")
    related_news: List[NewsItem] = Field(default_factory=list, description="相关新闻")
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


# 定义新闻列表 响应数据模型
class NewsListResponse(BaseModel):
    page: int = Field(..., description="页码")
    limit: int = Field(..., description="每页数量")
    total: int = Field(..., description="总条数")
    list: List[NewsItem] = Field(default_factory=list, description="新闻列表")
    has_more: bool = Field(..., description="是否有更多数据", alias="hasMore")
    category: int | None = Field(None, description="分类ID", alias="categoryId")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    

from fastapi import HTTPException
from sqlalchemy import select, delete

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from schemas.schemas import PageCommons, page_commons
from schemas.favorite import FavoriteItemRequest, FavoriteListResponse, IsFavoriteResponse
from models.favorite import Favorite
from models.news import News



# 检查用户是否收藏了新闻
async def check_favorite_crud(
    session: AsyncSession,
    user_id: int,
    news_id: int,
) -> bool:

    # 检查用户是否收藏了新闻
    favorite = await session.scalar(
        select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    )
    return IsFavoriteResponse(is_favorite=favorite is not None)


# 新增收藏记录
async def add_favorite_crud(
    session: AsyncSession,
    user_id: int,
    news_id: int,
) -> str:
    
    favorite = await session.scalar(
        select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    )
    if favorite:
        raise HTTPException(status_code=400, detail="新闻已被收藏")
    # 新增收藏记录
    favorite = Favorite(
        user_id=user_id,
        news_id=news_id,
    )
    session.add(favorite)
    await session.flush()
    
    return '收藏成功'


# 删除收藏记录
async def delete_favorite_crud(
    session: AsyncSession,
    user_id: int,
    news_id: int,
) -> str:
    
    #删除用户收藏
    favorite = await session.scalar(
        select(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id)
    )
    if not favorite:
        raise HTTPException(status_code=404, detail="收藏记录不存在")

    await session.delete(favorite)
    await session.flush()
    

    return '取消收藏成功'

# 获取收藏列表
async def get_favorite_list_crud(
    session: AsyncSession,
    user_id: int,
    page_commons: PageCommons,
) -> FavoriteListResponse[FavoriteItemRequest]:
    
    skip = (page_commons.page - 1) * page_commons.limit

    sub_query = select(Favorite.news_id, Favorite.created_at).where(Favorite.user_id == user_id).subquery()

    stmt = (
        select(News, sub_query.c.created_at.label("favorite_time"))
        .join(sub_query, News.id == sub_query.c.news_id)
        .order_by(sub_query.c.created_at.desc())
        .offset(skip)
        .limit(page_commons.limit)
    )
    total = await session.scalar(select(func.count(Favorite.id)).where(Favorite.user_id == user_id))
    results = (await session.execute(stmt)).all()

    items = [FavoriteItemRequest.model_validate({
        **news.__dict__,
        'favorite_time': favorite_time
    }) for news, favorite_time in results]
    
    return FavoriteListResponse(
        list=items,
        total=total,
        page=page_commons.page,
        limit=page_commons.limit,
        has_more=len(results) >= page_commons.limit,
    )


# 删除所有收藏记录
async def delete_favorite_list_crud(
    session: AsyncSession,
    user_id: int,
) -> str:
    
    # 删除用户所有收藏记录
    await session.execute(
        delete(Favorite).where(Favorite.user_id == user_id)
    )
    await session.flush()
    
    return '清除收藏列表成功'
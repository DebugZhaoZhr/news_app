from fastapi import HTTPException
from sqlalchemy import select, delete

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from schemas.schemas import PageCommons, page_commons
from schemas.history import HistoryItemRequest, HistoryListResponse
from models.history import History
from models.news import News

from datetime import datetime

# 新增历史记录
async def add_history_crud(
    session: AsyncSession,
    user_id: int,
    news_id: int,
) -> str:
    
    history = await session.scalar(
        select(History).where(History.user_id == user_id, History.news_id == news_id)
    )
    if history:
        history.view_time = datetime.now()
        await session.flush()
        return '已更新历史记录'
    else:
        # 新增历史记录
        history = History(
            user_id=user_id,
            news_id=news_id,
        )
        session.add(history)
        await session.flush()
    
    return '已加入历史记录'


# 删除历史记录
async def delete_history_crud(
    session: AsyncSession,
    user_id: int,
    news_id: int,
) -> str:
    
    #删除用户历史记录
    history = await session.scalar(
        select(History).where(History.news_id == news_id, History.user_id == user_id)
    )
    if not history:
        raise HTTPException(status_code=404, detail="历史记录不存在")

    await session.delete(history)
    await session.flush()
    
    return '删除历史记录成功'


# 获取历史记录列表
async def get_history_list_crud(
    session: AsyncSession,
    user_id: int,
    page_commons: PageCommons,
) -> HistoryListResponse[HistoryItemRequest]:
    
    skip = (page_commons.page - 1) * page_commons.limit

    sub_query = select(History.news_id, History.view_time).where(History.user_id == user_id).subquery()

    stmt = (
        select(News, sub_query.c.view_time)
        .join(sub_query, News.id == sub_query.c.news_id)
        .order_by(sub_query.c.view_time.desc())
        .offset(skip)
        .limit(page_commons.limit)
    )
    results = (await session.execute(stmt)).all()

    list = [HistoryItemRequest.model_validate({
        **news.__dict__,
        'view_time': view_time
    }) for news, view_time in results]

    
    total = await session.scalar(
        select(func.count(History.id)).where(History.user_id == user_id)
    )
    
    return HistoryListResponse(
        list=list,
        total=total,
        page=page_commons.page,
        limit=page_commons.limit,
        has_more=len(results) >= page_commons.limit,
    )


# 删除所有历史记录
async def delete_history_list_crud(
    session: AsyncSession,
    user_id: int,
) -> str:
    
    # 删除用户所有历史记录
    await session.execute(
        delete(History).where(History.user_id == user_id)
    )
    await session.flush()
    
    return '清除历史记录列表成功'

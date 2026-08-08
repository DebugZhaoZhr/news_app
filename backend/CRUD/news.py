from models.news import Category, News
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from random import randint


async def get_categories(
    # page_commons: dict = Depends(page_commons),
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
) -> list[Category]:
    skip = (page - 1) * limit
    stmt = select(Category).offset(skip).limit(limit)
    categories = (await session.scalars(stmt)).all()
    
    return categories

async def get_news_list(
    # page_commons: dict = Depends(page_commons),
    session: AsyncSession,
    category_id: int | None = None,
    page: int = 1,
    limit: int = 10,
) -> list[News]:

    skip = (page - 1) * limit
    if category_id is not None:
        stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
        count_stmt = select(func.count(News.id)).where(News.category_id == category_id)
    else:
        stmt = select(News).offset(skip).limit(limit)
        count_stmt = select(func.count(News.id))
    total = await session.scalar(count_stmt)
    news = (await session.scalars(stmt)).all()
    
    
    return {'news': news, 'total': total, 'has_more': total > skip + limit}
    
async def get_news_detail(
    session: AsyncSession,
    news_id: int
) -> News:
    news = await session.get(News, news_id)
    return news

async def increase_view_count(
    session: AsyncSession,
    news_id: int
) -> None:

    # 方法1 直接更新数据库
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

    # # 方法2 先查询 再更新
    # news = await session.get(News, news_id)
    # news.views += 1
    # await session.commit()
    # return news

async def get_related_news(
    session: AsyncSession,
    news_id: int,
    category_id: int
) -> list[News]:

    stmt = select(News).where(
        News.id != news_id,
        News.category_id == category_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(5)
    result = (await session.scalars(stmt)).all()

    # 列表推导式 转换为字典列表
    # result = [News]
    return result

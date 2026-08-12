from models.news import Category, News
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from random import randint
from schemas.news_response import CategoryListResponse, NewsItem, NewsDetailItem, NewsListResponse


async def get_categories(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
) -> CategoryListResponse:
    async with session.begin():
        skip = (page - 1) * limit
        stmt = select(Category).offset(skip).limit(limit)
        categories = (await session.scalars(stmt)).all()
        
        count_stmt = select(func.count(Category.id))
        total = await session.scalar(count_stmt)

    return CategoryListResponse(
        page=page,
        limit=limit,
        total=total,
        list=categories
    )
    

async def get_news_list(
    session: AsyncSession,
    category_id: int | None = None,
    page: int = 1,
    limit: int = 10,
) -> NewsListResponse:

    # async with session.begin():
    skip = (page - 1) * limit
    if category_id is not None:
        stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
        count_stmt = select(func.count(News.id)).where(News.category_id == category_id)
    else:
        stmt = select(News).offset(skip).limit(limit)
        count_stmt = select(func.count(News.id))
    total = await session.scalar(count_stmt)
    news = (await session.scalars(stmt)).all()
    await session.flush()
    
    return NewsListResponse(
        page=page,
        limit=limit,
        total=total,
        list=news,
        has_more=total > skip + limit,
        category=category_id
    )
    # return {'news': news, 'total': total, 'has_more': total > skip + limit}
    
    
async def get_news_detail(
    session: AsyncSession,
    news_id: int
) -> NewsDetailItem:
    # async with session.begin():
    news = await session.get(News, news_id)
    if not news:
        return None
    await session.flush()
    return NewsDetailItem.model_validate(news)


async def increase_view_count(
    session: AsyncSession,
    news_id: int
) -> None:
    # async with session.begin():
    # 方法1 直接更新数据库
    # stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    # result = await session.execute(stmt)
    # # 方法2 先查询 再更新
    news = await session.get(News, news_id)
    if not news:
        return None
    news.views += 1
    await session.flush()
    return news
    # return result.rowcount > 0


async def get_related_news(
    session: AsyncSession,
    news_id: int,
    category_id: int
) -> list[NewsItem]:
    # async with session.begin():
    stmt = select(News).where(
        News.id != news_id,
        News.category_id == category_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(5)
    result = (await session.scalars(stmt)).all()
    await session.flush()

    return [NewsItem.model_validate(item) for item in result]

from models.news import Category, News
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func


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
    category_id: int,
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
   ) -> list[News]:
   
    skip = (page - 1) * limit

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    count_stmt = select(func.count(News.id)).where(News.category_id == category_id)
    total = await session.scalar(count_stmt)
    news = (await session.scalars(stmt)).all()
    
    
    return {'news': news, 'total': total}
from models.news import Category, News
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from random import randint
from schemas.news_response import CategoryListResponse, NewsItem, NewsDetailItem, NewsListResponse
from cache.news_cache import get_cached_categories, set_cached_categories, get_cached_news_list, set_cached_news_list
from fastapi.encoders import jsonable_encoder



# 获取新闻分类列表
async def get_categories(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
) -> CategoryListResponse:

    # 从缓存中获取分类列表
    cached_categories = await get_cached_categories()
    if cached_categories is not None:
        return CategoryListResponse(
            page=page,
            limit=limit,
            total=len(cached_categories),
            list=cached_categories
        )
    
    skip = (page - 1) * limit
    stmt = select(Category).offset(skip).limit(limit)
    categories = (await session.scalars(stmt)).all()

    count_stmt = select(func.count(Category.id))
    total = await session.scalar(count_stmt)

    if categories:
        # 转换为JSON可序列化格式
        categories_data = jsonable_encoder(categories)
        # 缓存分类列表
        ok = await set_cached_categories(categories_data)
        if not ok:
            print('缓存分类列表失败, 请检查 Redis 配置')
    else:
        categories_data = []
    return CategoryListResponse(
        page=page,
        limit=limit,
        total=total,
        list=categories_data
    )
    
# 获取新闻列表
async def get_news_list(
    session: AsyncSession,
    category_id: int | None = None,
    page: int = 1,
    limit: int = 10,
) -> NewsListResponse:

    skip = (page - 1) * limit
    
    # 从缓存中获取新闻列表
    cached_news = await get_cached_news_list(category_id, page, limit)
    if cached_news is not None:
        return NewsListResponse(
            page=page,
            limit=limit,
            total=cached_news['total'],
            list=cached_news['list'],
            has_more=cached_news['total'] > skip + limit,
            category=category_id
        )

    if category_id is not None:
        stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
        count_stmt = select(func.count(News.id)).where(News.category_id == category_id)
    else:
        stmt = select(News).offset(skip).limit(limit)
        count_stmt = select(func.count(News.id))
    total = await session.scalar(count_stmt)
    news = (await session.scalars(stmt)).all()
    await session.flush()

    if news:
        # 转换为JSON可序列化格式
        news_data = jsonable_encoder(news)
        # 缓存新闻列表
        ok = await set_cached_news_list(category_id, page, limit, total, news_data)
        if not ok:
            print('缓存新闻列表失败, 请检查 Redis 配置')
    
    return NewsListResponse(
        page=page,
        limit=limit,
        total=total,
        list=news,
        has_more=total > skip + limit,
        category=category_id
    )
    # return {'news': news, 'total': total, 'has_more': total > skip + limit}
    
    
# 获取新闻详情
async def get_news_detail(
    session: AsyncSession,
    news_id: int
) -> NewsDetailItem:

    news = await session.get(News, news_id)
    if not news:
        return None
    await session.flush()
    return NewsDetailItem.model_validate(news)

# 增加新闻点击量
async def increase_view_count(
    session: AsyncSession,
    news_id: int
) -> None:

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

# 获取相关新闻
async def get_related_news(
    session: AsyncSession,
    news_id: int,
    category_id: int
) -> list[NewsItem]:

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

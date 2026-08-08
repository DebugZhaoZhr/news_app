from config.db_conf import get_session
from CRUD.news import get_categories as get_categories_crud
from CRUD.news import get_news_list as get_news_list_crud
from fastapi import APIRouter, Depends, Query
from schemas.schemas import page_commons
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/api/news', tags=['news'])

@router.get('/categories')
async def get_categories(
    page_commons: dict = Depends(page_commons),
    session: AsyncSession = Depends(get_session)
):
    categories = await get_categories_crud(
        session=session, page=page_commons['page'], limit=page_commons['limit'])
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": {
            # "total": len(categories),
            "data": categories,
            "page": page_commons['page'],
            "limit": page_commons['limit'],
        }
    }

@router.get('/list')
async def get_news_list(
    category_id: int = Query(alias='categoryId'),
    page_commons: dict = Depends(page_commons),
    session: AsyncSession = Depends(get_session),
):
    response = await get_news_list_crud(
        session=session,
        page=page_commons['page'],
        limit=page_commons['limit'],
        category_id=category_id
    )
    total = response['total']
    news = response['news']
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "total": total,
            "category": category_id,
            "list": news,
            "page": page_commons['page'],
            "limit": page_commons['limit'],
            "hasMore": True,
        }
    }
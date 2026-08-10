from typing import Any


from config.db_conf import get_session
from CRUD.news import get_categories as get_categories_crud
from CRUD.news import get_news_list as get_news_list_crud
from CRUD.news import get_news_detail as get_news_detail_crud
from CRUD.news import increase_view_count, get_related_news

from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.news_response import NewsListResponse, CategoryListResponse, NewsDetailItem
from schemas.schemas import page_commons, PageCommons, ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/api/news', tags=['news'])

@router.get('/categories')
async def get_categories(
    page_commons: PageCommons = Depends(page_commons),
    session: AsyncSession = Depends(get_session)
):
    categories = await get_categories_crud(
        session=session,
        page=page_commons.page,
        limit=page_commons.limit
    )

    return ApiResponse[CategoryListResponse](msg="获取新闻分类成功", data=categories)


@router.get('/list')
async def get_news_list(
    category_id: int | None = Query(None, alias='categoryId', description='分类ID（可选）'),
    page_commons: PageCommons = Depends(page_commons),
    session: AsyncSession = Depends(get_session),
):
    response = await get_news_list_crud(
        session=session,
        page=page_commons.page,
        limit=page_commons.limit,
        category_id=category_id,
    )
    data = NewsListResponse(
        page=page_commons.page,
        limit=page_commons.limit,
        total=response.total,
        list=response.list,
        has_more=response.has_more,
        category=category_id,
    )
    return ApiResponse[NewsListResponse](msg="获取新闻列表成功", data=data)

@router.get('/detail')
async def get_news_detail_curd(
    news_id: int = Query(alias='id', description='新闻ID'),
    session: AsyncSession = Depends(get_session),
):
    response = await get_news_detail_crud(
        session=session,
        news_id=news_id,
    )
    if not response:
        raise HTTPException(status_code=404, detail="新闻不存在")
    # else:


    views_res = await increase_view_count(session, news_id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")
    

    related_news = await get_related_news(session, news_id, response.category_id)
    
    
    response.related_news = related_news
    return ApiResponse[NewsDetailItem](msg="获取新闻详情成功", data=response)
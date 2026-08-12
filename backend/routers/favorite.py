
from config.db_conf import get_session
from schemas.favorite import IsFavoriteResponse, FavoriteRequest

from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.schemas import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserInfoResponse
from schemas.favorite import FavoriteListResponse
from CRUD.auth import verify_token
from CRUD.favorite import check_favorite_crud, add_favorite_crud, delete_favorite_crud, get_favorite_list_crud, delete_favorite_list_crud
from schemas.schemas import PageCommons, page_commons


router = APIRouter(prefix='/api/favorite', tags=['favorite'])

# 检查用户是否收藏了新闻
@router.get('/check')
async def check_favorite(
    news_id: int = Query(..., alias='newsId', description='新闻ID'),
    session: AsyncSession = Depends(get_session),
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse[IsFavoriteResponse]:

    async with session.begin():
        response = await check_favorite_crud(
            session=session,
            user_id=current_user.id,
            news_id=news_id,
        )
    return ApiResponse[IsFavoriteResponse](msg="新闻已被收藏" if response.is_favorite else "新闻未被收藏", data=response) 
    

# 收藏新闻
@router.post('/add')
async def add_favorite(
    favorite_request: FavoriteRequest,
    session: AsyncSession = Depends(get_session),    
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        msg = await add_favorite_crud(
            session=session,
            user_id=current_user.id,
            news_id=favorite_request.news_id,
        )
    return ApiResponse[None](msg=msg) 
    

# 删除收藏记录
@router.delete('/remove')
async def remove_favorite(
    news_id: int = Query(..., alias='newsId', description='新闻ID'),
    session: AsyncSession = Depends(get_session),    
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        msg = await delete_favorite_crud(
            session=session,
            user_id=current_user.id,
            news_id=news_id,
        )
    return ApiResponse[None](msg=msg) 
    

# 获取收藏列表
@router.get('/list')
async def get_favorite_list(
    page_commons: PageCommons = Depends(page_commons),
    session: AsyncSession = Depends(get_session),    
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        response = await get_favorite_list_crud(
            session=session,
            user_id=current_user.id,
            page_commons=page_commons,
        )
            
    return ApiResponse[FavoriteListResponse](msg='获取收藏列表成功', data=response) 
    

# 获取收藏列表
@router.delete('/clear')
async def clear_favorite_list(
    session: AsyncSession = Depends(get_session),    
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        msg = await delete_favorite_list_crud(
            session=session,
            user_id=current_user.id,
        )
            
    return ApiResponse[None](msg='清除收藏列表成功') 
    

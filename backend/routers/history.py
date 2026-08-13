
from config.db_conf import get_session
from schemas.history import HistoryRequest

from fastapi import APIRouter, Depends, Path
from schemas.schemas import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserInfoResponse
from schemas.history import HistoryListResponse
from CRUD.auth import verify_token
from CRUD.history import add_history_crud, delete_history_crud, get_history_list_crud, delete_history_list_crud
from schemas.schemas import PageCommons, page_commons


router = APIRouter(prefix='/api/history', tags=['history'])


# 添加历史记录
@router.post('/add')
async def add_history(
    history_request: HistoryRequest,
    session: AsyncSession = Depends(get_session),    
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        msg = await add_history_crud(
            session=session,
            user_id=current_user.id,
            news_id=history_request.news_id,
        )
    return ApiResponse[None](msg=msg) 
    

# 删除历史记录
@router.delete('/delete/{news_id}')
async def remove_history(
    news_id: int = Path(..., description='新闻ID'),
    session: AsyncSession = Depends(get_session),
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        msg = await delete_history_crud(
            session=session,
            user_id=current_user.id,
            news_id=news_id,
        )
    return ApiResponse[None](msg=msg) 
    

# 获取历史记录列表
@router.get('/list')
async def get_history_list(
    page_commons: PageCommons = Depends(page_commons),
    session: AsyncSession = Depends(get_session),    
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        response = await get_history_list_crud(
            session=session,
            user_id=current_user.id,
            page_commons=page_commons,
        )
            
    return ApiResponse[HistoryListResponse](msg='获取历史记录列表成功', data=response) 
    

# 获取历史记录列表
@router.delete('/clear')
async def clear_history_list(
    session: AsyncSession = Depends(get_session),    
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        msg = await delete_history_list_crud(
            session=session,
            user_id=current_user.id,
        )
            
    return ApiResponse[None](msg=msg) 
    

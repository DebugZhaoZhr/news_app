from config.db_conf import get_session
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserRequest, UserInfoResponse, UserAuthResponse, UserInfoBase, UserUptPwdResponse
from schemas.schemas import ApiResponse
from CRUD.user import create_user, get_user, create_token, get_token, get_user_info, get_user_update, update_password as update_password_crud
from CRUD.auth import verify_token



router = APIRouter(prefix='/api/user', tags=['user'])


@router.post('/register')
async def register(
    user_data: UserRequest,
    session: AsyncSession = Depends(get_session),
) -> ApiResponse:
    async with session.begin():
        user = await get_user(session, user_data.username)
        if user:
            raise HTTPException(status_code=400, detail="用户名已存在")
        user_info = await create_user(session, user_data)
        user_token = await create_token(session, user_info.id)
        
        response_data = UserAuthResponse(
            token=user_token,
            user_info=UserInfoResponse.model_validate(user_info)
        )
    return ApiResponse[UserAuthResponse](msg="注册成功", data=response_data)


@router.post('/login')
async def login(
    user_data: UserRequest,
    session: AsyncSession = Depends(get_session),
) -> ApiResponse:

    async with session.begin():
        user = await get_user(session, user_data.username)
        if not user:
            raise HTTPException(status_code=400, detail="用户名不存在")

        data = await get_token(session, user_data)
        
    return ApiResponse[UserAuthResponse](msg="登录成功", data=data)


@router.get('/info')
async def info(user: UserInfoResponse = Depends(verify_token)) -> ApiResponse:

    return ApiResponse[UserInfoResponse](msg="获取用户信息成功", data=user)


@router.put('/update')
async def update(
    user_data: UserInfoBase,
    session: AsyncSession = Depends(get_session),
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        result = await get_user_update(
            session, 
            current_user.id, 
            user_data
        )
        if not result:
            raise HTTPException(status_code=400, detail="用户名不存在")

        
    return ApiResponse[UserInfoBase](msg="更新成功", data=result)


@router.put('/password')
async def update_password(
    user_data: UserUptPwdResponse,
    session: AsyncSession = Depends(get_session),
    current_user: UserInfoResponse = Depends(verify_token)
) -> ApiResponse:

    async with session.begin():
        result = await update_password_crud(
            session, 
            current_user.id, 
            user_data
        )
        if not result:
            raise HTTPException(status_code=400, detail="用户名不存在")

        
    return ApiResponse[None](msg="更新成功", data=None)

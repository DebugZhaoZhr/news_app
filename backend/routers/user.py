from config.db_conf import get_session
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserRequest, UserInfoResponse, UserAuthResponse
from utils.response import success_response
from fastapi.responses import JSONResponse

from CRUD.user import create_user, get_user, create_token

router = APIRouter(prefix='/api/user', tags=['user'])

@router.post('/register')
async def register(
    user_data: UserRequest,
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    user = await get_user(session, user_data.username)
    if user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user_info = await create_user(session, user_data)
    user_token = await create_token(session, user_info.id)
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": user_token,
    #         "user_info": {
    #             "id": user_info.id,
    #             "username": user_info.username,
    #             "bio": user_info.bio,
    #             "gender": user_info.gender,
    #             "avatar": user_info.avatar,
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=user_token, user_info=UserInfoResponse.model_validate(user_info))
    return success_response(msg="注册成功", data=response_data)

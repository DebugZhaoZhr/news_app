from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_session

from routers.user import UserInfoResponse
from CRUD.user import get_user_info



async def verify_token(
    session: AsyncSession = Depends(get_session),
    token: str = Header(..., alias="Authorization")
) -> UserInfoResponse:

    async with session.begin():
        user = await get_user_info(session, token)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌无效或已过期")
        
    return UserInfoResponse.model_validate(user)

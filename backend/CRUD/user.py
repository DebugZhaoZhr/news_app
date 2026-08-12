from models.user import User, UserToken
from schemas.user import UserRequest, UserAuthResponse, UserInfoResponse, UserInfoBase
from utils.public import hash_password, verify_password

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Header
from datetime import datetime, timedelta

import uuid


async def get_user(
    session: AsyncSession,
    user_name: str
) -> UserInfoResponse | None:
    # async with session.begin():
    stmt = select(User).where(User.username == user_name)
    user = await session.scalar(stmt)
    
    data = None
    if user:
        data = UserInfoResponse(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            gender=user.gender,
            bio=user.bio,
        )
    await session.flush()
    return data


async def create_user(
    session: AsyncSession,
    user_data: UserRequest
):
    # async with session.begin():

    user_data.password = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        password=user_data.password,
    )
    session.add(user)
    await session.flush()
    return user


async def create_token(
    session: AsyncSession,
    user_id: int
):

    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(minutes=100)
    
    stmt = select(UserToken).where(UserToken.user_id == user_id)
    user_token = await session.scalar(stmt)

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        session.add(user_token)
    await session.flush()
    return token


async def get_token(
    session: AsyncSession,
    user_data: UserRequest
) -> UserAuthResponse:

    stmt = select(User).where(User.username == user_data.username)
    user = await session.scalar(stmt)

    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
                    
    token = await create_token(session, user.id)
        
    await session.flush()
    return UserAuthResponse(
        token=token,
        user_info=user
    )


async def get_user_info(
    session: AsyncSession,
    token: str
) -> UserInfoResponse:

    stmt = select(UserToken).where(UserToken.token == token)
    db_token = await session.scalar(stmt)
    
    if not db_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录!")
    if db_token.expires_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录过期，请重新登录!")
        
    query = select(User).where(User.id == db_token.user_id)
    user = await session.scalar(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
        
    
    await session.flush()
    return UserInfoResponse.model_validate(user)


async def get_user_update(
    session: AsyncSession,
    user_id: int,
    user_data: UserInfoBase,
) -> UserInfoBase:

    user = await session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # stmt = update(User).where(User.id == user_id).values(**user_data.model_dump(exclude_none=True))
    # await session.execute(stmt)

    update_data = user_data.model_dump(exclude_none=True)
    if not update_data:
        return UserInfoBase(
            nickname=user.nickname,
            avatar=user.avatar,
            gender=user.gender,
            bio=user.bio,
            phone=user.phone,
        )
        
    for key, value in update_data.items():
        setattr(user, key, value)

    await session.flush()
    
    return UserInfoBase(
        nickname=user.nickname,
        avatar=user.avatar,
        gender=user.gender,
        bio=user.bio,
        phone=user.phone,
    )

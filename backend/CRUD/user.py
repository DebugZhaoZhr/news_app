from models.user import User, UserToken
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from utils.public import hash_password
from schemas.user import UserRequest
import uuid
from datetime import datetime, timedelta



async def get_user(
    session: AsyncSession,
    user_name: str
) -> User | None:
    async with session.begin():
        stmt = select(User).where(User.username == user_name)
        user = await session.scalar(stmt)

    return user


async def create_user(
    session: AsyncSession,
    user_data: UserRequest
):
    async with session.begin():

        user_data.password = hash_password(user_data.password)
        user = User(
            username=user_data.username,
            password=user_data.password,
        )
        session.add(user)
    return user

async def create_token(
    session: AsyncSession,
    user_id: int
):
    async with session.begin():

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

    return token

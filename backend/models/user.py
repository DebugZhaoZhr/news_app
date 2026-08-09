from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from models.base import Base
from sqlalchemy import Enum, ForeignKey, DateTime
from datetime import datetime



class User(Base):
    __tablename__ = 'user'

    __table_args__ = (
        Index('username_unique', 'username'),
        Index('phone_unique', 'phone'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True, comment='用户ID')
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment='用户名')
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码(加密存储)')
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='昵称')
    avatar: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='头像')

    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True, index=True, comment='手机号')
    gender: Mapped[str | None] = mapped_column(
        Enum('male', 'female', 'unknown', name='gender_enum'),
        nullable=True,
        comment='性别'
    )
    bio: Mapped[str | None] = mapped_column(String, default='这个人很懒,什么都没有写', nullable=True, comment='个人简介')

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, nickname={self.nickname}, avatar={self.avatar})"



class UserToken(Base):
    __tablename__ = 'user_token'

    __table_args__ = (
        Index('token_unique', 'token'),
        Index('user_id_unique', 'user_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True, comment='用户tokenID')
    token: Mapped[str] = mapped_column(String(255), nullable=False, comment='用户token')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment='用户ID')
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment='过期时间')

    def __repr__(self):
        return f"UserToken(id={self.id}, token={self.token}, user_id={self.user_id}, expires_at={self.expires_at})"
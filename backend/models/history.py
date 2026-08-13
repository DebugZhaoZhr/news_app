
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, UniqueConstraint
from models.base import Base
from datetime import datetime


class History(Base):
    __tablename__ = 'history'

    __table_args__ = (
        UniqueConstraint ('user_id', 'news_id', name='user_news_unique'),
        Index('fk_history_user_id', 'user_id'), # 高频查询场景
        Index('fk_history_news_id', 'news_id'), # 高频查询场景
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键 收藏id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="用户id")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey('news.id'), nullable=False, comment="新闻id")
    view_time: Mapped[datetime] = mapped_column(default=datetime.now, comment="查看时间")


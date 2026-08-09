from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Index
from models.base import Base

class Category(Base):
    __tablename__ = 'news_category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键 分类id")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序顺序")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, sort_order={self.sort_order})"

class News(Base):
    __tablename__ = 'news'

    __table_args__ = ( # 创建索引 提升查询速度
        Index('fk_news_category_idx', 'category_id'), # 高频查询场景
        Index('idx_publish_time', 'publish_time'), # 按发布时间排序
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键 新闻id")   
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="新闻标题")
    description: Mapped[str] = mapped_column(String(500), comment="新闻描述")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻图片")
    author: Mapped[str] = mapped_column(String(50), comment="新闻作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="分类id")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="点击量")
    publish_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), comment="发布时间")

    def __repr__(self):
        return f"News(id={self.id}, title={self.title}, description={self.description}, category_id={self.category_id})"

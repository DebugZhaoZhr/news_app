from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 数据库URL
async_database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/news_app"

# 创建异步数据库引擎
async_engine = create_async_engine(
    async_database_url,
    echo=True,
    pool_size=10,
    max_overflow=20, # 设置连接池额外数量
    pool_timeout=20, # 设置连接池超时时间
    pool_recycle=3600, # 设置连接池回收时间
    pool_pre_ping=True # 设置连接池预连接
)

# 创建异步会话工厂
ASYNC_SESSION_LOCAL = async_sessionmaker[AsyncSession](
    bind=async_engine, # 绑定异步数据库引擎
    class_=AsyncSession, # 使用异步会话类
    autoflush=True, # 自动刷新会话 查找之前是否flush操作
    expire_on_commit=False, # 提交后会话不过期, 不会重新查询数据库
)

# 异步会话依赖项
async def get_session():
    async with ASYNC_SESSION_LOCAL() as session:
        yield session 
        await session.close()

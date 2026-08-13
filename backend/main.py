from fastapi import FastAPI
import uvicorn
from utils.register_exception import register_exception_handlers

from routers import news, user, favorite, history

app = FastAPI()

# 注册全局异常处理函数 
register_exception_handlers(app)

app.include_router(news.router)
app.include_router(user.router)
app.include_router(favorite.router)
app.include_router(history.router)

# 启动FastAPI应用
if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8080, reload=True)

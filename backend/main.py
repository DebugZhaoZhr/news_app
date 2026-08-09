from fastapi import FastAPI
import uvicorn

from routers import news, user

app = FastAPI()

app.include_router(news.router)
app.include_router(user.router)

# 启动FastAPI应用
if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8080, reload=True)

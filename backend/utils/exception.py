import traceback
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from starlette import status

# 开发模式: 返回详细错误信息
# 生产模式: 返回通用错误信息
DEBUG_MODE = True


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        },
        status_code=exc.status_code,
    )

async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    error_msg = str(exc.orig)

    if "username_unique" in error_msg or "duplicate" in error_msg:
        detail = "用户名已存在"
    elif "email_unique" in error_msg or "duplicate" in error_msg:
        detail = "邮箱已存在"
    else:
        detail = "数据库约束冲突, 请检查输入"
    error_data = None

    if DEBUG_MODE: 
        error_data = {
            "error_type": "IntegrityError",
            "error_msg": detail,
            "path": str(request.url),
        }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data
        },
    )

async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:

    error_data = None

    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_msg": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url),
        }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库错误",
            "data": error_data
        },
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    error_data = None

    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_msg": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url),
        }
    
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器错误",
            "data": error_data
        },
    )
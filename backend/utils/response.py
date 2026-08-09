from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(msg: str, data: dict = None) -> JSONResponse:
    content = {
        "code": 200,
        "message": msg,
        "data": data,
    }
    return JSONResponse(content=jsonable_encoder(content))

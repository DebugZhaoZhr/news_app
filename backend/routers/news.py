from fastapi import APIRouter

router = APIRouter(prefix='/api/news', tags=['news'])

@router.get('/categories')
def get_categories():
    return {"message": "获取成功"}
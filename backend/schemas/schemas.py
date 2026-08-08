from fastapi import Query

async def page_commons(
    page: int = Query(1, description="页码", ge=1, le=100),
    limit: int = Query(10, description="每页数量", le=100)
):
    return {
        'page': page,
        'limit': limit
    }

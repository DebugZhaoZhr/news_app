import redis.asyncio as redis_async
import json
from typing import Any

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis_async.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True, # 解码响应为字符串
    protocol=2,            # 强制使用 RESP2 协议，兼容 Redis < 6.0
    socket_timeout=5,
    socket_connect_timeout=5,
)


# 获取缓存
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f'获取缓存失败: {e}')
        return None


# 获取JSON缓存 列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        
        if not data:
            return None
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f'JSON缓存解析失败 key={key}: {e}')
        return None
    except Exception as e:
        print(f'获取缓存失败: {e}')
        return None


# 设置缓存 
async def set_cache(key: str, value: Any, expire: int = 60 * 5):
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f'设置缓存失败: {e}')
        return False

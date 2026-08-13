# 新闻相关的缓存
from config.cache_conf import get_json_cache, set_cache
from typing import Any, List, Dict

CATEGORY_KEY = 'news:category'


# 获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORY_KEY)


# 写入新闻分类缓存
# 分类/配置: 120分钟, 列表 10分钟, 详情 30分钟, 验证码 2分钟 -- 数据越稳定 缓存越久
async def set_cached_categories(
    data: List[Dict[str, Any]],
    expire: int = 60 * 120,
):
    return await set_cache(CATEGORY_KEY, data, expire)
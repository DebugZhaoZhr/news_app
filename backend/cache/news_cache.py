# 新闻相关的缓存
from config.cache_conf import get_json_cache, set_cache
from typing import Any, List, Dict

CATEGORY_KEY = 'news:category'
NEWS_LIST_KEY_PREFIX = 'news_list'


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


# 写入新闻列表分类缓存
# 分类/配置: 120分钟, 列表 10分钟, 详情 30分钟, 验证码 2分钟 -- 数据越稳定 缓存越久
async def set_cached_news_list(
    category_id: int | None,
    page: int,
    limit: int,
    total: int,
    news_list: List[Dict[str, Any]],
    expire: int = 60 * 10,
):

    category_id = category_id if category_id is not None else 'all'
    key = f'{NEWS_LIST_KEY_PREFIX}:{category_id}:{page}:{limit}'
    data = {
        'total': total,
        'list': news_list,
    }
    return await set_cache(key, data, expire)


# 获取新闻列表分类缓存
async def get_cached_news_list(
    category_id: int | None,
    page: int,
    limit: int,
):

    category_id = category_id if category_id is not None else 'all'
    key = f'{NEWS_LIST_KEY_PREFIX}:{category_id}:{page}:{limit}'
    return await get_json_cache(key)

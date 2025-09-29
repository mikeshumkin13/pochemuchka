from __future__ import annotations
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Tuple, Dict

from redis.asyncio import Redis
from app.config import settings

# Основной клиент Redis
_redis: Redis | None = Redis.from_url(settings.redis_url, decode_responses=True) if settings.redis_url else None

# Простой in-memory fallback (на случай отсутствия/падения Redis)
_mem_store: Dict[str, int] = {}

def _today_key(child_id: int) -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"quota:{child_id}:{today}"

def _seconds_until_end_of_day() -> int:
    now = datetime.now(timezone.utc)
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return int((tomorrow - now).total_seconds())

async def check_and_increment(child_id: int, daily_limit: int) -> Tuple[bool, int, int]:
    """
    Возвращает (allowed, used, limit)
    - allowed = used <= limit
    """
    key = _today_key(child_id)

    # Путь через Redis
    if _redis:
        try:
            used = await _redis.incr(key)
            if used == 1:
                await _redis.expire(key, _seconds_until_end_of_day())
            return (used <= daily_limit, used, daily_limit)
        except Exception:
            # упали на Redis — идём через fallback
            pass

    # Fallback: in-memory (dev)
    used = _mem_store.get(key, 0) + 1
    _mem_store[key] = used
    return (used <= daily_limit, used, daily_limit)



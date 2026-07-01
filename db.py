import asyncpg
import logging
from typing import Optional, List, Dict, Any

log = logging.getLogger(__name__)
_pool: Optional[asyncpg.pool.Pool] = None

async def init_db_pool(dsn: str, min_size: int = 1, max_size: int = 10):
    global _pool
    if _pool is not None:
        return
    try:
        _pool = await asyncpg.create_pool(dsn, min_size=min_size, max_size=max_size)
        log.info("Database pool initialized.")
    except Exception as e:
        log.exception("Failed to initialize DB pool: %s", e)
        raise

async def close_db_pool():
    global _pool
    if _pool is not None:
        try:
            await _pool.close()
            log.info("Database pool closed.")
        except Exception:
            log.exception("Error closing DB pool.")
        finally:
            _pool = None

async def init_db():
    """Create necessary tables if they do not exist."""
    global _pool
    if _pool is None:
        raise RuntimeError("DB pool is not initialized")
    create_sql = """
    CREATE TABLE IF NOT EXISTS welcome (
        chat_id BIGINT PRIMARY KEY,
        template TEXT
    );

    CREATE TABLE IF NOT EXISTS buttons (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT,
        btn_text TEXT,
        btn_url TEXT
    );

    CREATE TABLE IF NOT EXISTS channels (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT,
        channel_text TEXT
    );
    """
    try:
        async with _pool.acquire() as conn:
            await conn.execute(create_sql)
            log.info("DB tables ensured.")
    except Exception:
        log.exception("Failed to create/ensure DB tables.")
        raise

# ---- Welcome template operations ----
async def get_welcome(chat_id: int) -> Optional[str]:
    global _pool
    if _pool is None:
        log.warning("get_welcome called but DB pool is None")
        return None
    try:
        async with _pool.acquire() as conn:
            row = await conn.fetchrow("SELECT template FROM welcome WHERE chat_id=$1", chat_id)
            return row["template"] if row else None
    except Exception:
        log.exception("get_welcome failed for chat_id=%s", chat_id)
        return None

async def set_welcome(chat_id: int, template: str) -> bool:
    global _pool
    if _pool is None:
        log.warning("set_welcome called but DB pool is None")
        return False
    try:
        async with _pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO welcome(chat_id, template) VALUES($1, $2) "
                "ON CONFLICT (chat_id) DO UPDATE SET template = EXCLUDED.template",
                chat_id, template
            )
            return True
    except Exception:
        log.exception("set_welcome failed for chat_id=%s", chat_id)
        return False

async def delete_welcome(chat_id: int) -> bool:
    global _pool
    if _pool is None:
        log.warning("delete_welcome called but DB pool is None")
        return False
    try:
        async with _pool.acquire() as conn:
            await conn.execute("DELETE FROM welcome WHERE chat_id=$1", chat_id)
            return True
    except Exception:
        log.exception("delete_welcome failed for chat_id=%s", chat_id)
        return False

# ---- Buttons operations ----
async def add_button(chat_id: int, btn_text: str, btn_url: str) -> Optional[int]:
    global _pool
    if _pool is None:
        log.warning("add_button called but DB pool is None")
        return None
    try:
        async with _pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO buttons(chat_id, btn_text, btn_url) VALUES($1, $2, $3) RETURNING id",
                chat_id, btn_text, btn_url
            )
            return row["id"] if row else None
    except Exception:
        log.exception("add_button failed for chat_id=%s text=%s", chat_id, btn_text)
        return None

async def list_buttons(chat_id: int) -> List[Dict[str, Any]]:
    global _pool
    if _pool is None:
        return []
    try:
        async with _pool.acquire() as conn:
            rows = await conn.fetch("SELECT id, btn_text, btn_url FROM buttons WHERE chat_id=$1 ORDER BY id", chat_id)
            return [{"id": r["id"], "text": r["btn_text"], "url": r["btn_url"]} for r in rows]
    except Exception:
        log.exception("list_buttons failed for chat_id=%s", chat_id)
        return []

async def delete_button_by_id(chat_id: int, btn_id: int) -> bool:
    global _pool
    if _pool is None:
        return False
    try:
        async with _pool.acquire() as conn:
            await conn.execute("DELETE FROM buttons WHERE chat_id=$1 AND id=$2", chat_id, btn_id)
            return True
    except Exception:
        log.exception("delete_button_by_id failed for chat_id=%s id=%s", chat_id, btn_id)
        return False

async def delete_button_by_text(chat_id: int, btn_text: str) -> bool:
    global _pool
    if _pool is None:
        return False
    try:
        async with _pool.acquire() as conn:
            await conn.execute("DELETE FROM buttons WHERE chat_id=$1 AND btn_text=$2", chat_id, btn_text)
            return True
    except Exception:
        log.exception("delete_button_by_text failed for chat_id=%s text=%s", chat_id, btn_text)
        return False

# ---- Channels operations ----
async def add_channel(chat_id: int, channel_text: str) -> Optional[int]:
    global _pool
    if _pool is None:
        log.warning("add_channel called but DB pool is None")
        return None
    try:
        async with _pool.acquire() as conn:
            row = await conn.fetchrow("INSERT INTO channels(chat_id, channel_text) VALUES($1, $2) RETURNING id", chat_id, channel_text)
            return row["id"] if row else None
    except Exception:
        log.exception("add_channel failed for chat_id=%s channel=%s", chat_id, channel_text)
        return None

async def list_channels(chat_id: int) -> List[Dict[str, Any]]:
    global _pool
    if _pool is None:
        return []
    try:
        async with _pool.acquire() as conn:
            rows = await conn.fetch("SELECT id, channel_text FROM channels WHERE chat_id=$1 ORDER BY id", chat_id)
            return [{"id": r["id"], "channel": r["channel_text"]} for r in rows]
    except Exception:
        log.exception("list_channels failed for chat_id=%s", chat_id)
        return []

async def delete_channel_by_text(chat_id: int, channel_text: str) -> bool:
    global _pool
    if _pool is None:
        return False
    try:
        async with _pool.acquire() as conn:
            await conn.execute("DELETE FROM channels WHERE chat_id=$1 AND channel_text=$2", chat_id, channel_text)
            return True
    except Exception:
        log.exception("delete_channel_by_text failed for chat_id=%s channel=%s", chat_id, channel_text)
        return False

async def list_all_channels() -> List[str]:
    global _pool
    if _pool is None:
        return []
    try:
        async with _pool.acquire() as conn:
            rows = await conn.fetch("SELECT DISTINCT channel_text FROM channels")
            return [r["channel_text"] for r in rows]
    except Exception:
        log.exception("list_all_channels failed")
        return []

# ---- Stats ----
async def get_stats() -> Dict[str, int]:
    global _pool
    if _pool is None:
        return {"buttons": 0, "channels": 0, "welcomes": 0}
    try:
        async with _pool.acquire() as conn:
            buttons_count = await conn.fetchval("SELECT COUNT(*) FROM buttons")
            channels_count = await conn.fetchval("SELECT COUNT(*) FROM channels")
            welcomes_count = await conn.fetchval("SELECT COUNT(*) FROM welcome")
            return {"buttons": buttons_count, "channels": channels_count, "welcomes": welcomes_count}
    except Exception:
        log.exception("get_stats failed")
        return {"buttons": 0, "channels": 0, "welcomes": 0}

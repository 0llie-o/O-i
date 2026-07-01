import asyncpg
from typing import Optional, List, Dict, Any

_pool: Optional[asyncpg.pool.Pool] = None

async def init_db_pool(dsn: str):
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn)

async def close_db_pool():
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

async def init_db():
    """Create necessary tables if they do not exist."""
    global _pool
    assert _pool is not None, "DB pool is not initialized"
    async with _pool.acquire() as conn:
        await conn.execute(
            """
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
        )

# ---- Welcome template operations ----
async def get_welcome(chat_id: int) -> Optional[str]:
    global _pool
    async with _pool.acquire() as conn:
        row = await conn.fetchrow("SELECT template FROM welcome WHERE chat_id=$1", chat_id)
        return row["template"] if row else None

async def set_welcome(chat_id: int, template: str) -> None:
    global _pool
    async with _pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO welcome(chat_id, template) VALUES($1, $2) ON CONFLICT (chat_id) DO UPDATE SET template = EXCLUDED.template",
            chat_id,
            template,
        )

async def delete_welcome(chat_id: int) -> None:
    global _pool
    async with _pool.acquire() as conn:
        await conn.execute("DELETE FROM welcome WHERE chat_id=$1", chat_id)

# ---- Buttons operations ----
async def add_button(chat_id: int, btn_text: str, btn_url: str) -> int:
    global _pool
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO buttons(chat_id, btn_text, btn_url) VALUES($1, $2, $3) RETURNING id",
            chat_id,
            btn_text,
            btn_url,
        )
        return row["id"]

async def list_buttons(chat_id: int) -> List[Dict[str, Any]]:
    global _pool
    async with _pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, btn_text, btn_url FROM buttons WHERE chat_id=$1 ORDER BY id", chat_id)
        return [{"id": r["id"], "text": r["btn_text"], "url": r["btn_url"]} for r in rows]

async def delete_button_by_id(chat_id: int, btn_id: int) -> int:
    global _pool
    async with _pool.acquire() as conn:
        res = await conn.execute("DELETE FROM buttons WHERE chat_id=$1 AND id=$2", chat_id, btn_id)
        return res

async def delete_button_by_text(chat_id: int, btn_text: str) -> int:
    global _pool
    async with _pool.acquire() as conn:
        res = await conn.execute("DELETE FROM buttons WHERE chat_id=$1 AND btn_text=$2", chat_id, btn_text)
        return res

# ---- Channels operations ----
async def add_channel(chat_id: int, channel_text: str) -> int:
    global _pool
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO channels(chat_id, channel_text) VALUES($1, $2) RETURNING id",
            chat_id,
            channel_text,
        )
        return row["id"]

async def list_channels(chat_id: int) -> List[Dict[str, Any]]:
    global _pool
    async with _pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, channel_text FROM channels WHERE chat_id=$1 ORDER BY id", chat_id)
        return [{"id": r["id"], "channel": r["channel_text"]} for r in rows]

async def delete_channel_by_text(chat_id: int, channel_text: str) -> int:
    global _pool
    async with _pool.acquire() as conn:
        res = await conn.execute("DELETE FROM channels WHERE chat_id=$1 AND channel_text=$2", chat_id, channel_text)
        return res

async def list_all_channels() -> List[str]:
    """Return distinct channel identifiers across all chats."""
    global _pool
    async with _pool.acquire() as conn:
        rows = await conn.fetch("SELECT DISTINCT channel_text FROM channels")
        return [r["channel_text"] for r in rows]

# ---- Stats ----
async def get_stats() -> Dict[str, int]:
    global _pool
    async with _pool.acquire() as conn:
        buttons_count = await conn.fetchval("SELECT COUNT(*) FROM buttons")
        channels_count = await conn.fetchval("SELECT COUNT(*) FROM channels")
        welcomes_count = await conn.fetchval("SELECT COUNT(*) FROM welcome")
        return {"buttons": buttons_count, "channels": channels_count, "welcomes": welcomes_count}

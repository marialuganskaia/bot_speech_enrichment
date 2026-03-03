import aiosqlite
from database.models import db_path

#запросы к бд, связанные со словами
async def add_word(word, definition, example_text, author, book):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            INSERT INTO words (word, definition, example_text, author, book)
            VALUES (:word, :definition, :example_text, :author, :book)
        """, {"word": word, "definition": definition, "example_text": example_text, "author": author, "book": book})
        await db.commit()

async def get_unsent_words(limit=3):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("""
            SELECT id, word, definition, example_text, author, book
            FROM words
            WHERE sent_at IS NULL AND is_approved = 1
            LIMIT :limit
        """, {"limit": limit}) as cursor:
            return await cursor.fetchall()

async def mark_words_as_sent(word_ids: list):
    async with aiosqlite.connect(db_path) as db:
        await db.execute(f"""
            UPDATE words SET sent_at = CURRENT_TIMESTAMP
            WHERE id IN ({','.join('?' * len(word_ids))})
        """, word_ids)
        await db.commit()


#запросы к бд, связанные с юзерами
async def add_user(telegram_id):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (telegram_id) VALUES (:telegram_id)
        """, {"telegram_id": telegram_id})
        await db.commit()

async def set_user_active(telegram_id, is_active: bool):
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            UPDATE users SET is_active = :is_active WHERE telegram_id = :telegram_id
        """, {"is_active": int(is_active), "telegram_id": telegram_id})
        await db.commit()

async def get_active_users():
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("""
            SELECT telegram_id FROM users WHERE is_active = 1
        """) as cursor:
            return await cursor.fetchall()
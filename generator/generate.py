import json
import asyncio
from openai import OpenAI
from config import openai_api_key
from database.models import create_tables
from database.db import add_word
from generator.prompts import generate_words_prompt

client = OpenAI(api_key=openai_api_key)

async def generate_and_save_words():
    print('Запрашиваем слова у нейронки')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": generate_words_prompt}
        ],
        temperature=0.7
    )

    raw = response.choices[0].message.content
    print('Слова получены, парсим json')
    words = json.loads(raw)
    print(f"Получено слов: {len(words)}")
    await create_tables()

    for w in words:
        await add_word(
            word=w["word"],
            definition=w["definition"],
            example_text=w["example_text"],
            author=w["author"],
            book=w["book"]
        )
        print(f"Сохранено слов: {w['word']}")
    print('Всё')

if __name__ == "__main__":
    asyncio.run(generate_and_save_words())
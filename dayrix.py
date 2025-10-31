import os
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Твой ключ OpenRouter
OPENROUTER_API_KEY = os.getenv("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")  # можно прописать прямо в Railway Variables

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Асинхронная функция для запроса к OpenRouter
async def ask_openrouter(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-4",  # или любую другую модель из твоего списка
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, json=payload, headers=headers) as resp:
            data = await resp.json()
            # В зависимости от структуры ответа
            return data["choices"][0]["message"]["content"]

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я готов к работе.")

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Ждем выполнения корутины ask_openrouter
    reply = await ask_openrouter(user_text)
    await update.message.reply_text(reply)

# Основной запуск бота
async def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Telegram Token в Railway Variables
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
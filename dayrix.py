# dayrix.py
import asyncio
import aiohttp
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# -----------------------------
# Ключи (замени на свои)
OPENROUTER_API_KEY = "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"
TELEGRAM_TOKEN = 8469572341:AAF4rd5Ppx0RA79bB7em6o9D0lEdJ4ahSfE"
# -----------------------------

# Функция для запроса к OpenRouter API
async def ask_openrouter(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    json_data = {
        "model": "openrouter-gpt",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я DashRobl AI. Напиши мне что-нибудь.")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Обрабатываю...")
    try:
        reply = await ask_openrouter(user_text)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Основная функция
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    await app.run_polling()

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())
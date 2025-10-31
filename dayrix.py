import os
import asyncio
import aiohttp
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения!")

# --- Функции обработки сообщений ---

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот DashRobl.")

async def echo(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# --- Пример асинхронного запроса к OpenRouter ---
async def ask_openrouter(prompt: str):
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        return "API ключ OpenRouter не найден!"
    
    url = "https://openrouter.ai/api/v1/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4.1-mini",
        "input": prompt
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                return result.get("output", [{"content": "Нет ответа"}])[0]["content"]
            else:
                return f"Ошибка OpenRouter: {resp.status}"

# --- Основная функция бота ---
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Команды и обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    await app.run_polling()

# --- Запуск ---
if __name__ == "__main__":
    asyncio.run(main())
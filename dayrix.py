import asyncio
import aiohttp
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- Вставляем ключи прямо сюда ---
TELEGRAM_TOKEN = "8469572341:AAF4rd5Ppx0RA79bB7em6o9D0lEdJ4ahSfE"
OPENROUTER_API_KEY = "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"

# --- Функции обработки сообщений ---
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот DashRobl.")

async def echo(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# --- Запрос к OpenRouter ---
async def ask_openrouter(prompt: str):
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
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    await app.run_polling()

# --- Запуск ---
if __name__ == "__main__":
    asyncio.run(main())
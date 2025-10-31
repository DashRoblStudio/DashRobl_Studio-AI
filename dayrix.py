# dayrix.py
import asyncio
import aiohttp
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# -----------------------------
# Ключи (берутся из переменных окружения Railway)
OPENROUTER_API_KEY = os.environ.get("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")
TELEGRAM_TOKEN = os.environ.get("8469572341:AAF4rd5Ppx0RA79bB7em6o9D0lEdJ4ahSfE")
# -----------------------------

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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
            logger.info(f"OpenRouter response: {data}")
            return data["choices"][0]["message"]["content"]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я DashRobl AI. Напиши мне что-нибудь.")
    logger.info(f"User {update.effective_user.id} started the bot.")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logger.info(f"Received message from {update.effective_user.id}: {user_text}")
    await update.message.reply_text("Обрабатываю...")
    try:
        reply = await ask_openrouter(user_text)
        await update.message.reply_text(reply)
        logger.info(f"Sent reply to {update.effective_user.id}: {reply}")
    except Exception as e:
        error_msg = f"Ошибка при обработке сообщения: {e}"
        await update.message.reply_text(error_msg)
        logger.error(error_msg)

# Основная функция
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    logger.info("Bot is starting...")
    await app.run_polling()

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import asyncio

# 🔑 Токены
TELEGRAM_BOT_TOKEN = "8469572341:AAF4rd5Ppx0RA79bB7em6o9D0lEdJ4ahSfE"
OPENROUTER_API_KEY = "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"

# ⚙️ Функция общения с OpenRouter
async def ask_openrouter(prompt: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-4o-mini",  # можно заменить на любую доступную модель
        "messages": [
            {"role": "system", "content": "Ты — Telegram-бот Dayrix, отвечай умно и кратко."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Ошибка соединения с OpenRouter: {e}"
    except KeyError:
        return f"Ошибка в ответе OpenRouter: {response.text}"

# 💬 Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"[{update.effective_user.first_name}] {user_text}")
    reply = await asyncio.to_thread(ask_openrouter, user_text)
    await update.message.reply_text(reply)

# 🚀 Основная функция
def main():
    print("✅ DayrixBot запущен...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
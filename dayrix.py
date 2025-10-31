from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests

# 🔑 Ключи
TELEGRAM_BOT_TOKEN = "8469572341:AAF4rd5Ppx0RA79bB7em6o9D0lEdJ4ahSfE"
OPENROUTER_API_KEY = "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"

# ⚙️ Функция общения с OpenRouter
async def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",  # можно выбрать другую модель
        "messages": [
            {"role": "system", "content": "Ты — Telegram-бот Dayrix, отвечай умно и кратко."},
            {"role": "user", "content": prompt},
        ],
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"Ошибка: {r.status_code}\n{r.text}"
    except Exception as e:
        return f"Ошибка соединения: {e}"

# 💬 Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"[{update.effective_user.first_name}] {user_text}")
    reply = await ask_openrouter(user_text)
    await update.message.reply_text(reply)

# 🚀 Основная функция
def main():
    print("✅ DayrixBot запущен...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
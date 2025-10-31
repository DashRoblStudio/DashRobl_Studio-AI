# dayrix.py
import telebot
import requests

# ====== Токены ======
TELEGRAM_TOKEN = "8425180233:AAEuJg_EvS8FDK2DmnXxZvrgfhkUYAM_AzE"
OPENROUTER_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ====== Функция для OpenRouter ======
def openrouter_response(message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",  # или "gpt-3.5-turbo" если будут ошибки
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 500
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка: {e}"

# ====== Обработка сообщений Telegram ======
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    answer = openrouter_response(message.text)
    bot.reply_to(message, answer)

# ====== Запуск бота ======
print("Dayrix Telegram Bot запущен...")
bot.infinity_polling()
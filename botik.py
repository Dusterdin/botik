import telebot
import requests
import time

# 🔹 Встав свої дані сюди
TWITCH_CLIENT_ID = "fno7eo6cxyj1msvu1dyw53zer6l4xu"
TWITCH_ACCESS_TOKEN = "2dafephdqg7tpl40ina20zupzfet49"
TWITCH_USERNAME = "frudzi5"
TELEGRAM_BOT_TOKEN = "8108921426:AAHjjNQ1bTKEyhT6nwajDoaCa_aymGmGF_c"
TELEGRAM_CHAT_ID = "-1001837282281"

# Створюємо об'єкт бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Отримуємо ID стрімера
def get_twitch_user_id(username):
    url = f"https://api.twitch.tv/helix/users?login={username}"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers).json()
    if "data" in response and response["data"]:
        return response["data"][0]["id"]
    return None

# Перевіряємо, чи стрімер онлайн
def is_stream_online(user_id):
    url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers).json()
    return len(response["data"]) > 0  # True якщо стрім активний

# Основна функція моніторингу
def check_stream():
    user_id = get_twitch_user_id(TWITCH_USERNAME)
    if not user_id:
        print("ne vdalos ID strim.")
        return

    stream_live = False  # Стан стріму
    last_message_id = None  # ID останнього повідомлення

    while True:
        try:
            if is_stream_online(user_id):
                if not stream_live:
                    # Надсилаємо повідомлення про старт стріму
                    message_text = f"**Стрім розпочався!**\n🎥 Дивитися: https://www.twitch.tv/{TWITCH_USERNAME}"
                    sent_message = bot.send_message(TELEGRAM_CHAT_ID, message_text, parse_mode="Markdown")
                    
                    last_message_id = sent_message.message_id  # Запам'ятовуємо ID повідомлення
                    stream_live = True
            else:
                if stream_live and last_message_id:
                    # Видаляємо повідомлення, якщо стрім офлайн
                    try:
                        bot.delete_message(TELEGRAM_CHAT_ID, last_message_id)
                        print("Стрім завершено, повідомлення видалено.")
                    except Exception as e:
                        print(f" Помилка при видаленні повідомлення: {e}")

                    last_message_id = None  # Скидаємо ID повідомлення
                stream_live = False  # Скидаємо статус стріму

            time.sleep(60)  # Перевіряємо раз на хвилину

        except Exception as e:
            print(f"⚠️ Помилка: {e}")
            time.sleep(10)  # Якщо помилка, чекаємо 10 сек і пробуємо знову

# Запускаємо моніторинг
check_stream()


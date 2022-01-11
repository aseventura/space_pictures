import os
import requests
import time
import telegram
from dotenv import load_dotenv
from fetch_nasa import fetch_nasa_epic
from fetch_nasa import fetch_nasa_apod
from fetch_spacex_last_launch import fetch_spacex_last_launch


def send_pictures_in_telegram_channel(telegram_bot_token: str, telegram_chat_id: str, picture_path: str):
    bot = telegram.Bot(telegram_bot_token)
    with open(picture_path, 'rb') as picture:
        bot.send_photo(chat_id=telegram_chat_id, photo=picture)


def main():
    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    interval_to_publish = int(os.getenv('INTERVAL_TO_PUBLISH'))
    directories = ('SpaceX', 'APOD', 'EPIC')
    try:
        fetch_spacex_last_launch(directories[0])
        fetch_nasa_apod(directories[1], 50, nasa_api_key)
        fetch_nasa_epic(directories[2], nasa_api_key)
    except requests.models.HTTPError:
        print('Некорректный ответ сервера')
    while True:
        for directory in directories:
            for picture_name in os.listdir(directory):
                picture_path = os.path.join(directory, picture_name)
                send_pictures_in_telegram_channel(telegram_bot_token, telegram_channel_id, picture_path)
                time.sleep(interval_to_publish)


if __name__ == '__main__':
    main()
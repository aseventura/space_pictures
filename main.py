import os
import requests
import time
import telegram
from dotenv import load_dotenv
from fetch_nasa_epic import fetch_nasa_epic
from fetch_nasa_apod import fetch_nasa_apod
from fetch_spacex_last_launch import fetch_spacex_last_launch


def send_pictures_in_telegram_channel(telegram_bot_token: str, telegram_chat_id: str, picture_path: str):
    bot = telegram.Bot(telegram_bot_token)
    bot.send_photo(chat_id=telegram_chat_id, photo=open(picture_path, 'rb'))


def main():
    load_dotenv()
    NASA_API_KEY = os.getenv('NASA_API_KEY')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    INTERVAL_TO_PUBLISH = int(os.getenv('INTERVAL_TO_PUBLISH'))
    directories = ('SpaceX', 'APOD', 'EPIC')
    try:
        fetch_spacex_last_launch(directories[0])
        fetch_nasa_apod(directories[1], 50, NASA_API_KEY)
        fetch_nasa_epic(directories[2], NASA_API_KEY)
    except requests.models.HTTPError:
        print('Некорректный ответ сервера')
    while True:
        for directory in directories:
            for picture_name in os.listdir(directory):
                picture_path = os.path.join(directory, picture_name)
                send_pictures_in_telegram_channel(TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, picture_path)
                time.sleep(INTERVAL_TO_PUBLISH)


if __name__ == '__main__':
    main()
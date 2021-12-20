import os
import requests
import datetime
import time
import telegram
from pathlib import Path
from urllib import parse
from dotenv import load_dotenv


def create_directory(pictures_dir: str):
    directory = Path(pictures_dir)
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)


def download_picture(url: str, payload: str, picture_path: str):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(picture_path, 'wb') as picture_file:
        picture_file.write(response.content)


def get_file_extension(url: str):
    page_address = parse.urlsplit(parse.unquote(url)).path
    file_extension = os.path.splitext(page_address)[-1]
    return file_extension


def fetch_spacex_last_launch(pictures_dir: str):
    create_directory(pictures_dir)
    base_url = 'https://api.spacexdata.com/v3/rockets/falconheavy'
    '''
    More beautifull pictures:
    https://api.spacexdata.com/v3/rockets/starship
    https://api.spacexdata.com/v3/rockets/falcon9
    '''
    response = requests.get(base_url)
    response.raise_for_status()
    pictures_url = response.json()['flickr_images']
    for index, url in enumerate(pictures_url, 1):
        file_extension = get_file_extension(url)
        filename = f'falconheavy_{index}{file_extension}'
        picture_path = f'{pictures_dir}/{filename}'
        try:
            download_picture(
                url=url,
                payload='',
                picture_path=picture_path,
            )
        except requests.models.HTTPError:
            print('Не смог получить картинку')


def fetch_nasa_apod(pictures_dir: str, pictures_pcs: int, nasa_api_key: str):
    create_directory(pictures_dir)
    base_url = 'https://api.nasa.gov/planetary/apod'
    payloads = {
        'api_key': nasa_api_key,
        'count': pictures_pcs,
    }
    response = requests.get(base_url, params=payloads)
    response.raise_for_status()
    pictures_url = response.json()
    for index, picture_metadata in enumerate(pictures_url, 1):
        if picture_metadata['media_type'] == 'image':
            image_link = picture_metadata['url']
            file_extension = get_file_extension(image_link)
            filename = f'apod_{index}{file_extension}'
            picture_path = f'{pictures_dir}/{filename}'
            try:
                download_picture(
                    url=image_link,
                    payload='',
                    picture_path=picture_path,
                )
            except requests.models.HTTPError:
                print('Не смог получить картинку')


def fetch_nasa_epic(pictures_dir: str, nasa_api_key: str):
    create_directory(pictures_dir)
    base_url = 'https://api.nasa.gov/EPIC/'
    payload = {
        'api_key': nasa_api_key,
    }
    url = f'{base_url}api/natural/images'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    pictures_metadata = response.json()
    for picture_info in pictures_metadata:
        date_of_creation = datetime.datetime.fromisoformat(picture_info['date']).strftime('%Y/%m/%d')
        filename = picture_info['image']
        file_extension = '.png'
        image_link = f'{base_url}archive/natural/{date_of_creation}/png/{filename}{file_extension}'
        picture_path = f'{pictures_dir}/{filename}{file_extension}'
        try:
            download_picture(
                url=image_link,
                payload=payload,
                picture_path=picture_path,
            )
        except requests.models.HTTPError:
            print('Не смог получить картинку')


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
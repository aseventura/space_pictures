import datetime
import os
import requests
from download_picture import download_picture
from get_file_extension import get_file_extension


def fetch_nasa_apod(pictures_dir: str, pictures_pcs: int, nasa_api_key: str):
    os.makedirs(pictures_dir, exist_ok=True)
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
            download_picture(
                url=image_link,
                payload='',
                picture_path=picture_path,
            )


def fetch_nasa_epic(pictures_dir: str, nasa_api_key: str):
    os.makedirs(pictures_dir, exist_ok=True)
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
        download_picture(
            url=image_link,
            payload=payload,
            picture_path=picture_path,
        )
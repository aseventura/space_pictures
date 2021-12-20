import requests
import datetime
from create_directory import create_directory
from download_picture import download_picture


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
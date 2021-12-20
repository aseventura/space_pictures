import requests
from create_directory import create_directory
from get_file_extension import get_file_extension
from download_picture import download_picture


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
import requests
from create_directory import create_directory
from get_file_extension import get_file_extension
from download_picture import download_picture


'''
More beautifull pictures in:
    https://api.spacexdata.com/v3/rockets/starship
    https://api.spacexdata.com/v3/rockets/falcon9
'''


def fetch_spacex_last_launch(pictures_dir: str):
    create_directory(pictures_dir)
    base_url = 'https://api.spacexdata.com/v3/rockets/falconheavy'
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
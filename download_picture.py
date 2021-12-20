import requests


def download_picture(url: str, payload: str, picture_path: str):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(picture_path, 'wb') as picture_file:
        picture_file.write(response.content)
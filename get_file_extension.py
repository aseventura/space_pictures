import os
from urllib import parse


def get_file_extension(url: str):
    page_address = parse.urlsplit(parse.unquote(url)).path
    file_extension = os.path.splitext(page_address)[-1]
    return file_extension
import requests


def download_photo(url, path):
    data = requests.get(url).content
    with open(path, 'wb') as f:
        f.write(data)

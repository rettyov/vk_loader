import os
from typing import List
import urllib


def save_attachments(urls: List[str], save_path: str, part: str = 'photo'):
    save_photo_path = os.path.join(save_path, part)
    os.makedirs(save_photo_path, exist_ok=True)

    exist_files = os.listdir(save_photo_path)
    image_names = [url.split('?')[0].split('/')[-1] for url in urls]

    unique_image_names, unique_urls = [], []
    for url, image_name in zip(urls, image_names):
        if image_name not in exist_files:
            unique_image_names.append(image_name)
            unique_urls.append(url)

    for i, (url, image_name) in enumerate(zip(unique_urls, unique_image_names)):
        image_path = os.path.join(save_photo_path, image_name)
        local_filename, headers = urllib.request.urlretrieve(url, image_path)


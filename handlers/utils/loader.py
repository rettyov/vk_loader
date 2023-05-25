import os
from typing import List, Dict
import urllib

import yt_dlp


async def save_photo_attachments(save_part_path, unique_file_names, unique_urls):
    success_load = 0

    # В каждом urls содержится отсортированный список ссылок по доступным размерам
    for file_name, urls in zip(unique_file_names, unique_urls):
        file_path = os.path.join(save_part_path, file_name)

        for url in urls:
            try:
                local_filename, headers = urllib.request.urlretrieve(url, file_path)
                success_load += 1
                break
            except:
                continue
    return success_load


async def save_video_attachments(save_part_path, unique_file_names, unique_urls):
    success_load = 0

    # В каждом urls содержится отсортированный список ссылок по доступным размерам
    for file_name, urls in zip(unique_file_names, unique_urls):
        file_path = os.path.join(save_part_path, file_name)

        for url in urls:
            ydl_opts = {
                'cookiesfrombrowser': ('chrome', ),
                'verbose': True,
                'ie': 'vk',
                'outtmpl': file_path,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                success_load += 1
                break
            except:
                continue
    return success_load


# todo: В enum переделать!
download_function = {
    'photo': save_photo_attachments,
    'video': save_video_attachments,
}


async def save_attachments(attachments: Dict[str, List[List[str]]], save_path: str):
    result = {}
    for part, all_available_urls in attachments.items():
        save_part_path = os.path.join(save_path, part)
        os.makedirs(save_part_path, exist_ok=True)

        exist_files = os.listdir(save_part_path)
        file_names = [urls[0].split('?')[0].split('/')[-1] for urls in all_available_urls]

        if part == 'video':
            file_names = [file_name + '.mp4' for file_name in file_names]

        unique_file_names, unique_urls = [], []
        for file_name, urls in zip(file_names, all_available_urls):
            if file_name in unique_file_names or file_name in exist_files:
                continue
            unique_file_names.append(file_name)
            unique_urls.append(urls)

        success_load = await download_function[part](save_part_path, unique_file_names, unique_urls)

        result[part] = success_load
    return result

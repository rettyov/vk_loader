import os.path
from typing import List

from config.config import api


def get_max_size_index(sizes):
    max_height = 0
    best_index = 0
    for i, size in enumerate(sizes):
        if size.height > max_height:
            max_height = size.height
            best_index = i
    return best_index


def get_photo_urls(message, urls: List[str]) -> List[str]:
    for attachment in message.attachments:
        if attachment.photo:
            # todo: переделать на питоновский max
            max_size_index = get_max_size_index(attachment.photo.sizes)
            urls.append(attachment.photo.sizes[max_size_index].url)

    if message.fwd_messages:
        for fwd_message in message.fwd_messages:
            urls = get_photo_urls(fwd_message, urls)

    if message.reply_message:
        urls = get_photo_urls(message.reply_message, urls)

    return urls


async def get_save_path(message):
    users = await api.users.get(message.from_id)
    dir_name = f'{users[0].first_name}_{users[0].last_name}_{message.peer_id}'
    save_path = os.path.join(os.environ['save_dir'], dir_name)
    return save_path

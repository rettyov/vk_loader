import os.path
from typing import List

from config.config import api


def get_photo_urls(message, urls: List[List[str]]) -> List[List[str]]:
    for attachment in message.attachments:
        if attachment.photo:
            sorted_photos = sorted(attachment.photo.sizes, key=lambda x: x.height, reverse=True)
            urls.append([photo.url for photo in sorted_photos])

    if message.fwd_messages:
        for fwd_message in message.fwd_messages:
            urls = get_photo_urls(fwd_message, urls)

    if message.reply_message:
        urls = get_photo_urls(message.reply_message, urls)

    return urls


def get_video_urls(message, urls: List[List[str]]) -> List[List[str]]:
    for attachment in message.attachments:
        if attachment.video:
            urls.append([f'https://m.vk.com/video{attachment.video.owner_id}_{attachment.video.id}'])

    if message.fwd_messages:
        for fwd_message in message.fwd_messages:
            urls = get_video_urls(fwd_message, urls)

    if message.reply_message:
        urls = get_video_urls(message.reply_message, urls)

    return urls


async def get_attachments(message):
    # message не всегда включает весь контент для сообщений
    # поэтому используем get_by_id, чтобы получить message наверняка
    msg = await api.messages.get_by_id(message.id)

    photo_urls = []
    for item in msg.items:
        photo_urls = get_photo_urls(item, photo_urls)

    video_urls = []
    for item in msg.items:
        video_urls = get_video_urls(item, video_urls)

    return {'photo': photo_urls, 'video': video_urls}


async def get_save_path(message):
    users = await api.users.get(message.from_id)
    dir_name = f'{users[0].first_name}_{users[0].last_name}_{message.peer_id}'
    save_path = os.path.join(os.environ['save_dir'], dir_name)
    return save_path

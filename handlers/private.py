import os

from vkbottle.bot import BotLabeler, Message, rules
from .utils.processing import get_photo_urls, get_save_path
from .utils.loader import save_attachments

from config.config import api

private_labeler = BotLabeler()
private_labeler.auto_rules = [rules.FromPeerRule([
    int(os.environ["admin_id"]),
    int(os.environ["user_id"]),
])]


@private_labeler.message()
async def save_photos(message: Message):
    photo_urls = get_photo_urls(message, [])
    photo_urls = list(set(photo_urls))

    save_path = await get_save_path(message)
    await message.answer(f"Начинаю скачивать твои нюдсы({len(photo_urls)})! <3")
    save_attachments(photo_urls, save_path)
    await message.answer(f"Всё скачал!")




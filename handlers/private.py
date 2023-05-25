import os

from vkbottle.bot import BotLabeler, Message, rules
from .utils.processing import get_save_path, get_attachments
from .utils.loader import save_attachments


private_labeler = BotLabeler()
private_labeler.auto_rules = [rules.FromPeerRule([
    int(os.environ["admin_id"]),
    int(os.environ["user_id"]),
])]


@private_labeler.message()
async def save_photos(message: Message):
    attachments = await get_attachments(message)
    save_path = await get_save_path(message)

    if len(attachments['photo']) != 0:
        await message.answer(f"Начинаю скачивать твои нюдсы ({len(attachments['photo'])})! <3")
    if len(attachments['video']) != 0:
        await message.answer(f"Начинаю скачивать хоум-видосики ({len(attachments['video'])})! <3")
    result = await save_attachments(attachments, save_path)
    await message.answer(f"Всё скачал!\n{result['photo']} новых фото\n{result['video']} новых видео")




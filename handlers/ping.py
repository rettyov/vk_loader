from config.config import labeler


@labeler.message(text="ping")
async def ping_handler(message):
    await message.answer(f"pong! Yo ID: {message.peer_id}")

from vkbottle import Bot
from config.config import api, state_dispenser, labeler
from handlers import chat_labeler, admin_labeler, private_labeler


labeler.load(private_labeler)
labeler.load(chat_labeler)
labeler.load(admin_labeler)

bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)

bot.run_forever()

import os

from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler


api = API(os.environ["token"])
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

available_users = [
    int(os.environ['admin_id']),
    int(os.environ['user_id']),
]

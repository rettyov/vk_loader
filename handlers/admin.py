import os

from vkbottle.bot import BotLabeler, Message, rules


admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(int(os.environ["admin_id"]))]


@admin_labeler.message(command="halt")
async def halt(_):
    exit(0)

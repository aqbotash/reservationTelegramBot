from telegram import Bot

# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot = Bot(token='6258824392:AAEE_I40M8E908SUNoHttH-pLM3E6Kh6Qf4')

# Replace 'YOUR_GROUP_CHAT_ID' with the actual group chat ID
group_chat_id = bot.get_updates()[0].message.chat.id
print(group_chat_id)





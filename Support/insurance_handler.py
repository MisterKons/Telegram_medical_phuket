from .messages_base import messages


async def insurance_handler(client, message):
    user_id = message.from_user.id
    lang = client.user_data[user_id]["lang"]
    response = messages[lang]["insurance_about"]
    print("log")
    await client.send_message(user_id, response, disable_web_page_preview=True)

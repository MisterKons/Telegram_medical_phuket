import logging
from .messages_base import messages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

website_list = [
                "1. [Pillintrip](https://pillintrip.com/)",
                "2. [Drugs.com](https://www.drugs.com/)"
                ]

async def handle_medicine_command(client, message):
    user_id = message.from_user.id
    lang = client.user_data[user_id]["lang"]
    response = messages[lang]["medicine_sites"] + "\n".join(website_list)
    await client.send_message(user_id, response, disable_web_page_preview=True)

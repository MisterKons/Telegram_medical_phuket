import logging
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .messages_base import messages
from .credentials import ADMIN_ID

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def feedback_handler(client: Client, message):
    user_id = message.from_user.id
    lang = client.user_data.get(user_id, {}).get("lang", "en")

    feedback_message_user = messages[lang]["feedback_user"]
    client.user_data[user_id]["awaiting_feedback"] = True

    # Send message to the user
    await client.send_message(user_id, feedback_message_user)

async def handle_feedback_input(client: Client, message):
    user_id = message.from_user.id
    user = message.from_user
    username = user.username or user.first_name or user_id  # Use username if available, else first name, else user ID
    if user_id in client.user_data and client.user_data[user_id].get("awaiting_feedback"):
        feedback = message.text
        client.user_data[user_id]["awaiting_feedback"] = False
        lang = client.user_data[user_id]["lang"]

        # Send feedback to administrator
        admin_id = ADMIN_ID["KonstantinMRk"]
        try:
            await client.send_message(chat_id=admin_id, text=f"New feedback from user {username}:\n\n{feedback}")
            logger.info(f"Feedback from user {username} sent to admin.")
        except Exception as e:
            logger.error(f"Failed to send feedback to admin: {e}")

        # Thank the user for their feedback
        await client.send_message(user_id, messages[lang]["thank_you_feedback"])

        # Offer to start over or stop
        start_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(messages[lang]["try_again"], callback_data="start_over")],
            [InlineKeyboardButton(messages[lang]["stop"], callback_data="stop")]
        ])
        await client.send_message(user_id, messages[lang]["start_over_prompt"], reply_markup=start_keyboard)

from pymongo import MongoClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .credentials import MONGO_URI
import re
from .messages import messages

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['kons_new']
collection = db['clinics']

# Function to fetch unique values from a specified field
def fetch_unique_values(field_name):
    return collection.distinct(field_name)

# Function to get all sub_types
def get_sub_types():
    return fetch_unique_values('Sub_type')

# Function to send clinics in batches of 3
async def send_clinics(client, user_id, district, speciality, sent_clinics, message_id, lang):
    # Проверяем, используется ли специализированная клиника
    if client.user_data[user_id].get("specialized_clinic", False):
        # Используем регулярное выражение для поиска по частичному совпадению
        clinics = list(collection.find({"district_new": district, "Sub_type": re.compile(speciality, re.IGNORECASE)}))
    else:
        clinics = list(collection.find({"district_new": district, "type": speciality}))

    unsent_clinics = [clinic for clinic in clinics if clinic['_id'] not in sent_clinics]
    response = messages[lang]["clinic_info"]
    count = 0

    for clinic in unsent_clinics[:3]:
        response += (
            f"**Name:** {clinic.get('name')}\n"
            f"**Phone:** {clinic.get('phone_number')}\n"
            f"**Website:** [{messages[lang]['website_text']}]({clinic.get('website')})\n"
            f"**Location:** [{messages[lang]['maps_text']}]({clinic.get('place_link')})\n"
            f"**Specialization:** {clinic.get('type')} - {clinic.get('Sub_type')}\n\n"
        )
        sent_clinics.add(clinic['_id'])
        count += 1

    if count == 0:
        response = messages[lang]["no_more_clinics"]
        keyboard = [
            [InlineKeyboardButton(messages[lang]["try_again"], callback_data="try_again")],
            [InlineKeyboardButton(messages[lang]["stop"], callback_data="stop")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [[InlineKeyboardButton(messages[lang]["show_more"], callback_data="send_more")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

    await client.edit_message_text(user_id, message_id, response, reply_markup=reply_markup)

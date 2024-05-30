import re
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from support.credentials import MONGO_URI
from support.messages_base import messages

client_my = AsyncIOMotorClient(MONGO_URI)
db = client_my['kons_new']
collection = db['clinics']

async def fetch_unique_values(field_name):
    return await collection.distinct(field_name)

async def get_sub_types():
    return await fetch_unique_values('Sub_type')

async def send_clinics(client, user_id, district, speciality, sent_clinics, message_id, lang):
    query = {"district_new": district}
    if client.user_data[user_id].get("specialized_clinic", False):
        sub_type_field = f"Sub_type_{lang}" if lang != "en" else "Sub_type"
        query[sub_type_field] = re.compile(speciality, re.IGNORECASE)
    else:
        query["type"] = speciality

    clinics_cursor = collection.find(query, {
        "_id": 1,
        "name": 1,
        "phone_number": 1,
        "website": 1,
        "place_link": 1,
        "type": 1,
        f"Sub_type_{lang}" if lang != "en" else "Sub_type": 1
    })

    clinics = await clinics_cursor.to_list(length=100)

    unsent_clinics = [clinic for clinic in clinics if clinic['_id'] not in sent_clinics]
    response = messages[lang]["clinic_info"]
    count = 0

    for clinic in unsent_clinics[:3]:
        sub_type = clinic.get(f"Sub_type_{lang}") if lang != "en" else clinic.get("Sub_type")
        response += (
            f"**Name:** {clinic.get('name')}\n"
            f"**Phone:** {clinic.get('phone_number')}\n"
            f"**Website:** [{messages[lang]['website_text']}]({clinic.get('website')})\n"
            f"**Location:** [{messages[lang]['maps_text']}]({clinic.get('place_link')})\n"
            f"**Specialization:** {clinic.get('type')} - {sub_type}\n\n"
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

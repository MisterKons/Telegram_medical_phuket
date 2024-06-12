import re
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Support.credentials import MONGO_URI
from Support.messages_base import messages

client_my = AsyncIOMotorClient(MONGO_URI, maxPoolSize=100)
db = client_my['kons_new']
collection = db['clinics']


async def fetch_unique_values(field_name):
    return await collection.distinct(field_name)


async def get_sub_types():
    return await fetch_unique_values('Sub_type')


async def send_clinics(client, user_id, district, speciality, sent_clinics, message_id, lang, page=0):
    query = {}
    if district is not None:
        query["district_new"] = district
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

    clinics_per_page = 3
    total_clinics = len(clinics)
    total_pages = (total_clinics + clinics_per_page - 1) // clinics_per_page  # округление вверх

    if page >= total_pages:
        page = total_pages - 1
    if page < 0:
        page = 0

    start_index = page * clinics_per_page
    end_index = start_index + clinics_per_page
    clinics_to_show = clinics[start_index:end_index]

    response = messages[lang]["clinic_info"] + f"\n{messages[lang]['page']}" + f" {page + 1} - {total_pages}\n\n"

    for clinic in clinics_to_show:
        sub_type = clinic.get(f"Sub_type_{lang}") if lang != "en" else clinic.get("Sub_type")
        response += (
            f"**Name:** {clinic.get('name')}\n"
            f"**Phone:** {clinic.get('phone_number')}\n"
            f"**Website:** [{messages[lang]['website_text']}]({clinic.get('website')})\n"
            f"**Location:** [{messages[lang]['maps_text']}]({clinic.get('place_link')})\n"
            f"**Specialization:** {clinic.get('type')} - {sub_type}\n\n"
        )

    keyboard = []
    if page > 0:
        keyboard.append(InlineKeyboardButton(messages[lang]["previous"], callback_data="previous_clinics"))
    if end_index < total_clinics:
        keyboard.append(InlineKeyboardButton(messages[lang]["next"], callback_data="next_clinics"))

    reply_markup = InlineKeyboardMarkup([keyboard]) if keyboard else None

    if not clinics_to_show:
        response = messages[lang]["no_more_clinics"]
        keyboard = [
            [InlineKeyboardButton(messages[lang]["try_again"], callback_data="try_again")],
            [InlineKeyboardButton(messages[lang]["stop"], callback_data="stop")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    await client.edit_message_text(user_id, message_id, response, reply_markup=reply_markup)

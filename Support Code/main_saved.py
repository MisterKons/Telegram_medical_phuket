import asyncio
import nest_asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from credentials import API_ID, API_HASH, BOT_TOKEN, MONGO_URI
from messages import messages, lang_choice  # Импортируем сообщения

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['kons_new']
collection = db['clinics']

# Function to fetch unique values from a specified field
def fetch_unique_values(field_name):
    return collection.distinct(field_name)

# Fetch and store available districts and specialities
districts = fetch_unique_values('district_new')
specialities = fetch_unique_values('type')

# Function to create inline keyboard buttons in 2 columns
def create_column_buttons(options, prefix):
    keyboard = []
    for i in range(0, len(options), 2):
        row = [InlineKeyboardButton(option, callback_data=f"{prefix}_{option}") for option in options[i:i + 2]]
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

# Create a new Client instance
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Function to send clinics in batches of 3
async def send_clinics(client, user_id, district, speciality, sent_clinics, message_id, lang):
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
            f"**Specialization:** {clinic.get('type')} - {clinic.get('sub_type')}\n\n"
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

# Start command handler
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    app.user_data[user_id] = {"sent_clinics": set(), "lang": "en", "welcome_message_ids": []}  # Инициализация welcome_message_ids

    # Предлагаем выбрать язык
    lang_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("English", callback_data="lang_en")],
        [InlineKeyboardButton("Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("ไทย", callback_data="lang_th")]
    ])
    welcome_message = await message.reply_text(lang_choice, reply_markup=lang_keyboard)
    app.user_data[user_id]['welcome_message_ids'].append(welcome_message.id)

# Command handler for findclinic
@app.on_message(filters.command("findclinic") & filters.private)
async def find_clinic(client, message):
    user_id = message.from_user.id
    lang = app.user_data[user_id]["lang"]

    # Show district selection
    district_keyboard = create_column_buttons(districts, "district")
    await client.send_message(user_id, messages[lang]["choose_area"], reply_markup=district_keyboard)

# Callback query handler
@app.on_callback_query()
async def handle_callback_query(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if user_id not in app.user_data:
        app.user_data[user_id] = {"sent_clinics": set(), "lang": "en"}

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        app.user_data[user_id]["lang"] = lang
        welcome_message = messages[lang]["welcome"]
        await callback_query.message.edit_text(welcome_message)

    elif data.startswith("district_"):
        district = data.split("_")[1]
        lang = app.user_data[user_id]["lang"]
        await client.send_message(user_id, messages[lang]["chose_district"].format(district=district))

        # Store user data
        app.user_data[user_id]["district_new"] = district

        # Show speciality selection
        speciality_keyboard = create_column_buttons(specialities, "speciality")
        await callback_query.message.edit_text(messages[lang]["choose_speciality"], reply_markup=speciality_keyboard)

    elif data.startswith("speciality_"):
        speciality = data.split("_")[1]
        lang = app.user_data[user_id]["lang"]
        await client.send_message(user_id, messages[lang]["chose_speciality"].format(speciality=speciality))

        # Store user data
        app.user_data[user_id]["type"] = speciality

        # Confirm choices
        district = app.user_data[user_id]["district_new"]
        keyboard = [
            [InlineKeyboardButton(messages[lang]["confirm"], callback_data="confirm"),
             InlineKeyboardButton(messages[lang]["try_again"], callback_data="try_again")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await callback_query.message.edit_text(
            messages[lang]["confirm_choices"].format(district=district, speciality=speciality),
            reply_markup=reply_markup)

    elif data == "confirm":
        user_data = app.user_data[user_id]
        district = user_data["district_new"]
        speciality = user_data["type"]
        lang = user_data["lang"]

        # Fetch and send clinics, editing the previous message
        await send_clinics(client, user_id, district, speciality, user_data["sent_clinics"], callback_query.message.id,
                           lang)

    elif data == "send_more":
        user_data = app.user_data[user_id]
        district = user_data["district_new"]
        speciality = user_data["type"]
        lang = user_data["lang"]

        # Send more clinics, editing the previous message
        await send_clinics(client, user_id, district, speciality, user_data["sent_clinics"], callback_query.message.id,
                           lang)

    elif data == "try_again":
        user_data = app.user_data[user_id]
        lang = user_data["lang"]

        # Restart from district selection
        district_keyboard = create_column_buttons(districts, "district")
        await callback_query.message.edit_text(messages[lang]["choose_area"], reply_markup=district_keyboard)

    elif data == "stop":
        lang = app.user_data[user_id]["lang"]
        await client.edit_message_text(user_id, callback_query.message.id, messages[lang]["goodbye"])

# Initialize user_data
app.user_data = {}

# Run the bot
async def main():
    async with app:
        print("Bot is running...")
        await idle()

# Start the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

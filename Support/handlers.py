from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Support.database import send_clinics
from Support.messages import messages, lang_choice
from Support.utils import create_column_buttons


def translate_to_english(value, category, lang):
    if category == "districts":
        return next((k for k, v in zip(messages["en"]["districts"], messages[lang]["districts"]) if v == value), value)
    elif category == "clinic_types":
        return next((k for k, v in zip(messages["en"]["clinic_types"], messages[lang]["clinic_types"]) if v == value),
                    value)


def initialize_user_data(app, user_id):
    if user_id not in app.user_data:
        app.user_data[user_id] = {"sent_clinics": set(), "lang": "en", "welcome_message_ids": []}
    return app.user_data[user_id]


def create_lang_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("English", callback_data="lang_en")],
        [InlineKeyboardButton("Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("ไทย", callback_data="lang_th")]
    ])


def create_district_keyboard(lang):
    return create_column_buttons(messages[lang]["districts"], "district")


def create_speciality_keyboard(lang):
    return create_column_buttons(messages[lang]["clinic_types"], "speciality")


def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start(client, message):
        user_id = message.from_user.id
        initialize_user_data(app, user_id)

        lang_keyboard = create_lang_keyboard()
        welcome_message = await message.reply_text(lang_choice, reply_markup=lang_keyboard)
        app.user_data[user_id]['welcome_message_ids'].append(welcome_message.id)

    @app.on_message(filters.command("findclinic") & filters.private)
    async def find_clinic(client, message):
        user_id = message.from_user.id
        user_data = initialize_user_data(app, user_id)

        district_keyboard = create_district_keyboard(user_data["lang"])
        await client.send_message(user_id, messages[user_data["lang"]]["choose_area"], reply_markup=district_keyboard)

    @app.on_callback_query()
    async def handle_callback_query(client, callback_query):
        data = callback_query.data
        user_id = callback_query.from_user.id
        user_data = initialize_user_data(app, user_id)
        lang = user_data["lang"]

        if data.startswith("lang_"):
            lang = data.split("_")[1]
            user_data["lang"] = lang
            welcome_message = messages[lang]["welcome"]
            await callback_query.message.edit_text(welcome_message)

        elif data.startswith("district_"):
            district = data.split("_")[1]
            district_name = next((d for d in messages[lang]["districts"] if d == district), None)
            if district_name:
                await client.send_message(user_id, messages[lang]["chose_district"].format(district=district_name))
                user_data["district_new"] = district_name

                speciality_keyboard = create_speciality_keyboard(lang)
                await callback_query.message.edit_text(messages[lang]["choose_speciality"],
                                                       reply_markup=speciality_keyboard)
            else:
                await client.send_message(user_id, messages[lang]["invalid_district"])

        elif data.startswith("speciality_"):
            speciality = data.split("_")[1]
            speciality_name = next((s for s in messages[lang]["clinic_types"] if s == speciality), None)
            if speciality_name:
                if speciality_name == messages[lang]["clinic_types"][3]:  # Specialized Clinic
                    await client.send_message(user_id, messages[lang]["enter_speciality"])
                    user_data.update({"awaiting_speciality_input": True, "specialized_clinic": True})
                else:
                    await client.send_message(user_id,
                                              messages[lang]["chose_speciality"].format(speciality=speciality_name))
                    user_data.update({"type": speciality_name, "specialized_clinic": False})

                    district = user_data["district_new"]
                    keyboard = [[InlineKeyboardButton(messages[lang]["confirm"], callback_data="confirm"),
                                 InlineKeyboardButton(messages[lang]["try_again"], callback_data="try_again")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await callback_query.message.edit_text(
                        messages[lang]["confirm_choices"].format(district=district, speciality=speciality_name),
                        reply_markup=reply_markup)
            else:
                await client.send_message(user_id, messages[lang]["invalid_speciality"])

        elif data == "confirm":
            district = translate_to_english(user_data["district_new"], "districts", lang)
            speciality = translate_to_english(user_data["type"], "clinic_types", lang)
            await send_clinics(client, user_id, district, speciality, user_data["sent_clinics"],
                               callback_query.message.id, lang)

        elif data == "send_more":
            district = translate_to_english(user_data["district_new"], "districts", lang)
            speciality = translate_to_english(user_data["type"], "clinic_types", lang)
            await send_clinics(client, user_id, district, speciality, user_data["sent_clinics"],
                               callback_query.message.id, lang)

        elif data == "try_again":
            district_keyboard = create_district_keyboard(lang)
            await callback_query.message.edit_text(messages[lang]["choose_area"], reply_markup=district_keyboard)

        elif data == "stop":
            await client.edit_message_text(user_id, callback_query.message.id, messages[lang]["goodbye"])

    @app.on_message(filters.text & filters.private)
    async def handle_speciality_input(client, message):
        user_id = message.from_user.id
        user_data = initialize_user_data(app, user_id)
        if user_data.get("awaiting_speciality_input"):
            speciality = message.text
            user_data.update({"type": speciality, "awaiting_speciality_input": False})
            lang = user_data["lang"]

            await client.send_message(user_id, messages[lang]["chose_speciality"].format(speciality=speciality))

            district = user_data["district_new"]
            keyboard = [[InlineKeyboardButton(messages[lang]["confirm"], callback_data="confirm"),
                         InlineKeyboardButton(messages[lang]["try_again"], callback_data="try_again")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.send_message(user_id, messages[lang]["confirm_choices"].format(district=district,
                                                                                        speciality=speciality),
                                      reply_markup=reply_markup)


def create_column_buttons(options, prefix):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(option, callback_data=f"{prefix}_{option}") for option in options[i:i + 2]]
        for i in range(0, len(options), 2)
    ])

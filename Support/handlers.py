from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .database import send_clinics
from .messages_base import messages, lang_choice
from .utils import translate_to_english, create_column_buttons
from .feedback_handler import feedback_handler, handle_feedback_input

def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start(client, message):
        user_id = message.from_user.id
        client.user_data[user_id] = {"sent_clinics": set(), "lang": "en", "welcome_message_ids": []}

        # Offer language selection
        lang_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("English", callback_data="lang_en")],
            [InlineKeyboardButton("Русский", callback_data="lang_rus")],
            [InlineKeyboardButton("Deutsch", callback_data="lang_ger")],
            [InlineKeyboardButton("ไทย", callback_data="lang_thai")]
        ])
        welcome_message = await message.reply_text(lang_choice, reply_markup=lang_keyboard)
        client.user_data[user_id]['welcome_message_ids'].append(welcome_message.id)

    @app.on_message(filters.command("findclinic") & filters.private)
    async def find_clinic(client, message):
        user_id = message.from_user.id
        if user_id not in client.user_data:
            client.user_data[user_id] = {"sent_clinics": set(), "lang": "en"}
        lang = client.user_data[user_id]["lang"]

        # Show district selection
        district_keyboard = create_column_buttons(messages[lang]["districts"], "district")
        await client.send_message(user_id, messages[lang]["choose_area"], reply_markup=district_keyboard)

    @app.on_message(filters.command("feedback") & filters.private)
    async def feedback(client, message):
        await feedback_handler(client, message)

    @app.on_message(filters.text & filters.private)
    async def handle_text_message(client, message):
        user_id = message.from_user.id
        if client.user_data.get(user_id, {}).get("awaiting_feedback"):
            await handle_feedback_input(client, message)
        elif client.user_data.get(user_id, {}).get("awaiting_speciality_input"):
            await handle_speciality_input(client, message)
        # Add other text message handling here if needed

    @app.on_callback_query()
    async def handle_callback_query(client, callback_query):
        data = callback_query.data
        user_id = callback_query.from_user.id

        if user_id not in client.user_data:
            client.user_data[user_id] = {"sent_clinics": set(), "lang": "en"}

        lang = client.user_data[user_id]["lang"]

        if data.startswith("lang_"):
            lang = data.split("_")[1]
            client.user_data[user_id]["lang"] = lang
            welcome_message = messages[lang]["welcome"]
            await callback_query.message.edit_text(welcome_message)

        elif data.startswith("district_"):
            district = data.split("_")[1]
            district_name = next((d for d in messages[lang]["districts"] if d == district), None)
            if district_name:
                await client.send_message(user_id, messages[lang]["chose_district"].format(district=district_name))

                # Store user data
                client.user_data[user_id]["district_new"] = district_name

                # Show speciality selection
                speciality_keyboard = create_column_buttons(messages[lang]["clinic_types"], "speciality")
                await callback_query.message.edit_text(messages[lang]["choose_speciality"], reply_markup=speciality_keyboard)
            else:
                await client.send_message(user_id, messages[lang]["invalid_district"])

        elif data.startswith("speciality_"):
            speciality = data.split("_")[1]
            speciality_name = next((s for s in messages[lang]["clinic_types"] if s == speciality), None)
            if speciality_name:
                if speciality_name == messages[lang]["clinic_types"][3]:  # Use translated value for "Specialized Clinic"
                    await client.send_message(user_id, messages[lang]["enter_speciality"])
                    client.user_data[user_id]["awaiting_speciality_input"] = True
                    client.user_data[user_id]["specialized_clinic"] = True
                else:
                    await client.send_message(user_id, messages[lang]["chose_speciality"].format(speciality=speciality_name))

                    # Store user data
                    client.user_data[user_id]["type"] = speciality_name
                    client.user_data[user_id]["specialized_clinic"] = False

                    # Confirm choices
                    district = client.user_data[user_id]["district_new"]
                    keyboard = [
                        [InlineKeyboardButton(messages[lang]["confirm"], callback_data="confirm"),
                         InlineKeyboardButton(messages[lang]["try_again"], callback_data="try_again")]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await callback_query.message.edit_text(
                        messages[lang]["confirm_choices"].format(district=district, speciality=speciality_name),
                        reply_markup=reply_markup)
            else:
                await client.send_message(user_id, messages[lang]["invalid_speciality"])

        elif data == "confirm":
            user_data = client.user_data[user_id]
            district = user_data["district_new"]
            speciality = user_data["type"]
            lang = user_data["lang"]

            # Translate district and speciality to English
            translated_district = translate_to_english(district, "districts", lang)
            translated_speciality = translate_to_english(speciality, "clinic_types", lang)

            # Fetch and send clinics, editing the previous message
            await send_clinics(client, user_id, translated_district, translated_speciality, user_data["sent_clinics"], callback_query.message.id, lang)

        elif data == "send_more":
            user_data = client.user_data[user_id]
            district = user_data["district_new"]
            speciality = user_data["type"]
            lang = user_data["lang"]

            # Translate district and speciality to English
            translated_district = translate_to_english(district, "districts", lang)
            translated_speciality = translate_to_english(speciality, "clinic_types", lang)

            # Send more clinics, editing the previous message
            await send_clinics(client, user_id, translated_district, translated_speciality, user_data["sent_clinics"], callback_query.message.id, lang)

        elif data == "try_again":
            user_data = client.user_data[user_id]
            lang = user_data["lang"]

            # Restart from district selection
            district_keyboard = create_column_buttons(messages[lang]["districts"], "district")
            await callback_query.message.edit_text(messages[lang]["choose_area"], reply_markup=district_keyboard)

        elif data == "stop":
            lang = client.user_data[user_id]["lang"]
            await client.edit_message_text(user_id, callback_query.message.id, messages[lang]["goodbye"])

        elif data == "start_over":
            await start(client, callback_query.message)

    async def handle_speciality_input(client, message):
        user_id = message.from_user.id
        if user_id in client.user_data and client.user_data[user_id].get("awaiting_speciality_input"):
            speciality = message.text

            client.user_data[user_id]["type"] = speciality
            client.user_data[user_id]["awaiting_speciality_input"] = False
            lang = client.user_data[user_id]["lang"]

            await client.send_message(user_id, messages[lang]["chose_speciality"].format(speciality=speciality))

            # Confirm choices
            district = client.user_data[user_id]["district_new"]
            keyboard = [
                [InlineKeyboardButton(messages[lang]["confirm"], callback_data="confirm"),
                 InlineKeyboardButton(messages[lang]["try_again"], callback_data="try_again")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await client.send_message(
                user_id,
                messages[lang]["confirm_choices"].format(district=district, speciality=speciality),
                reply_markup=reply_markup
            )

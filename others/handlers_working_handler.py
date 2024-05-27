from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .database import send_clinics
from .messages_base import messages, lang_choice
from .utils import create_column_buttons

def translate_to_english(value, category, lang):
    if category == "districts":
        return next((k for k, v in zip(messages["en"]["districts"], messages[lang]["districts"]) if v == value), value)
    elif category == "clinic_types":
        return next((k for k, v in zip(messages["en"]["clinic_types"], messages[lang]["clinic_types"]) if v == value), value)

def register_handlers(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start(client, message):
        user_id = message.from_user.id
        app.user_data[user_id] = {"sent_clinics": set(), "lang": "en", "welcome_message_ids": []}

        # Предлагаем выбрать язык
        lang_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("English", callback_data="lang_en")],
            [InlineKeyboardButton("Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("Deutsch", callback_data="lang_de")],
            [InlineKeyboardButton("ไทย", callback_data="lang_th")]
        ])
        welcome_message = await message.reply_text(lang_choice, reply_markup=lang_keyboard)
        app.user_data[user_id]['welcome_message_ids'].append(welcome_message.id)

    @app.on_message(filters.command("findclinic") & filters.private)
    async def find_clinic(client, message):
        user_id = message.from_user.id
        if user_id not in app.user_data:
            app.user_data[user_id] = {"sent_clinics": set(), "lang": "en"}
        lang = app.user_data[user_id]["lang"]
    

    @app.on_message(filters.command("feedback") & filters.private)
    async def feedback(client, message):
        print("Feedback handler triggered")  # Debug log
        user_id = message.from_user.id
        lang = app.user_data.get(user_id, {}).get("lang", "en")
        
        feedback_message_user = messages[lang]["feedback_user"]
        feedback_message_owner = messages[lang]["feedback_owner"]
        
        # Отправляем сообщение пользователю
        await client.send_message(user_id, feedback_message_user)

        # Пересылаем сообщение координатору
        coordinator_username = "konstantinMrk"
        forward_message = f"User {user_id} sent feedback.\n\n{feedback_message_owner}"
        await client.send_message(f"@{coordinator_username}", forward_message)

        # Show district selection
        district_keyboard = create_column_buttons(messages[lang]["districts"], "district")
        await client.send_message(user_id, messages[lang]["choose_area"], reply_markup=district_keyboard)

    @app.on_callback_query()
    async def handle_callback_query(client, callback_query):
        data = callback_query.data
        user_id = callback_query.from_user.id

        if user_id not in app.user_data:
            app.user_data[user_id] = {"sent_clinics": set(), "lang": "en"}

        lang = app.user_data[user_id]["lang"]

        if data.startswith("lang_"):
            lang = data.split("_")[1]
            app.user_data[user_id]["lang"] = lang
            welcome_message = messages[lang]["welcome"]
            await callback_query.message.edit_text(welcome_message)

        elif data.startswith("district_"):
            district = data.split("_")[1]
            district_name = next((d for d in messages[lang]["districts"] if d == district), None)
            if district_name:
                await client.send_message(user_id, messages[lang]["chose_district"].format(district=district_name))

                # Store user data
                app.user_data[user_id]["district_new"] = district_name

                # Show speciality selection
                speciality_keyboard = create_column_buttons(messages[lang]["clinic_types"], "speciality")
                await callback_query.message.edit_text(messages[lang]["choose_speciality"], reply_markup=speciality_keyboard)
            else:
                await client.send_message(user_id, messages[lang]["invalid_district"])

        elif data.startswith("speciality_"):
            speciality = data.split("_")[1]
            speciality_name = next((s for s in messages[lang]["clinic_types"] if s == speciality), None)
            if speciality_name:
                if speciality_name == messages[lang]["clinic_types"][3]:  # Используем переведенное значение для "Specialized Clinic"
                    await client.send_message(user_id, messages[lang]["enter_speciality"])
                    app.user_data[user_id]["awaiting_speciality_input"] = True
                    app.user_data[user_id]["specialized_clinic"] = True
                else:
                    await client.send_message(user_id, messages[lang]["chose_speciality"].format(speciality=speciality_name))

                    # Store user data
                    app.user_data[user_id]["type"] = speciality_name
                    app.user_data[user_id]["specialized_clinic"] = False

                    # Confirm choices
                    district = app.user_data[user_id]["district_new"]
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
            user_data = app.user_data[user_id]
            district = user_data["district_new"]
            speciality = user_data["type"]
            lang = user_data["lang"]

            # Ищем английские значения для district и speciality
            translated_district = translate_to_english(district, "districts", lang)
            translated_speciality = translate_to_english(speciality, "clinic_types", lang)

            # Fetch and send clinics, editing the previous message
            await send_clinics(client, user_id, translated_district, translated_speciality, user_data["sent_clinics"], callback_query.message.id, lang)

        elif data == "send_more":
            user_data = app.user_data[user_id]
            district = user_data["district_new"]
            speciality = user_data["type"]
            lang = user_data["lang"]

            # Ищем английские значения для district и speciality
            translated_district = translate_to_english(district, "districts", lang)
            translated_speciality = translate_to_english(speciality, "clinic_types", lang)

            # Send more clinics, editing the previous message
            await send_clinics(client, user_id, translated_district, translated_speciality, user_data["sent_clinics"], callback_query.message.id, lang)

        elif data == "try_again":
            user_data = app.user_data[user_id]
            lang = user_data["lang"]

            # Restart from district selection
            district_keyboard = create_column_buttons(messages[lang]["districts"], "district")
            await callback_query.message.edit_text(messages[lang]["choose_area"], reply_markup=district_keyboard)

        elif data == "stop":
            lang = app.user_data[user_id]["lang"]
            await client.edit_message_text(user_id, callback_query.message.id, messages[lang]["goodbye"])

    @app.on_message(filters.text & filters.private)
    async def handle_speciality_input(client, message):
        user_id = message.from_user.id
        if user_id in app.user_data and app.user_data[user_id].get("awaiting_speciality_input"):
            speciality = message.text

            app.user_data[user_id]["type"] = speciality
            app.user_data[user_id]["awaiting_speciality_input"] = False
            lang = app.user_data[user_id]["lang"]

            await client.send_message(user_id, messages[lang]["chose_speciality"].format(speciality=speciality))

            # Confirm choices
            district = app.user_data[user_id]["district_new"]
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

def create_column_buttons(options, prefix):
    keyboard = []
    for i in range(0, len(options), 2):
        row = [InlineKeyboardButton(option, callback_data=f"{prefix}_{option}") for option in options[i:i + 2]]
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

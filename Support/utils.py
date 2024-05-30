from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .messages_base import messages

# Function to create inline keyboard buttons in 2 columns
def create_column_buttons(options, prefix):
    keyboard = []
    for i in range(0, len(options), 2):
        row = [InlineKeyboardButton(option, callback_data=f"{prefix}_{option}") for option in options[i:i + 2]]
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

# Function to translate values to English
def translate_to_english(value, category, lang):
    if category == "districts":
        return next((k for k, v in zip(messages["en"]["districts"], messages[lang]["districts"]) if v == value), value)
    elif category == "clinic_types":
        return next((k for k, v in zip(messages["en"]["clinic_types"], messages[lang]["clinic_types"]) if v == value), value)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Function to create inline keyboard buttons in 2 columns
def create_column_buttons(options, prefix):
    keyboard = []
    for i in range(0, len(options), 2):
        row = [InlineKeyboardButton(option, callback_data=f"{prefix}_{option}") for option in options[i:i + 2]]
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

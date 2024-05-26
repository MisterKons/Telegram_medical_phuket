import asyncio
import nest_asyncio
from pyrogram import Client, idle
from Support.credentials import API_ID, API_HASH, BOT_TOKEN
from Support.handlers import register_handlers

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Create a new Client instance
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Initialize user_data dictionary
app.user_data = {}

# Register handlers
register_handlers(app)


# Run the bot
async def main():
    async with app:
        print("Bot is running...")
        await idle()


# Start the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

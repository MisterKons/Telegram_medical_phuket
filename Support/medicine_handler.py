# support/medicine_handler.py

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def register_medicine_handlers(app):
    @app.on_message(filters.command("medicine") & filters.private)
    async def medicine(client, message):
        user_id = message.from_user.id
        client.user_data[user_id] = {"awaiting_medicine_input": True}

        instruction_message = "📝 Пожалуйста, введите название лекарства, которое вы ищете. Не используйте специальные символы, такие как $#@!., и т.д. 👇\n\n🔎 Поиск может занять до 10 секунд."
        await message.reply_text(instruction_message)

    @app.on_message(filters.private)
    async def handle_user_input(client, message):
        user_id = message.from_user.id
        if user_id in client.user_data and client.user_data[user_id].get("awaiting_medicine_input"):
            medicine_name = message.text
            client.user_data[user_id]["awaiting_medicine_input"] = False

            # Validate medicine name
            if re.match("^[A-Za-z0-9А-Яа-я]+$", medicine_name):
                # Inform the user about the search process
                await message.reply_text("🔄 Выполняется поиск аналогов лекарства... Пожалуйста, подождите.")
                
                # Perform the search
                analogs = search_drug_analogs(medicine_name)
                if analogs:
                    response = "🔍 Найдены следующие аналоги:\n\n"
                    for link, snippet in analogs:
                        response += f"🔗 [{snippet}]({link})\n\n"
                else:
                    response = "❌ Извините, аналогов не найдено."
            else:
                response = "⚠️ Неправильное название лекарства. Пожалуйста, попробуйте еще раз, избегая специальных символов."

            await message.reply_text(response, disable_web_page_preview=True)

    def search_drug_analogs(russian_drug_name):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        try:
            driver.get('https://drugsearch.carrd.co/')
            time.sleep(2)
            search_box = driver.find_element(By.CSS_SELECTOR, 'input.gsc-input')
            search_query = f"{russian_drug_name} аналог, эквивалент, замена в аптеке Таиланда"
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)
            results = driver.find_elements(By.CSS_SELECTOR, '.gsc-webResult .gsc-result')
            analogs = []
            for result in results[:3]:
                title_element = result.find_element(By.CSS_SELECTOR, '.gs-title a')
                snippet_element = result.find_element(By.CSS_SELECTOR, '.gs-snippet')
                analog_link = title_element.get_attribute('href')
                analog_snippet = snippet_element.text
                analogs.append((analog_link, analog_snippet))
            return analogs
        finally:
            driver.quit()

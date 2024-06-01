import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def register_medicine_handlers(client, message):
    user_id = message.from_user.id
    client.user_data[user_id] = client.user_data.get(user_id, {})
    instruction_message = ("📝 Пожалуйста, введите название лекарства, которое вы ищете. Не используйте специальные "
                           "символы, такие как $#@!., и т.д. 👇\n\n🔎 Поиск может занять до 10 секунд.")
    client.user_data[user_id]["awaiting_medicine_input"] = True

    await client.send_message(user_id, instruction_message)


async def handle_medicine_input(client, message):
    user_id = message.from_user.id
    if user_id in client.user_data and client.user_data[user_id].get("awaiting_medicine_input"):
        medicine_name = message.text
        client.user_data[user_id]["awaiting_medicine_input"] = False

        if re.match("^[A-Za-z0-9А-Яа-я]+$", medicine_name):
            await message.reply_text("🔄 Выполняется поиск аналогов лекарства... Пожалуйста, подождите.")
            try:
                analogs = await search_drug_analogs(medicine_name)
                if analogs:
                    response = "🔍 Найдены следующие аналоги:\n\n"
                    for link, snippet in analogs:
                        response += f"🔗 [{snippet}]({link})\n\n"
                else:
                    response = "❌ Извините, аналогов не найдено."
            except Exception as e:
                logger.error(f"Error occurred during drug analog search: {e}")
                response = "⚠️ Произошла ошибка при поиске аналогов лекарства. Пожалуйста, попробуйте позже."

        else:
            response = "⚠️ Неправильное название лекарства. Пожалуйста, попробуйте еще раз, избегая специальных символов."

        await client.send_message(user_id, response, disable_web_page_preview=True)


async def search_drug_analogs(russian_drug_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get('https://drugsearch.carrd.co/')
        await asyncio.sleep(3)  # Ensure the page loads completely

        search_box = driver.find_element(By.CSS_SELECTOR, 'input.gsc-input')
        search_query = f"{russian_drug_name} аналог, эквивалент, замена в аптеке Таиланда"
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        await asyncio.sleep(3)  # Wait for search results to load

        results = driver.find_elements(By.CSS_SELECTOR, '.gsc-webResult .gsc-result')
        analogs = []
        for result in results[:3]:  # Limit to top 3 results
            try:
                title_element = result.find_element(By.CSS_SELECTOR, '.gs-title a')
                snippet_element = result.find_element(By.CSS_SELECTOR, '.gs-snippet')
                analog_link = title_element.get_attribute('href')
                analog_snippet = snippet_element.text
                analogs.append((analog_link, analog_snippet))
            except Exception as e:
                logger.error(f"Error parsing search result: {e}")
                continue
        return analogs
    finally:
        driver.quit()

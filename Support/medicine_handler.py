import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import asyncio
import concurrent.futures
from transformers import pipeline
from others.database import get_saved_analog, save_drug_analog

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание пайплайна для вопросов и ответов с поддержкой русского языка
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2",
                       tokenizer="deepset/roberta-base-squad2")


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

        saved_analog = await get_saved_analog(medicine_name)
        if saved_analog:
            response = (f"🔍 Найден следующий аналог для препарата {medicine_name}:\n\n"
                        f"{saved_analog['text']}\n"
                        f"[Ссылка на источник]({saved_analog['link']})\n\n")
            await client.send_message(user_id, response, disable_web_page_preview=True)
            return

        if re.match("^[A-Za-z0-9А-Яа-я]+$", medicine_name):
            await message.reply_text("🔄 Выполняется поиск аналогов лекарства... Пожалуйста, подождите.")
            try:
                analog = await search_drug_analogs(medicine_name)
                if analog:
                    client.user_data[user_id]["current_medicine"] = medicine_name
                    client.user_data[user_id]["current_analog"] = analog

                    response = (f"🔍 Найден следующий аналог для препарата {medicine_name}:\n\n"
                                f"{analog['text']}\n"
                                f"[Ссылка на источник]({analog['link']})\n\n"
                                f"Этот ответ был полезен? [Да](feedback_correct) / [Нет](feedback_incorrect)")

                else:
                    response = "❌ Извините, аналогов не найдено."
            except Exception as e:
                logger.error(f"Error occurred during drug analog search: {e}")
                response = "⚠️ Произошла ошибка при поиске аналогов лекарства. Пожалуйста, попробуйте позже."

        else:
            response = ("⚠️ Неправильное название лекарства. Пожалуйста, попробуйте еще раз, избегая специальных "
                        "символов.\n💊Вводите в чат только название лекарстава. \n🔁Попробовать еще раз /medicine")

        await client.send_message(user_id, response, disable_web_page_preview=True)


async def search_drug_analogs(russian_drug_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get('https://drugsearch.carrd.co/')
        await asyncio.sleep(2)  # Ensure the page loads completely

        search_box = driver.find_element(By.CSS_SELECTOR, 'input.gsc-input')
        search_query = f"{russian_drug_name} аналог в Таиланде"
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        await asyncio.sleep(2)  # Wait for search results to load

        results = driver.find_elements(By.CSS_SELECTOR, '.gsc-webResult .gsc-result')
        best_analog = None
        highest_score = 0

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_result = {executor.submit(process_result, result, russian_drug_name): result for result in
                                results[:5]}  # Limit to top 5 results

            for future in concurrent.futures.as_completed(future_to_result):
                try:
                    analog = future.result()
                    if analog and analog['score'] > highest_score:
                        highest_score = analog['score']
                        best_analog = analog
                except Exception as e:
                    logger.error(f"Error processing result: {e}")
                    continue

        return best_analog
    finally:
        driver.quit()


def process_result(result, russian_drug_name):
    try:
        title_element = result.find_element(By.CSS_SELECTOR, '.gs-title a')
        snippet_element = result.find_element(By.CSS_SELECTOR, '.gs-snippet')
        analog_link = title_element.get_attribute('href')
        analog_snippet = snippet_element.text

        # Используем модель для вопросов и ответов
        answer = qa_pipeline(question=f"Какой аналог {russian_drug_name} в Таиланде?", context=analog_snippet)
        answer_text = extract_full_sentence(analog_snippet, answer['answer'])
        return {"link": analog_link, "text": answer_text, "score": answer['score']}
    except Exception as e:
        logger.error(f"Error processing result: {e}")
        return None


def extract_full_sentence(context, answer):
    # Простая функция для извлечения полного предложения, содержащего ответ
    sentences = context.split('. ')
    for sentence in sentences:
        if answer in sentence:
            return sentence.strip()
    return answer  # Возвращаем ответ, если предложение не найдено

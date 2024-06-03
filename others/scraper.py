import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from transliterate import translit
import concurrent.futures
import time

def transliterate_medicine(name_medicine):
    # Транслитерация названия лекарства с русского на английский
    transliterated_name = translit(name_medicine, 'ru', reversed=True)
    print(f"Transliterated medicine name: {transliterated_name}")
    return transliterated_name

def scrape_alternatives_sync(medicine_name):
    # Транслитерация названия лекарства
    transliterated_name = transliterate_medicine(medicine_name)
    
    # Формирование URL для запроса
    url = f"https://pillintrip.com/search_analog_ru-{transliterated_name}_in_thailand"
    
    # Настройка Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Открытие URL
    driver.get(url)
    time.sleep(5)  # Подождем, пока страница полностью загрузится

    try:
        # Поиск необходимого текста
        right_side_bar_content = driver.find_element(By.CLASS_NAME, 'right_side_bar_content1')
        
        h1_tag = right_side_bar_content.find_element(By.TAG_NAME, 'h1')
        analog_search_info = right_side_bar_content.find_element(By.CLASS_NAME, 'analog_search_info')
        
        h1_text = h1_tag.text.strip()
        analog_info_text = analog_search_info.text.strip()
        
        driver.quit()
        return h1_text, analog_info_text
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

async def scrape_alternatives_async(medicine_name):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, scrape_alternatives_sync, medicine_name)
    return result

async def main(medicine_names):
    tasks = [scrape_alternatives_async(name) for name in medicine_names]
    results = await asyncio.gather(*tasks)
    for name, result in zip(medicine_names, results):
        if result:
            h1_text, analog_info_text = result
            print(f"Medicine Name: {name}")
            print(f"H1 Text: {h1_text}")
            print(f"Analog Info: {analog_info_text}")
        else:
            print(f"Medicine Name: {name}")
            print("No data found or an error occurred.")

# Пример использования
medicine_names = ["Ибупрофен"]
asyncio.run(main(medicine_names))

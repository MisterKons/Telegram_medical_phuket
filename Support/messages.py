lang_choice = """
# 🌐 Please choose your language  

- 🇺🇸 **English**  

- 🇷🇺 **Пожалуйста, выберите язык**  

- 🇩🇪 **Bitte wählen Sie Ihre Sprache** 

- 🇹🇭 **กรุณาเลือกภาษาของคุณ**  
"""

messages = {
    "en": {
        "welcome": "👋 Welcome to Phuket Clinic Finder Bot! 🌴\n\nThis bot helps you find the best medical clinics in Phuket. \nTo start, use one of the commands:\n\n/start - Choose language and first step\n/findclinic - Start searching for clinics by districts\n/medicine - Under development\n/insurance - Under development\n/feedback - Under development\n\nWe hope you enjoy our service. Please use the feedback command to send us feedback or recommendations. We are happy to improve with your help. For recommendations and complaints, contact @konstaninMrK 🏥✨",
        "choose_area": "Please choose the area where you want to find a clinic:",
        "choose_speciality": "Please choose the specialization of the clinic:",
        "clinic_info": "Here are the clinics matching your criteria:\n\n",
        "no_more_clinics": "No more clinics available.",
        "try_again": "Try Again",
        "stop": "Stop",
        "goodbye": "Thank you for using our bot! Goodbye!",
        "confirm_choices": "You chose district: {district} and specialization: {speciality}\nIs this information correct?",
        "confirm": "Confirm",
        "show_more": "Show More",
        "website_text": "Company website",
        "maps_text": "Company Google Maps location",
        "chose_district": "You chose district: {district}",
        "chose_speciality": "You chose specialization: {speciality}",
        "enter_speciality": "Please enter the speciality you are looking for:",
        "clinic_types": ["Medical Clinic", "Dental Clinic", "Hospital", "Specialized Clinic", "Wellness Clinic",
                         "Physical Therapy Clinic", "Laboratory"],
        "districts": ["Bang Tao", "Chalong", "Kamala", "Karon", "Kata", "Kathu", "Patong", "Phuket Town", "Rawai",
                      "Thalang"]
    },
    "ru": {
        "welcome": "👋 Добро пожаловать в бота для поиска клиник в Пхукете! 🌴\n\nЭтот бот поможет вам найти лучшие медицинские клиники в Пхукете. \nЧтобы начать, используйте одну из команд:\n\n/start - Выберите язык и первый шаг\n/findclinic - Начните поиск клиник по районам\n/medicine - В разработке\n/insurance - В разработке\n/feedback - В разработке\n\nНадеемся, вам понравится наш сервис. Пожалуйста, используйте команду обратной связи, чтобы отправить нам отзывы или рекомендации. Мы рады улучшить его с вашей помощью. Для рекомендаций и жалоб свяжитесь с @konstaninMrK 🏥✨",
        "choose_area": "Пожалуйста, выберите ваш район:",
        "choose_speciality": "Пожалуйста, выберите вашу специальность:",
        "clinic_info": "Вот клиники, соответствующие вашим критериям:\n\n",
        "no_more_clinics": "Больше нет клиник.",
        "try_again": "Попробовать снова",
        "stop": "Остановить",
        "goodbye": "Спасибо за использование нашего бота! До свидания!",
        "confirm_choices": "Вы выбрали район: {district} и специальность: {speciality}\nВерна ли эта информация?",
        "confirm": "Подтвердить",
        "show_more": "Показать ещё",
        "website_text": "Сайт компании",
        "maps_text": "Расположение на Google Maps",
        "chose_district": "Вы выбрали район: {district}",
        "chose_speciality": "Вы выбрали специальность: {speciality}",
        "enter_speciality": "Пожалуйста, введите специальность, которую вы ищете:",
        "clinic_types": ["Медицинская клиника", "Стоматологическая клиника", "Больница", "Специализированная клиника",
                         "Клиника здоровья", "Клиника физиотерапии", "Лаборатория"],
        "districts": ["Банг Тао", "Чалонг", "Камала", "Карон", "Ката", "Кату", "Патонг", "Пхукет Таун", "Равай",
                      "Таланг"]
    },
    "de": {
        "welcome": "👋 Willkommen beim Phuket Clinic Finder Bot! 🌴\n\nDieser Bot hilft Ihnen, die besten medizinischen Kliniken in Phuket zu finden. \nUm zu starten, verwenden Sie einen der Befehle:\n\n/start - Sprache wählen und erster Schritt\n/findclinic - Beginnen Sie mit der Suche nach Kliniken nach Bezirken\n/medicine - In Entwicklung\n/insurance - In Entwicklung\n/feedback - In Entwicklung\n\nWir hoffen, dass Ihnen unser Service gefällt. Bitte nutzen Sie den Feedback-Befehl, um uns Feedback oder Empfehlungen zu senden. Wir freuen uns, mit Ihrer Hilfe besser zu werden. Für Empfehlungen und Beschwerden kontaktieren Sie @konstaninMrK 🏥✨",
        "choose_area": "Bitte wählen Sie das Gebiet, in dem Sie eine Klinik finden möchten:",
        "choose_speciality": "Bitte wählen Sie die Spezialisierung der Klinik:",
        "clinic_info": "Hier sind die Kliniken, die Ihren Kriterien entsprechen:\n\n",
        "no_more_clinics": "Keine weiteren Kliniken verfügbar.",
        "try_again": "Erneut versuchen",
        "stop": "Stoppen",
        "goodbye": "Danke, dass Sie unseren Bot genutzt haben! Auf Wiedersehen!",
        "confirm_choices": "Sie haben Gebiet: {district} und Spezialisierung: {speciality} gewählt\nIst diese Information korrekt?",
        "confirm": "Bestätigen",
        "show_more": "Mehr anzeigen",
        "website_text": "Unternehmenswebsite",
        "maps_text": "Standort auf Google Maps",
        "chose_district": "Sie haben das Gebiet gewählt: {district}",
        "chose_speciality": "Sie haben die Spezialisierung gewählt: {speciality}",
        "enter_speciality": "Bitte geben Sie die gesuchte Spezialisierung ein:",
        "clinic_types": ["Allgemeinarztpraxis", "Zahnarztpraxis", "Krankenhaus", "Spezialisierte Klinik",
                         "Wellness-Klinik", "Physiotherapie-Klinik", "Labor"],
        "districts": ["Bang Tao", "Chalong", "Kamala", "Karon", "Kata", "Kathu", "Patong", "Phuket Stadt", "Rawai",
                      "Thalang"]
    },
    "th": {
        "welcome": "👋 ยินดีต้อนรับสู่บอทค้นหาคลินิกในภูเก็ต! 🌴\n\nบอทนี้จะช่วยคุณค้นหาคลินิกทางการแพทย์ที่ดีที่สุดในภูเก็ต \nเริ่มต้นโดยใช้คำสั่ง:\n\n/start - เลือกภาษาและขั้นตอนแรก\n/findclinic - เริ่มค้นหาคลินิกตามเขต\n/medicine - อยู่ระหว่างการพัฒนา\n/insurance - อยู่ระหว่างการพัฒนา\n/feedback - อยู่ระหว่างการพัฒนา\n\nหวังว่าคุณจะพึงพอใจกับบริการของเรา โปรดใช้คำสั่ง feedback เพื่อส่งความคิดเห็นหรือคำแนะนำถึงเรา เรายินดีที่จะพัฒนาบริการของเราด้วยความช่วยเหลือจากคุณ สำหรับคำแนะนำและข้อร้องเรียน ติดต่อ @konstaninMrK 🏥✨",
        "choose_area": "โปรดเลือกพื้นที่ที่คุณต้องการหาคลินิก:",
        "choose_speciality": "โปรดเลือกความเชี่ยวชาญของคลินิก:",
        "clinic_info": "นี่คือคลินิกที่ตรงกับเกณฑ์ของคุณ:\n\n",
        "no_more_clinics": "ไม่มีคลินิกเพิ่มเติม",
        "try_again": "ลองอีกครั้ง",
        "stop": "หยุด",
        "goodbye": "ขอบคุณที่ใช้บริการบอทของเรา! ลาก่อน!",
        "confirm_choices": "คุณเลือกเขต: {district} และความเชี่ยวชาญ: {speciality}\nข้อมูลนี้ถูกต้องหรือไม่?",
        "confirm": "ยืนยัน",
        "show_more": "แสดงเพิ่มเติม",
        "website_text": "เว็บไซต์ของบริษัท",
        "maps_text": "ตำแหน่งบน Google Maps",
        "chose_district": "คุณเลือกเขต: {district}",
        "chose_speciality": "คุณเลือกความเชี่ยวชาญ: {speciality}",
        "enter_speciality": "โปรดป้อนความเชี่ยวชาญที่คุณกำลังมองหา:",
        "clinic_types": ["คลินิกทั่วไป", "คลินิกทันตกรรม", "โรงพยาบาล", "คลินิกเฉพาะทาง", "คลินิกสุขภาพ",
                         "คลินิกกายภาพบำบัด", "ห้องปฏิบัติการ"],
        "districts": ["บางเทา", "ฉลอง", "กมลา", "กะรน", "กะตะ", "กะทู้", "ป่าตอง", "เมืองภูเก็ต", "ราไวย์", "ถลาง"]
    }
}

lang_choice = """
# 🌐 Please choose your language  

- 🇺🇸 **English**  

- 🇷🇺 **Пожалуйста, выберите язык**  

- 🇩🇪 **Bitte wählen Sie Ihre Sprache** 

- 🇹🇭 **กรุณาเลือกภาษาของคุณ**  
"""

messages = {
    "en": {
        "welcome": "👋 Welcome to Phuket Clinic Finder Bot! 🌴\n\nThis bot helps you find the best medical clinics in "
                   "Phuket. \nTo start, use one of the commands:\n\n/start - Choose language and first "
                   "step\n/findclinic - Start searching for clinics by districts\n/medicine - Here you can find "
                   "medecine substitution\n/insurance - Under development\n/feedback - Suggestions and Feedback\n\nWe "
                   "hope you enjoy our service. Please use the feedback command to send us feedback or "
                   "recommendations. We are happy to improve with your help. For recommendations and complaints, "
                   "contact @konstaninMrK 🏥✨",
        "medicine_sites": "🔍 Here are the sites where you can find information about medicine substitutes:\n\n",
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
        "invalid_district": "Invalid district selected. Please try again.",
        "invalid_speciality": "Invalid speciality selected. Please try again.",
        "districts": ["Bang tao", "Chalong", "Kamala", "Karon", "Kata", "Kathu", "Patong", "Phuket Town", "Rawai",
                      "Thalang"],
        "clinic_types": ["Medical Clinic", "Dental Clinic", "Hospital", "Specialized Clinic", "Wellness Clinic",
                         "Physical Therapy Clinic", "Laboratory"],
        "feedback_user": "😊 **Thank you for planning to send us your feedback.**\n\n"
                         "🔍 It is very important for us to know how we can improve our service.\n\n"
                         "📧 You can send an email to [thesoowai.inc@gmail.com](mailto:thesoowai.inc@gmail.com) "
                         "or send a message in the chat.\n\n"
                         "👇👇👇",
        "thank_you_feedback": "😊 Thank you for your feedback! We appreciate your input.",
        "start_over_prompt": "Would you like to start over?",
        "insurance_about": "General information about insurance and how to use it. \n\n 🦺 [Article](https://telegra.ph/I-Have-Insurance-How-Do-I-Use-It-06-07)",
        "use_buttons": [
            "Please use the buttons, {user_name}.",
            "{user_name}, kindly use the buttons provided.",
            "To proceed, {user_name}, please use the available buttons.",
            "{user_name}, click on the buttons instead of typing."
        ]
    },
    "rus": {
        "welcome": "👋 Добро пожаловать в бота для поиска клиник на Пхукете! 🌴\n\nЭтот бот поможет вам найти лучшие медицинские клиники в Пхукете. \nЧтобы начать, используйте одну из команд:\n\n/start - Выберите язык и первый шаг\n/findclinic - Начать поиск клиник по районам\n/medicine - Найди препараты аналоги не выходя из телеграмма \n/insurance - В разработке\n/feedback - Предложения и Отзывы\n\nНадеемся, вам понравится наш сервис. Пожалуйста, используйте команду обратной связи, чтобы отправить нам отзыв или рекомендации. Мы рады улучшить его с вашей помощью. Для рекомендаций и жалоб свяжитесь с @konstantinMrk 🏥✨",
        "medicine_sites": "🔍 Вот сайты, где вы можете найти информацию об аналогах медикаментов:\n\n",
        "choose_area": "Пожалуйста, выберите район, в котором вы хотите найти клинику:",
        "choose_speciality": "Пожалуйста, выберите специализацию клиники:",
        "clinic_info": "Вот клиники, соответствующие вашим критериям:\n\n",
        "no_more_clinics": "Больше нет клиник.",
        "try_again": "Попробовать снова",
        "stop": "Остановить",
        "goodbye": "Спасибо за использование нашего бота! До свидания!",
        "confirm_choices": "Вы выбрали район: {district} и специализацию: {speciality}\nЭта информация верна?",
        "confirm": "Подтвердить",
        "show_more": "Показать больше",
        "website_text": "Веб-сайт компании",
        "maps_text": "Расположение компании на Google Maps",
        "chose_district": "Вы выбрали район: {district}",
        "chose_speciality": "Вы выбрали специализацию: {speciality}",
        "enter_speciality": "Пожалуйста, введите специализацию, которую вы ищете:",
        "invalid_district": "Выбран неверный район. Пожалуйста, попробуйте снова.",
        "invalid_speciality": "Выбрана неверная специализация. Пожалуйста, попробуйте снова.",
        "districts": ["Банг Тао", "Чалонг", "Камала", "Карон", "Ката", "Кату", "Патонг", "Пхукет Таун", "Раваи",
                      "Таланг"],
        "clinic_types": ["Медицинская клиника", "Стоматологическая клиника", "Больница", "Специализированная клиника",
                         "Оздоровительная клиника", "Клиника физиотерапии", "Лаборатория"],
        "feedback_user": "😊 **Спасибо за ваше намерение отправить нам отзыв.**\n\n"
                         "🔍 Для нас очень важно знать, как мы можем улучшить наш сервис.\n\n"
                         "📧 Вы можете отправить электронное письмо на [thesoowai.inc@gmail.com](mailto:thesoowai.inc@gmail.com) "
                         "или отправить сообщение в чате.\n\n"
                         "👇👇👇",
        "thank_you_feedback": "😊 Спасибо за ваш отзыв! Мы ценим ваш вклад.",
        "start_over_prompt": "Хотите начать сначала?",
        "insurance_about": "Общая информация о страховке и как ей пользоваться. \n\n 🦺 [Статья](https://telegra.ph/U-menya-est-strahovka-kak-ej-vospolzovatsya-06-07)",
        "use_buttons": [
            "Пожалуйста, используйте кнопки, {user_name}.",
            "{user_name}, пожалуйста, используйте предоставленные кнопки.",
            "Чтобы продолжить, {user_name}, пожалуйста, используйте доступные кнопки.",
            "{user_name}, нажмите на кнопки вместо ввода текста."
        ]
    },
    "ger": {
        "welcome": "👋 Willkommen beim Phuket Clinic Finder Bot! 🌴\n\nDieser Bot hilft Ihnen, die besten medizinischen Kliniken in Phuket zu finden. \nUm zu starten, verwenden Sie einen der Befehle:\n\n/start - Sprache auswählen und erster Schritt\n/findclinic - Beginnen Sie mit der Suche nach Kliniken nach Bezirken\n/medicine - Finden Sie Analoga von Arzneimitteln, ohne das Telegramm zu verlassen\n/insurance - In Entwicklung\n/feedback - Vorschläge und Feedback\n\nWir hoffen, dass Sie unseren Service genießen. Bitte verwenden Sie den Feedback-Befehl, um uns Feedback oder Empfehlungen zu senden. Wir freuen uns, mit Ihrer Hilfe zu verbessern. Für Empfehlungen und Beschwerden kontaktieren Sie @konstaninMrK 🏥✨",
        "choose_area": "Bitte wählen Sie den Bereich, in dem Sie eine Klinik finden möchten:",
        "medicine_sites": "🔍 Hier sind die Websites, auf denen Sie Informationen zu Arzneimittelersatzstoffen finden können:\n\n",
        "choose_speciality": "Bitte wählen Sie die Spezialisierung der Klinik:",
        "clinic_info": "Hier sind die Kliniken, die Ihren Kriterien entsprechen:\n\n",
        "no_more_clinics": "Keine weiteren Kliniken verfügbar.",
        "try_again": "Erneut versuchen",
        "stop": "Stopp",
        "goodbye": "Danke, dass Sie unseren Bot nutzen! Auf Wiedersehen!",
        "confirm_choices": "Sie haben Bezirk: {district} und Spezialisierung: {speciality} gewählt\nIst diese Information korrekt?",
        "confirm": "Bestätigen",
        "show_more": "Mehr anzeigen",
        "website_text": "Unternehmenswebseite",
        "maps_text": "Unternehmensstandort auf Google Maps",
        "chose_district": "Sie haben den Bezirk gewählt: {district}",
        "chose_speciality": "Sie haben die Spezialisierung gewählt: {speciality}",
        "enter_speciality": "Bitte geben Sie die gesuchte Spezialisierung ein:",
        "invalid_district": "Ungültiger Bezirk ausgewählt. Bitte versuchen Sie es erneut.",
        "invalid_speciality": "Ungültige Spezialisierung ausgewählt. Bitte versuchen Sie es erneut.",
        "districts": ["Bang Tao", "Chalong", "Kamala", "Karon", "Kata", "Kathu", "Patong", "Phuket Town", "Rawai",
                      "Thalang"],
        "clinic_types": ["Medizinische Klinik", "Zahnklinik", "Krankenhaus", "Spezialisierte Klinik", "Wellness-Klinik",
                         "Physiotherapie-Klinik", "Labor"],
        "feedback_user": "😊 **Vielen Dank, dass Sie uns Ihr Feedback geben möchten.**\n\n"
                         "🔍 Es ist sehr wichtig für uns zu wissen, wie wir unseren Service verbessern können.\n\n"
                         "📧 Sie können eine E-Mail an [thesoowai.inc@gmail.com](mailto:thesoowai.inc@gmail.com) senden "
                         "oder eine Nachricht im Chat senden.\n\n"
                         "👇👇👇",
        "thank_you_feedback": "😊 Vielen Dank für Ihr Feedback! Wir schätzen Ihren Beitrag.",
        "start_over_prompt": "Möchten Sie neu anfangen?",
        "insurance_about": "Allgemeine Informationen über Versicherungen und deren Nutzung. \n\n 🦺 [Artikel](https://telegra.ph/Ich-habe-eine-Versicherung-wie-benutze-ich-sie-06-07)",
        "use_buttons": [
            "Bitte verwenden Sie die Schaltflächen, {user_name}.",
            "{user_name}, bitte verwenden Sie die bereitgestellten Schaltflächen.",
            "Um fortzufahren, {user_name}, verwenden Sie bitte die verfügbaren Schaltflächen.",
            "{user_name}, klicken Sie auf die Schaltflächen anstatt zu tippen."
        ]
    },
    "thai": {
        "welcome": "👋 ยินดีต้อนรับสู่บอทค้นหาคลินิกในภูเก็ต! 🌴\n\nบอทนี้จะช่วยคุณค้นหาคลินิกทางการแพทย์ที่ดีที่สุดในภูเก็ต \nในการเริ่มต้น ใช้คำสั่งใดคำสั่งหนึ่งต่อไปนี้:\n\n/start - เลือกภาษาและขั้นตอนแรก\n/findclinic - เริ่มค้นหาคลินิกตามเขต\n/medicine - ค้นหายาที่คล้ายคลึงกันโดยไม่ต้องออกจากโทรเลข\n/insurance - อยู่ระหว่างการพัฒนา\n/feedback - ข้อเสนอแนะและข้อเสนอแนะ\n\nเราหวังว่าคุณจะพอใจกับบริการของเรา โปรดใช้คำสั่ง feedback เพื่อส่งคำติชมหรือคำแนะนำถึงเรา เรายินดีที่จะปรับปรุงด้วยความช่วยเหลือจากคุณ สำหรับคำแนะนำและข้อร้องเรียน ติดต่อ @konstaninMrK 🏥✨",
        "medicine_sites": "🔍 นี่คือเว็บไซต์ที่คุณสามารถค้นหาข้อมูลเกี่ยวกับการแทนยาต่างๆ:\n\n",
        "choose_area": "โปรดเลือกพื้นที่ที่คุณต้องการหาคลินิก:",
        "choose_speciality": "โปรดเลือกความเชี่ยวชาญของคลินิก:",
        "clinic_info": "นี่คือคลินิกที่ตรงตามเกณฑ์ของคุณ:\n\n",
        "no_more_clinics": "ไม่มีคลินิกเพิ่มเติม",
        "try_again": "ลองอีกครั้ง",
        "stop": "หยุด",
        "goodbye": "ขอบคุณที่ใช้บอทของเรา! ลาก่อน!",
        "confirm_choices": "คุณเลือกเขต: {district} และความเชี่ยวชาญ: {speciality}\nข้อมูลนี้ถูกต้องหรือไม่?",
        "confirm": "ยืนยัน",
        "show_more": "แสดงเพิ่มเติม",
        "website_text": "เว็บไซต์บริษัท",
        "maps_text": "ตำแหน่งบริษัทบน Google Maps",
        "chose_district": "คุณเลือกเขต: {district}",
        "chose_speciality": "คุณเลือกความเชี่ยวชาญ: {speciality}",
        "enter_speciality": "โปรดป้อนความเชี่ยวชาญที่คุณกำลังมองหา:",
        "invalid_district": "เลือกเขตไม่ถูกต้อง โปรดลองอีกครั้ง",
        "invalid_speciality": "เลือกความเชี่ยวชาญไม่ถูกต้อง โปรดลองอีกครั้ง",
        "districts": ["บางเทา", "ฉลอง", "กมลา", "กะรน", "กะตะ", "กะทู้", "ป่าตอง", "ตัวเมืองภูเก็ต", "ราไวย์", "ถลาง"],
        "clinic_types": ["คลินิกแพทย์", "คลินิกทันตกรรม", "โรงพยาบาล", "คลินิกเฉพาะทาง", "คลินิกสุขภาพ",
                         "คลินิกกายภาพบำบัด", "ห้องปฏิบัติการ"],
        "feedback_user": "😊 **ขอบคุณที่ตั้งใจจะส่งคำติชมของคุณให้เรา**\n\n"
                         "🔍 สิ่งสำคัญมากสำหรับเราที่จะรู้ว่าเราสามารถปรับปรุงบริการของเราได้อย่างไร.\n\n"
                         "📧 คุณสามารถส่งอีเมลไปที่ [thesoowai.inc@gmail.com](mailto:thesoowai.inc@gmail.com) "
                         "หรือส่งข้อความในแชท\n\n"
                         "👇👇👇",
        "thank_you_feedback": "😊 ขอบคุณสำหรับความคิดเห็นของคุณ! เราขอขอบคุณสำหรับความคิดเห็นของคุณ.",
        "start_over_prompt": "คุณต้องการเริ่มต้นใหม่หรือไม่?",
        "insurance_about": "ข้อมูลทั่วไปเกี่ยวกับการประกันภัยและวิธีใช้งาน \n\n 🦺 [บทความ](https://telegra.ph/%E0%B8%89%E0%B8%B1%E0%B8%99%E0%B8%A1%E0%B8%B5%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%B1%E0%B8%99-%E0%B8%88%E0%B8%B0%E0%B9%83%E0%B8%8A%E0%B9%89%E0%B8%A1%E0%B8%B1%E0%B8%99%E0%B8%AD%E0%B8%A2%E0%B9%88%E0%B8%B2%E0%B8%87%E0%B9%84%E0%B8%A3-06-07)",
        "use_buttons": [
            "โปรดใช้ปุ่ม, {user_name}.",
            "{user_name}, โปรดใช้ปุ่มที่ให้ไว้.",
            "ในการดำเนินการต่อ, {user_name}, โปรดใช้ปุ่มที่มีให้.",
            "{user_name}, คลิกที่ปุ่มแทนการพิมพ์."
        ]
    }
}

import sqlite3

def init_db():
    conn = sqlite3.connect('meds_answers.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS drug_analogs
                      (name TEXT PRIMARY KEY, link TEXT, text TEXT)''')
    conn.commit()
    conn.close()

# Запуск функции для создания базы данных
init_db()
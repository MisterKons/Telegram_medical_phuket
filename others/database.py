import sqlite3


async def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS drug_analogs
                      (name TEXT PRIMARY KEY, link TEXT, text TEXT)''')
    conn.commit()
    conn.close()


async def save_drug_analog(name, analog):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO drug_analogs (name, link, text) VALUES (?, ?, ?)",
                   (name, analog['link'], analog['text']))
    conn.commit()
    conn.close()


async def get_saved_analog(name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT link, text FROM drug_analogs WHERE name=?", (name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"link": result[0], "text": result[1]}
    return None

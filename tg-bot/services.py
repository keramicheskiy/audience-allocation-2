from settings import cursor, conn


def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Token (tg_id INTEGER PRIMARY KEY, token TEXT)''')
    conn.commit()


def get_token(tg_id):
    cursor.execute('SELECT token FROM users WHERE tg_id = ?', (tg_id,))
    result = cursor.fetchone()
    return result[0] if result else None


def save_token(tg_id, token):
    cursor.execute('INSERT OR REPLACE INTO Token (tg_id, token) VALUES (?, ?)', (tg_id, token))
    conn.commit()


def delete_token(tg_id):
    cursor.execute('DELETE FROM Token WHERE tg_id = ?', (tg_id,))
    conn.commit()

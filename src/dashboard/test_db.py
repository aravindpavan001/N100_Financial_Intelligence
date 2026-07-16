import utils.db as db

print("DB_PATH =", db.DB_PATH)

conn = db.get_connection()

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

print(cursor.fetchall())

conn.close()
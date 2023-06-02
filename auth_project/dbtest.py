import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
print("Opened database successfully")
cursor.execute(
    'CREATE TABLE IF NOT EXISTS users('
    'ID INTEGER PRIMARY KEY     AUTOINCREMENT, '
    'USERNAME TEXT  NOT NULL, '
    'PASSWORD           TEXT     NOT NULL, '
    'UNIQUE(USERNAME));'
)
cursor.execute('''CREATE TABLE IF NOT EXISTS notes(
         ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         user_id         TEXT  ,
         NOTE           TEXT,
         TIME           TEXT     DEFAULT(datetime('now','localtime')));''')

print("Table created successfully")
'''
for i in range(10, 20):
    cursor.execute(
        'INSERT INTO users (username,password) VALUES (:user,:pass)',
        {'user': f'user{i}', "pass": i}
    )

for uid in range(1, 8):
    for note in range(1,11):
        cursor.execute(
            'INSERT INTO notes (user_id,note) VALUES (:user_id,:note)',
            {'note': f'noteNum{note}', "user_id": uid}
        )
conn.commit()
'''
userData = cursor.execute('SELECT * FROM users')
for row in userData:
    print(row)

login = input("login: ")
password = input("password: ")


def sign_up(login, password):
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username,password)\
    VALUES (:login,:password)',
    {'login': login, "password": password})
    conn.commit()


def login_user(login, password):
    cursor = db.cursor()
    cursor.execute(
        ('SELECT id, username, password FROM users '
        'WHERE username = :login AND password = :password'),
        {"login": login, "password": password}
                )

    active_user = cursor.fetchone()
    return active_user


def insert_note():
    cursor = db.cursor()
    if active_user:
        note = input("Insert note: ")
        cursor.execute('INSERT INTO notes (note,user_id) \
        VALUES (:note,: user_id)', {"note": note, "user_id": active_user[0]})
        conn.commit()


def notes_join():
    cursor = db.cursor()
    data = cursor.execute(
        'SELECT users.username, users.id, notes.note, notes.time\
        FROM users LEFT JOIN notes on notes.user_id = users.id'
    )
    return data


conn.close()

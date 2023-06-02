from __init__ import db


class Users:
    def __init__(self):
        self.cursor = db.cursor()

    def get_all(self):
        self.cursor.execute('SELECT username FROM users')
        return self.cursor.fetchall()

    def check_username(self, username):
        self.cursor.execute(
            ('SELECT username FROM users '
                'WHERE username=:username'),
            {"username": username}
        )
        return self.cursor.fetchone()

    def sign_up(self, login, password):
        self.cursor.execute(
            ('INSERT INTO users (username,password)'
                'VALUES (:login,:password)'),
            {'login': login, "password": password}
        )
        db.commit()
        return self.cursor.lastrowid

    def login(self, login, password):
        self.cursor.execute(
            ('SELECT id, username, password FROM users '
                'WHERE username = :login AND password = :password'),
            {"login": login, "password": password}
        )

        active_user = self.cursor.fetchone()
        return active_user

    def get_user_by_id(self, user_id):
        self.cursor.execute(
            ('SELECT id, username, password FROM users '
                'WHERE id=:user_id'),
            {"user_id": user_id}
                    )
        return self.cursor.fetchone()


class Notes:
    def __init__(self):
        self.cursor = db.cursor()

    def insert(self, note: str, user_id: int):
        self.cursor.execute(
            ('INSERT INTO notes (note,user_id) '
                'VALUES (:note,:user_id)'),
            {"note": note, "user_id": user_id}
        )
        db.commit()
        return self.cursor.lastrowid

    def get_all(self, limit: int, offset: int):
        return self.cursor.execute(
            'SELECT users.username, users.id, '
            'notes.note, notes.time, notes.id '
            'AS note_id '
            'FROM users LEFT JOIN notes ON notes.user_id = users.id '
            'WHERE notes.note IS NOT NULL '
            'ORDER BY time DESC LIMIT :offset, :limit',
            {"limit": limit, "offset": offset}
        )

    def get_by_user_id(self, user_id: int):
        return self.cursor.execute(
            'SELECT users.username, users.id, '
            'notes.note, notes.time, notes.id '
            'AS note_id '
            'FROM users LEFT JOIN notes ON notes.user_id = users.id '
            'WHERE users.id=:user_id '
            'ORDER BY time DESC',
            {"user_id": user_id}
        )

    def edit_note(self, note_id: int, edited_note: str):
        self.cursor.execute(
            'UPDATE notes '
            'SET note = :edited_note '
            'WHERE notes.id = :note_id',
            {"note_id": note_id, "edited_note": edited_note}
            )
        db.commit()

    def get_by_id(self, note_id: int):
        return self.cursor.execute(
            'SELECT * FROM notes '
            'WHERE notes.id = :note_id',
            {"note_id": note_id}
            ).fetchone()

    def deletenote(self, note_id: int):
        self.cursor.execute(
            'DELETE FROM notes '
            'WHERE id = :note_id',
            {"note_id": note_id})
        db.commit()

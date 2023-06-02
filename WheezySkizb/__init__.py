import sqlite3
db = sqlite3.connect('test.db')
db.row_factory = sqlite3.Row

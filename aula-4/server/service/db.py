import sqlite3
from service.config import DB_NAME


CREATE_ACCOUNTS_TABLE = """
CREATE TABLE IF NOT EXISTS account(
  username TEXT PRIMARY KEY,
  created_at INTEGER
)
"""

CREATE_ACCOUNT = """
INSERT INTO account(username, created_at) VALUES(?, ?)
"""

LIST_ACCOUNTS = """
SELECT username, created_at FROM account
"""


class DB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(CREATE_ACCOUNTS_TABLE)

    def create_account(self, username, timestamp):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(CREATE_ACCOUNT, (username, timestamp))

    def list_accounts(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(LIST_ACCOUNTS)
            rows = cursor.fetchall()

        return [{"username": row[0], "created_at": row[1] } for row in rows]


database = DB(DB_NAME)

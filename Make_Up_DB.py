import sqlite3


class HeadScrabDB:

    def __init__(self) -> None:
        self.connection = sqlite3.connect('head_scrab.db')
        self.cursor = self.connection.cursor()

    def make_table(self) -> None:
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS scrabs (
            Name TEXT NOT NULL,
            Price TEXT,
            Description TEXT,
            Rating TEXT
        )""")

    def add_product(self, product) -> None:
        sql = "INSERT INTO scrabs VALUES(?,?,?,?)"
        self.cursor.execute(sql, product[0])

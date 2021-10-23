import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
       # self.cur.execute("CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY, part text, customer text, retailer text, price text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM MEDICAMENTOS")
        rows = self.cur.fetchall()
        return rows

    def insert(self, part, customer):
        self.cur.execute("INSERT INTO MEDICAMENTOS VALUES (NULL, ?, ?)",
                         (part, customer))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM MEDICAMENTOS WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, part, customer):
        self.cur.execute("UPDATE MEDICAMENTOS SET nome = ?, hora = ? WHERE id = ?",
                         (part, customer, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

import sqlite3


class DBHelper:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

def setup(self):
    tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
    itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
    ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
    self.conn.execute(tblstmt)
    self.conn.execute(itemidx)
    self.conn.execute(ownidx)
    self.conn.commit()

    def add_item(self, item_text):
        stmt = "INSERT INTO items (description) VALUES (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description FROM items"
        return [x[0] for x in self.conn.execute(stmt)]


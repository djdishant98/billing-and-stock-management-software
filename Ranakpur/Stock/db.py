from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from pathlib import Path
import os , sys

class Db_Manager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
            cls._instance.create_tables()
        return cls._instance

    def _init_db(self):
        _dir = Path(__file__).resolve().parent
        db_path = _dir/"Stock_database.db"
        self.db =QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(str(db_path))
        if self.db.open():
            print("Successfully opened Database connection")
        else:
            print("Failed to open")
            sys.exit(1)

    def create_tables(self):
        query = QSqlQuery()
        query_dict ={'sell_table' : """
                                CREATE TABLE IF NOT EXISTS sell(
                                bill_no INTEGER PRIMARY KEY,
                                name TEXT,
                                address TEXT,
                                contact TEXT,
                                amount NUMERIC(10,3),
                                date TEXT)""",
                'sell_detail_table' :"""
                                CREATE TABLE IF NOT EXISTS sell_detail(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                bill_no INTEGER,
                                product TEXT,
                                weight NUMERIC(10,2),
                                quantity INTEGER,
                                amount NUMERIC(10,3),
                                mode TEXT,
                                date TEXT,
                                FOREIGN KEY(bill_no) REFERENCES sell(bill_no))""",
                'stock_table' :"""CREATE TABLE IF NOT EXISTS stock(
                                p_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                product TEXT,
                                carat TEXT,
                                weight REAL,
                                quantity INT,
                                entry_date TEXT,
                                previous_date TEXT)"""}
        for key , value in query_dict.items():
            if not query.exec_(value):
                print(query.lastError().text())
            else:
                print(f"Succefully created {key}")
            query.clear()
        
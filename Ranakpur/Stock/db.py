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
            #cls._instance.select_table('sell')
            #cls._instance.select_table('sell_detail')
            #cls._instance.delete_table('sell')
            #cls._instance.delete_table('sell_detail')
        return cls._instance

    def _init_db(self):
        _dir = Path(__file__).resolve().parent
        db_path = _dir/"Stock_database.db"
        self.db =QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(str(db_path))
        if self.db.open():
            print(self.db.isOpen())
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
            query.clear()

#-------------------------insertion operation in sell table---------------------------------------

    def insert_into_sell(self,*values):
        items = list(values)
        data = """INSERT INTO sell(bill_no,name,address,contact,amount,date) VALUES (?,?,?,?,?,?)"""
        query = QSqlQuery()
        if len(items) == 6:
            query.prepare(data)
            query.addBindValue(int(items[0]))
            query.addBindValue(items[1])
            query.addBindValue(items[2])
            query.addBindValue(items[3])
            query.addBindValue(float(items[4]))
            query.addBindValue(items[5])
            if not query.exec_():
                print(query.lastError().text())
        else:
            print(f"sell len count {len}")

#--------------------------------------returns bill number of sell table--------------------------------------

    def select_billno_sell(self):                                            
        query = QSqlQuery()
        if query.exec_("""SELECT MAX(bill_no) FROM sell"""):
            if query.next():
                raw_query = query.value(0)
                if str(raw_query).strip() != '' and raw_query is not None:
                    b_n = str(int(raw_query)+1)
                else:
                    b_n = '1'
            else:
                b_n ='1'
        return b_n

#-------------------------------insertion into sell_detail table-------------------------------------------------

    def insert_into_sell_detail(self,b_n,item2,item3,item4,item5,item6,datee):
        items = [b_n,item2,item3,item4,item5,item6,datee]
        query = QSqlQuery()
        data = """INSERT INTO sell_detail(bill_no,product,weight,quantity,amount,mode,date) VALUES(?,?,?,?,?,?,?)"""
        try:
            val1 = int(items[0])
        except:
            val1 = 0

        val2 = str(items[1])

        try:
            val3 = float(items[2])
        except:
            val3 = 0.0

        try:
            val4 = int(items[3])
        except:
            val4 = 0 

        try:
            val5 = float(items[4])
        except:
            val5 = 0.0

        val6 = str(items[5])
        val7 = str(items[6])
        query.prepare(data)
        query.addBindValue(val1)
        query.addBindValue(val2)
        query.addBindValue(val3)
        query.addBindValue(val4)
        query.addBindValue(val5)
        query.addBindValue(val6)
        query.addBindValue(val7)
        if not query.exec_():
            print(query.lastError().text())
        
#---------------------------------------insertion into stock table--------------------------------------------

    def insert_into_stock(self):
        pass


    def select_table(self,table_name):
        data = f"SELECT * FROM {table_name}"
        query = QSqlQuery()
        query.exec_(data)
        record = query.record()
        cols = record.count()
        headers = [record.fieldName(i) for i in range(cols)]

        # Collect all rows first to calculate dynamic column widths
        rows = []
        while query.next():
            rows.append([str(query.value(i)) for i in range(cols)])

        if not rows:
            print(f"\nTable '{table_name}' is currently empty.\n")
            return

        # Calculate max width for each column dynamically
        widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(val))

        # Generate structural dividers
        divider = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
        
        # Print Header
        print(f"\n[TABLE: {table_name.upper()}]")
        print(divider)
        header_row = "|" + "|".join([f" {headers[i]:<{widths[i]}} " for i in range(cols)]) + "|"
        print(header_row)
        print(divider)

        # Print Data Rows
        for row in rows:
            data_row = "|" + "|".join([f" {row[i]:<{widths[i]}} " for i in range(cols)]) + "|"
            print(data_row)
            
        print(divider + "\n")

    def delete_table(self,table_name):
        data = f'DELETE FROM {table_name}'
        data1 = f"DELETE FROM sqlite_sequence WHERE name ='{table_name}'" 
        query = QSqlQuery()
        if not query.exec_(data):
            print(f"Unable to perform delete on {table_name}")
        query.clear()
        if not query.exec_(data1):
            print(f"Unsuccessful deletetion for {table_name}")


#d = Db_Manager()
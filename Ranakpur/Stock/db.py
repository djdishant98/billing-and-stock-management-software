from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from pathlib import Path
import os , sys
from datetime import date , datetime

class Db_Manager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
            cls._instance.create_tables()
            #cls._instance.select_table('sell')
            #cls._instance.select_table('sell_detail')
            #cls._instance.select_table('buy')
            #cls._instance.select_table('buy_detail')
            #cls._instance.select_table('gst_gold')
            #cls._instance.select_table('gst_silver')
            #cls._instance.select_table('buy_silver')
            #cls._instance.select_table('buy_silver_detail')
            #cls._instance.delete_table('sell')
            #cls._instance.delete_table('sell_detail')
            #cls._instance.delete_table('buy')
            #cls._instance.delete_table('buy_detail')
            #cls._instance.delete_table('buy_silver')
            #cls._instance.delete_table('buy_silver_detail')
            #cls._instance.delete_table('gst_gold')
            #cls._instance.delete_table('gst_silver')
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
        #print(self.db.tables())

    def create_tables(self):
        query = QSqlQuery()
        """ query.exec_("DROP TABLE IF EXISTS buy")
        query.exec_("DROP TABLE IF EXISTS buy_detail")
        query.exec_("DROP TABLE IF EXISTS buy_silver")
        query.exec_("DROP TABLE IF EXISTS buy_silver_detail") """
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
                                previous_date TEXT)""",
        'stock_table_silver' :"""CREATE TABLE IF NOT EXISTS stock_silver(
                                p_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                product TEXT,
                                purity TEXT,
                                weight REAL,
                                quantity INT,
                                entry_date TEXT,
                                previous_date TEXT)""",
                        "buy" :"""CREATE TABLE IF NOT EXISTS buy(
                                bill_no INTEGER PRIMARY KEY,
                                name TEXT,
                                address TEXT,
                                contact INTEGER,
                                pan TEXT,
                                amount NUMERIC(10,3),
                                discount NUMERIC(4,3),
                                mode TEXT,
                                date TEXT)""",
                  'buy_detail' :"""CREATE TABLE IF NOT EXISTS buy_detail(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                bill_no INTEGER,
                                product TEXT,
                                carat TEXT,
                                weight NUMERIC(5,3),
                                less NUMERIC(4,3),
                                net NUMERIC(5,3),
                                quantity INTEGER,
                                making TEXT,
                                rate NUMERIC(10,3),
                                amount NUMERIC(10,3),
                                date TEXT,
                                FOREIGN KEY(bill_no) REFERENCES buy(bill_no))""",
                  'buy_silver':"""CREATE TABLE IF NOT EXISTS buy_silver(
                                bill_no INTEGER PRIMARY KEY,
                                name TEXT,
                                address TEXT,
                                contact INTEGER,
                                pan TEXT,
                                amount NUMERIC(10,3),
                                discount NUMERIC(4,3),
                                mode TEXT,
                                date TEXT)""",
            'buy_silver_detail':"""CREATE TABLE IF NOT EXISTS buy_silver_detail(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                bill_no INTEGER,
                                product TEXT,
                                purity TEXT,
                                weight NUMERIC(5,3),
                                less NUMERIC(4,3),
                                net NUMERIC(5,3),
                                quantity INTEGER,
                                making TEXT,
                                rate NUMERIC(10,3),
                                amount NUMERIC(10,3),
                                date TEXT,
                                FOREIGN KEY(bill_no) REFERENCES buy_silver(bill_no))""",
                    'gst_gold':"""CREATE TABLE IF NOT EXISTS gst_gold(
                                bill_no INTEGER,
                                sgst NUMERIC(10,3),
                                cgst NUMERIC(10,3),
                                gst NUMERIC(10,3),
                                date TEXT)""",
                'sell_silver': """CREATE TABLE IF NOT EXISTS sell_silver(
                                bill_no INTEGER PRIMARY KEY,
                                name TEXT,
                                address TEXT,
                                contact TEXT,
                                amount NUMERIC(10,3),
                                date TEXT)""",
        'sell_silver_details':  """CREATE TABLE IF NOT EXISTS sell_silver_detail(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                bill_no INTEGER,
                                product TEXT,
                                weight NUMERIC(10,2),
                                quantity INTEGER,
                                amount NUMERIC(10,3),
                                mode TEXT,
                                date TEXT,
                                FOREIGN KEY(bill_no) REFERENCES sell_silver(bill_no))""",
                    'gst_silver':"""CREATE TABLE IF NOT EXISTS gst_silver(
                                bill_no INTEGER,
                                sgst NUMERIC(10,3),
                                cgst NUMERIC(10,3),
                                gst NUMERIC(10,3),
                                date TEXT)"""
                                }
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
        query.prepare(data)
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

#--------------------------------------insertion into buy table-------------------------------------------------

    def insert_into_buy(self,bill_no,name,address,contact,pan,amount,discount,mode,datee):
        query = QSqlQuery()
        data = """INSERT INTO buy(bill_no,name,address,contact,pan,amount,discount,mode,date)
                    VALUES
                (?,?,?,?,?,?,?,?,?)"""
        query.prepare(data)
        try:
            bill_no = int(bill_no)
        except:
            bill_no = 0
        try:
            name =str(name)
        except:
            name = 'Null'
        try:
            address = str(address)
        except:
            address = 'Null'
        try:
            contact = int(contact)
        except:
            contact = 0
        try:
            pan =str(pan)
        except:
            pan = 'Null'
        try:
            amount = float(amount)
        except:
            amount = 0.0
        try:
            discount = float(discount)
        except:
            discount = 0.0
        try:
            mode = str(mode)
        except:
            mode = 'Cash'
        try:
            datee = str(datee)
        except:
            today = date.today()
            datee=today.strftime("%d-%m-%Y")
        query.addBindValue(bill_no)
        query.addBindValue(name)
        query.addBindValue(address)
        query.addBindValue(contact)
        query.addBindValue(pan)
        query.addBindValue(amount)
        query.addBindValue(discount)
        query.addBindValue(mode)
        query.addBindValue(datee)
        if query.exec_():
            print("buy table updated")
        else:
            print(query.lastError().text())

#-------------------------------------insertion into buy_detail table--------------------------------------

    def insert_into_buy_detail(self,bill_no,product,carat,weight,less,net,quantity,making,rate,amount,datee):
        query = QSqlQuery()
        data = """INSERT INTO buy_detail(bill_no,product,carat,weight,less,net,quantity,making,rate,amount,date)
                    VALUES
                  (?,?,?,?,?,?,?,?,?,?,?)"""
        query.prepare(data)
        try:
            bill_no = int(bill_no)
        except:
            bill_no = 0
        try:
            product = str(product)
        except:
            product ='Null'
        try:
            carat = str(carat)
        except:
            carat = "Null"
        try:
            weight = float(weight)
        except:
            weight = 0.0
        try:
            less = float(less)
        except:
            less =0.0
        try:
            net = float(net)
        except:
            net =0.0
        try:
            quantity = int(quantity)
        except:
            quantity = 0
        try:
            making = str(making)
        except:
            making ="Null"
        try:
            rate = float(rate)
        except:
            rate = 0.0
        try:
            amount = float(amount)
        except:
            amount =0.0
        try:
            datee = str(datee)
        except:
            today = date.today()
            datee=today.strftime("%d-%m-%Y")
        query.addBindValue(bill_no)
        query.addBindValue(product)
        query.addBindValue(carat)
        query.addBindValue(weight)
        query.addBindValue(less)
        query.addBindValue(net)
        query.addBindValue(quantity)
        query.addBindValue(making)
        query.addBindValue(rate)
        query.addBindValue(amount)
        query.addBindValue(datee)
        if query.exec_():
            print("buy_detail table updated")
        else:
            print(query.lastError().text())

#-----------------------------------insertion into buy_silver_detail table---------------------------------

    def insert_into_buy_silver_detail(self,bill_no,product,purity,weight,less,net,qunatity,making,rate,amount,datee):
        query = QSqlQuery()
        data = """INSERT INTO buy_silver_detail(bill_no,product,purity,weight,less,net,quantity,making,rate,amount,date)
                    VALUES
                    (?,?,?,?,?,?,?,?,?,?,?)"""
        query.prepare(data)
        try:
            bill_no = int(bill_no)
        except:
            bill_no = 0
        try:
            product = str(product)
        except:
            product ='Null'
        try:
            purity = str(purity)
        except:
            purity = "Null"
        try:
            weight = float(weight)
        except:
            weight = 0.0
        try:
            less = float(less)
        except:
            less =0.0
        try:
            net = float(net)
        except:
            net =0.0
        try:
            quantity = int(quantity)
        except:
            quantity = 0
        try:
            making = str(making)
        except:
            making ="Null"
        try:
            rate = float(rate)
        except:
            rate = 0.0
        try:
            amount = float(amount)
        except:
            amount =0.0
        try:
            datee = str(datee)
        except:
            today = date.today()
            datee=today.strftime("%d-%m-%Y")
        query.addBindValue(bill_no)
        query.addBindValue(product)
        query.addBindValue(purity)
        query.addBindValue(weight)
        query.addBindValue(less)
        query.addBindValue(net)
        query.addBindValue(quantity)
        query.addBindValue(making)
        query.addBindValue(rate)
        query.addBindValue(amount)
        query.addBindValue(datee)
        if query.exec_():
            print("buy_silver_detail table updated")
        else:
            print("Failed to update buy_silver_detail table")

#-----------------------------------insertion into buy_silver table---------------------------------------

    def insert_into_buy_silver(self,bill_no,name,address,contact,pan,amount,discount,mode,datee):
        query = QSqlQuery()
        data = """INSERT INTO buy_silver(bill_no,name,address,contact,pan,amount,discount,mode,date)
                    VALUES
                (?,?,?,?,?,?,?,?,?)"""
        query.prepare(data)
        try:
            bill_no = int(bill_no)
        except:
            bill_no = 0
        try:
            name =str(name)
        except:
            name = 'Null'
        try:
            address = str(address)
        except:
            address = 'Null'
        try:
            contact = int(contact)
        except:
            contact = 0
        try:
            pan =str(pan)
        except:
            pan = 'Null'
        try:
            amount = float(amount)
        except:
            amount = 0.0
        try:
            discount = float(discount)
        except:
            discount = 0.0
        try:
            mode = str(mode)
        except:
            mode = 'Cash'
        try:
            datee = str(datee)
        except:
            today = date.today()
            datee=today.strftime("%d-%m-%Y")
        query.addBindValue(bill_no)
        query.addBindValue(name)
        query.addBindValue(address)
        query.addBindValue(contact)
        query.addBindValue(pan)
        query.addBindValue(amount)
        query.addBindValue(discount)
        query.addBindValue(mode)
        query.addBindValue(datee)
        if query.exec_():
            print("buy_silver table updated")
        else:
            print(query.lastError().text())

#-------------------------------------insertion into gst_gold table---------------------------------------

    def insert_into_gst_gold(self,bill_no,sgst,cgst,gst,datee):
        query =QSqlQuery()
        data = """INSERT INTO gst_gold(bill_no,sgst,cgst,gst,date)
                VALUES
                (?,?,?,?,?)"""
        query.prepare(data)
        try:
            bill_no =int(bill_no)
        except(ValueError,TypeError):
            bill_no =0
        try:
            sgst = float(sgst)
        except(ValueError,TypeError):
            sgst = 0.0
        try:
            cgst = float(cgst)
        except(ValueError,TypeError):
            cgst =0.0
        try:
            gst = float(gst)
        except(ValueError,TypeError):
            gst = 0.0
        try :
            datee = str(datee)
        except:
            today = date.today()
            datee = today.strftime("%d-%m-%Y")
        query.addBindValue(bill_no)
        query.addBindValue(sgst)
        query.addBindValue(cgst)
        query.addBindValue(gst)
        query.addBindValue(datee)
        if query.exec_():
            print("GST of gold Updated")
        else:
            print(query.lastError().text())


#--------------------------------------insertion into gst_silver table-------------------------------------

    def insert_into_gst_silver(self,bill_no,sgst,cgst,gst,datee):
        query =QSqlQuery()
        data = """INSERT INTO gst_silver(bill_no,sgst,cgst,gst,date)
                VALUES
                (?,?,?,?,?)"""
        query.prepare(data)
        try:
            bill_no =int(bill_no)
        except(ValueError,TypeError):
            bill_no =0
        try:
            sgst = float(sgst)
        except(ValueError,TypeError):
            sgst = 0.0
        try:
            cgst = float(cgst)
        except(ValueError,TypeError):
            cgst =0.0
        try:
            gst = float(gst)
        except(ValueError,TypeError):
            gst = 0.0
        try :
            datee = str(datee)
        except:
            today = date.today()
            datee = today.strftime("%d-%m-%Y")
        query.addBindValue(bill_no)
        query.addBindValue(sgst)
        query.addBindValue(cgst)
        query.addBindValue(gst)
        query.addBindValue(datee)
        if query.exec_():
            print("GST of silver Updated")
        else:
            print("Failed to update silver gst")
    
#--------------------------------DISPLAYING TABLES----------------------------------------------

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
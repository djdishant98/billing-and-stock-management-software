from PyQt5.QtCore import Qt , QAbstractTableModel
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QLabel,
                             QLineEdit,
                             QCheckBox,
                             QPushButton,
                             QVBoxLayout,
                             QHBoxLayout,
                             QComboBox,
                             QFrame,
                             QMainWindow,
                             QTableWidget,
                             QTableView,
                             QMessageBox,
                             QRadioButton,
                             QHeaderView,
                             QStackedWidget,
                             QAction
                             )
from PyQt5.QtGui import (QFont,
                         QStandardItemModel, 
                         QStandardItem,
                         QBrush,
                         QColor)
from PyQt5.QtSql import QSqlTableModel , QSqlQuery , QSqlDatabase
#from Stock.stock import Bill
import json
import re , sqlite3 , os , sys
from datetime import date , datetime
from pathlib import Path

"""class TableModal(QAbstractTableModel):
    def __init__(self,data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self,index):
        return len(self._data)

    def columnCount(self,index):
        return len(self._data[0])"""

class Pilot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_background_db()
        cur_dict = Path(__file__).resolve().parent
        config_path = cur_dict/"Data"/"config.json"
        if not config_path.exists():
            data ={}
        else:
            try:
                with open(str(config_path),'r') as file:
                    data = json.load(file)
                    self.gold_list = data.get("Gold_List")
                    self.silver_list = data.get("Silver_List")
                    carat = data.get("Carat")
                    mode = data.get("Mode")
                    self.gold_making = data.get("Gold_Making")
                    self.silver_making = data.get("Silver_Making")
                    self.g_rate = data.get("Gold_Rate")
                    self.s_rate = data.get("Silver_Rate")
                    self.firm = data.get("Shop_Name")
                    self.address = data.get("Address")
                    self.contact = data.get("Contact")
                    self.gst = data.get("GST")

            except json.JSONDecodeError:
                print("Json file is corrupted")
                return False
        self.orna =''


        #--------------------Creating main Layout---------------------------------
        #--------------------Creating widgets for layout desigining----------------

        self.container_widget = QWidget()  
        self.stack_ = QStackedWidget()
        self.create_menu_bar()  
        header_widget = QFrame()
        header_widget.setFrameStyle(QFrame.Plain | QFrame.Panel)
        header_widget.setLineWidth(2)
        details_widget = QFrame()
        details_widget.setFrameStyle(QFrame.Plain | QFrame.Panel)
        details_widget.setLineWidth(1)
        product_widget = QFrame()
        product_widget.setFrameStyle(QFrame.Panel | QFrame.Plain)
        product_widget.setLineWidth(1)
        billing_widget = QFrame()
        billing_widget.setFrameStyle(QFrame.Panel | QFrame.Plain)
        billing_table_widget = QFrame()
        billing_widget.setFrameStyle(QFrame.Panel | QFrame.Plain)

        self.head = QLabel("Ranakpur Jewellers")
        self.gold = QRadioButton('GOLD')
        self.silver = QRadioButton('SILVER')
        self.head.setStyleSheet('font:30pt')
        self.cus_name_label = QLabel('Name')
        self.cus_name = QLineEdit()
        self.cus_address_label = QLabel('Address')
        self.cus_address = QLineEdit()
        self.cus_contact_label = QLabel('Contact')
        self.cus_contact = QLineEdit()
        self.date_label = QLabel('Date')
        today = date.today()
        d=today.strftime("%d-%m-%Y")
        self.date_ = QLabel(d)
        self.product_list_label = QLabel('Product')
        self.product_list = QComboBox()
        self.product_list.setEditable(True)                 #Editing checkbox
        self.product_quantity_label = QLabel('Quantity')
        self.product_quantity = QLineEdit()
        self.product_weight_label = QLabel('Weight')
        self.product_weight = QLineEdit()
        self.product_carat_label = QLabel('Carat')
        self.product_carat = QComboBox()
        self.product_carat.addItems(carat)
        self.product_carat.setEditable(True)
        self.amount_label = QLabel('Amount')
        self.amount = QLineEdit()
        self.payment_mode_label = QLabel('Payment Mode')
        self.payment_mode = QComboBox()
        self.payment_mode.addItems(mode)
        self.payment_mode.setEditable(True)
        self.rate_label = QLabel('Rate')
        self.rate = QLabel(self.g_rate)
        self.m_c_label = QLabel('Making Charge')
        self.m_c = QComboBox()
        self.m_c.setEditable(True)
        self.print_button = QPushButton("PRINT")
        #self.print_button.setContentsMargins(20,20,20,20)
        self.reset_button = QPushButton("RESET")
        #self.reset_button.setContentsMargins(20,20,20,20)
        self.add_button = QPushButton("ADD")
        #self.add_button.setContentsMargins(20,20,20,20)
        self.create_GST_button = QPushButton("Create GST")
        
        #----------------------Events---------------------------------

        self.print_button.clicked.connect(self.create_bill_function)
        #self.print_button.released.connect(self.clear_field_function)
        self.reset_button.clicked.connect(self.reset_function)
        self.add_button.pressed.connect(self.print_function)
        self.create_GST_button.clicked.connect(self.create_GST_function)
        self.add_button.released.connect(self.clear_field_function)
        self.gold.toggled.connect(self.gold_silver_toggle_function)
        self.silver.toggled.connect(self.gold_silver_toggle_function)

        #------------------------Header Layout-------------------------

        header = QHBoxLayout()
        header.addWidget(self.head,alignment=Qt.AlignmentFlag.AlignCenter)
        header.addWidget(self.gold,alignment=Qt.AlignmentFlag.AlignRight)
        header.addWidget(self.silver,alignment=Qt.AlignmentFlag.AlignRight)
        header_widget.setLayout(header)
        header_widget.setContentsMargins(20,20,20,20)

        #----------------Customer details layout--------------------

        name_layout = QHBoxLayout()
        name_layout.addWidget(self.cus_name_label,stretch=30)
        name_layout.addWidget(self.cus_name,stretch=70)
        address_layout = QHBoxLayout()
        address_layout.addWidget(self.cus_address_label,stretch=30)
        address_layout.addWidget(self.cus_address,stretch=70)
        contact_layout = QHBoxLayout()
        contact_layout.addWidget(self.cus_contact_label,stretch=30)
        contact_layout.addWidget(self.cus_contact,stretch=70)
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_label,stretch=30)
        date_layout.addWidget(self.date_,stretch=70)
        details_layout = QVBoxLayout()
        details_layout.addLayout(name_layout)
        details_layout.addLayout(address_layout)
        details_layout.addLayout(contact_layout)
        details_layout.addLayout(date_layout)
        details_widget.setLayout(details_layout)
        details_widget.setContentsMargins(30,20,30,20)

        #-----------------Product information layout------------------

        product_list_layout = QHBoxLayout()
        product_list_layout.addWidget(self.product_list_label,stretch=30)
        product_list_layout.addWidget(self.product_list,stretch=70)
        product_quantity_layout = QHBoxLayout()
        product_quantity_layout.addWidget(self.product_quantity_label,stretch=30)
        product_quantity_layout.addWidget(self.product_quantity,stretch=70)
        product_weight_layout = QHBoxLayout()
        product_weight_layout.addWidget(self.product_weight_label,stretch=30)
        product_weight_layout.addWidget(self.product_weight,stretch=70)
        product_carat_layout = QHBoxLayout()
        product_carat_layout.addWidget(self.product_carat_label,stretch=30)
        product_carat_layout.addWidget(self.product_carat,stretch=70)
        product_layout = QVBoxLayout()
        product_layout.addLayout(product_list_layout)
        product_layout.addLayout(product_quantity_layout)
        product_layout.addLayout(product_weight_layout)
        product_layout.addLayout(product_carat_layout)
        product_widget.setLayout(product_layout)
        product_widget.setContentsMargins(30,20,30,20)

        #------------------Billing Layout--------------------------

        amount_layout = QHBoxLayout()
        amount_layout.addWidget(self.amount_label,stretch=30)
        amount_layout.addWidget(self.amount,stretch=70)
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(self.rate_label,stretch=30)
        rate_layout.addWidget(self.rate,stretch=70)
        making_layout = QHBoxLayout()
        making_layout.addWidget(self.m_c_label,stretch=30)
        making_layout.addWidget(self.m_c,stretch=70)
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.payment_mode_label,stretch=30)
        mode_layout.addWidget(self.payment_mode,stretch=70)
        billing_layout = QVBoxLayout()
        billing_layout.addLayout(rate_layout)
        billing_layout.addLayout(making_layout)
        billing_layout.addLayout(amount_layout)
        billing_layout.addLayout(mode_layout)
        billing_widget.setLayout(billing_layout)
        billing_widget.setContentsMargins(30,20,30,20)

        #------------------button layout-----------------------

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.create_GST_button)
        button_layout.setContentsMargins(20,20,20,20)
        button_layout.setAlignment(Qt.AlignRight)

        #-------------------Table View Layout----------------------

        self.view = QTableView()
        self.row=0
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Product','carat/purity','weight','Quantity','Making','Rate','Amount'])
        self.view.setModel(self.model)
        self.view.setShowGrid(False)
        #self.view.setContentsMargins(30,30,30,30)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.view.setBackgroundRole

        #------------------Final Window Page Layout--------------------

        part_1_layout = QVBoxLayout()
        part_2_layout = QVBoxLayout()
        final_layout = QHBoxLayout()
        part_1_layout.addWidget(header_widget)
        part_1_layout.addWidget(details_widget)
        part_1_layout.addWidget(product_widget)
        part_1_layout.addWidget(billing_widget)
        part_1_layout.addLayout(button_layout)
        part_2_layout.addWidget(self.view)
        final_layout.addLayout(part_1_layout)
        final_layout.addLayout(part_2_layout)
        self.container_widget.setLayout(final_layout)
        self.layout_design(self.container_widget)
        self.setWindowTitle('Billing v1.0')
        self.stack_.addWidget(self.container_widget)
        self.stack_.setCurrentWidget(self.container_widget)
        self.setCentralWidget(self.stack_)
        self.showMaximized()

    #----------------------------Creating menu bar---------------------------------------------

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&Category')
        exit_menu = menu_bar.addMenu('&Exit')

        purchase_action = QAction('&Purchase',self)
        purchase_action.setShortcut('Ctrl+D')
        purchase_action.triggered.connect(self.purchase_function)
        sell_action = QAction('&Sell',self)
        sell_action.setShortcut('Ctrl+F')
        sell_action.triggered.connect(self.sell_function)
        file_menu.addAction(purchase_action)
        file_menu.addAction(sell_action)

        exit_action = QAction('&Exit',self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.exit_function)
        exit_menu.addAction(exit_action)

    #------------------------------Event listeners of menubar-------------------------------

    def purchase_function(self):
        self.stack_.setCurrentWidget(self.container_widget)

    def sell_function(self):
        s = Sell(self)
        self.stack_.addWidget(s)
        self.stack_.setCurrentWidget(s)

    def exit_function(self):
        sys.exit(1)

    #----------------------------------creating database connection with existing table----------------

    def init_background_db(self):
        db_p= f'{Path.cwd()}/Stock/Stock_database.db'
        current_dir = Path(__file__).resolve().parent
        db_path = current_dir/"Stock"/"Stock_database.db"
        if QSqlDatabase.contains("qt_sql_default_connection"):
            # Re-use the existing active database connection pointer safely
            db = QSqlDatabase.database("qt_sql_default_connection")
        else:
            db = QSqlDatabase.addDatabase('QSQLITE','qt_sql_default_connection')
            db.setDatabaseName(str(db_path))
        if not db.open():
            QMessageBox.critical(self,db.lastError().text())
            return False
        else:
            self.db_model = QSqlTableModel(self,db)
            self.db_model.setTable('stock')
            self.db_model.select()

        #--------------------------------Creating Bill Print layout---------------------------
    def p_widget_function(self):
        self.p = QWidget()
        frame1 = QFrame()
        frame1.setFrameStyle(QFrame.Panel | QFrame.Plain)
        frame1.setLineWidth(4)
        frame2 = QFrame()
        frame2.setFrameStyle(QFrame.Panel | QFrame.Plain)
        frame2.setLineWidth(2)
        frame3 = QFrame()
        frame3.setFrameStyle(QFrame.Panel | QFrame.Plain)
        frame3.setLineWidth(2)
        self.label1 = QLabel("Ranakpur Jewellers")
        self.label2 = QLabel(self.address)
        self.label3 = QLabel(self.contact)
        self.label4 = QLabel(self.gst)
        self.label5 = QLabel('GOLD/SILVER PURCHASE')
        self.label6 = QLabel('Name:')
        self.label6_1 = QLabel(self.cus_name.text())
        self.label7 = QLabel('Address:')
        self.label7_1 = QLabel(self.cus_address.text())
        self.label8 = QLabel('Contact:')
        self.label8_1 = QLabel(self.cus_contact.text())
        self.label9 = QLabel(self.date_.text())
        time = datetime.now()
        self.label10 = QLabel(f'Customer\'s Sign')
        self.label11 = QLabel('For Ranakpur Jewellers')
        self.label12 = QLabel(str(time))
        layout1 = QVBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.label2)
        layout1.addWidget(self.label3)
        layout1.addWidget(self.label4)
        layout2 = QVBoxLayout()
        layout2_1 = QHBoxLayout()
        layout2_1.addWidget(self.label6)
        layout2_1.addWidget(self.label6_1)
        layout2_2 = QHBoxLayout()
        layout2_2.addWidget(self.label7)
        layout2_2.addWidget(self.label7_1)
        layout2_3 = QHBoxLayout()
        layout2_3.addWidget(self.label8)
        layout2_3.addWidget(self.label8_1)
        layout2_4 = QHBoxLayout()
        layout2_4.addWidget(self.label9)
        layout2.addLayout(layout2_1)
        layout2.addLayout(layout2_2)
        layout2.addLayout(layout2_3)
        layout2.addLayout(layout2_4)
        frame1.setLayout(layout1)
        frame2.setLayout(layout2)
        layout3 = QVBoxLayout()
        layout3.addWidget(self.label5,alignment=Qt.AlignmentFlag.AlignCenter)
        self.v = QTableView()
        self.v.setShowGrid(False)
        self.v.setContentsMargins(30,30,30,30)
        self.v.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.v.setModel(self.model)
        layout3.addWidget(self.v)
        layout4 = QHBoxLayout()
        layout4.addWidget(self.label10,alignment=Qt.AlignmentFlag.AlignLeft)
        layout4.addWidget(self.label11,alignment=Qt.AlignmentFlag.AlignRight)
        layout4.addWidget(self.label12,alignment=Qt.AlignmentFlag.AlignBottom)
        frame3.setLayout(layout4)
        b_final_layout = QVBoxLayout()
        b_final_layout.addWidget(frame1)
        b_final_layout.addWidget(frame2)
        b_final_layout.addLayout(layout3)
        b_final_layout.addWidget(frame3)
        self.p.setLayout(b_final_layout)
        self.stack_.addWidget(self.p)
        self.stack_.setCurrentWidget(self.p)

    #----------------------Establishing Database Connection----------------

        """self.conn = sqlite3.connect('bill_database.db',isolation_level=None)
        self.conn.execute('CREATE TABLE IF NOT EXISTS Customer_details(bill_no INT PRIMARY KEY NOT NULL,' \
                                                                    'name TEXT NOT NULL,' \
                                                                    'address TEXT NOT NULL,' \
                                                                    'contact TEXT,' \
                                                                    'total_items INT,' \
                                                                    'date TEXT(DD-MM-YYY))')
        self.conn.execute('CREATE TABLE IF NOT EXISTS Billing(id TEXT PRIMARY KEY NOT NULL,' \
                                                            'bill_no INT NOT NULL,' \
                                                            'category TEXT NOT NULL'
                                                            'product TEXT NOT NULL,' \
                                                            'weight REAL NOT NULL,' \
                                                            'quantity INT ,' \
                                                            'carat TEXT ,' \
                                                            'rate REAL,' \
                                                            'making TEXT NOT NULL,' \
                                                            'amount INT NOT NULL,' \
                                                            'FOREIGN KEY(bill_no) REFERENCES Customer_details(bill_no))')"""

    #----------------------function for desigining layouts----------------

    def layout_design(self,c):
       design = """QLabel{font:18pt;
                          color:#0c315b;
                          background:#c3d2d9}
                    QLineEdit{font:16pt;
                              color:#0c315b;
                              background:#e6dada}
                    QComboBox{font:16pt;
                              color:#0c315b;
                              background:#e6dada}
                    QPushButton{font:16pt;
                                background:#0a6ba0}""" 
       c.setStyleSheet(design)

#------------------------function to search in model for stock update during bill print function---------------------------

    def search_fields(self,product,carat):

        for r in range(self.db_model.rowCount()):
            data1 = self.db_model.index(r,1).data()
            data2 = self.db_model.index(r,2).data()
            if product == data1 and carat == data2:
                return r
        return False

    #----------------------function to create GST bill--------------------------------

    def create_GST_function(self):
        sgst = 0
        cgst = 0
        gst = 0
        gt = 0
        row = self.model.rowCount()
        if row is None:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Null Entries")
            msg.setText("Nothing to calculate")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            tt = self.model.data(self.model.index(10,6))
            sgst = (float(tt) * 1.5)/100 
            cgst = sgst
            gst = cgst + sgst
            gt = float(tt) + gst
            item8 = QStandardItem(str(sgst))
            item8.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item9 = QStandardItem(str(cgst))
            item9.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item10 = QStandardItem(str(gst))
            item10.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item11 = QStandardItem(str(gt))
            item11.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.model.setItem(11,5,QStandardItem('SGST'))
            self.model.setItem(12,5,QStandardItem('CGST'))
            self.model.setItem(13,5,QStandardItem('GST'))
            self.model.setItem(14,5,QStandardItem('Grand Total'))
            self.model.setItem(11,6,item8)
            self.model.setItem(12,6,item9)
            self.model.setItem(13,6,item10)
            self.model.setItem(14,6,item11)

    #----------------------function to print bill-------------------------------------

    def print_function(self):

        total=0
        item1 = self.product_list.currentText()
        item2 = self.product_carat.currentText()
        item3 = self.product_weight.text()
        item4 = self.product_quantity.text()
        item5 = self.m_c.currentText()

        if  not item1 or not item2 or not item3 or not item4:

            msg = QMessageBox(self)
            msg.setWindowTitle('Empty Field')
            msg.setText("Enter the Necessary details\nAll Fields Should be filled up")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        else:

            m_c = item5[:-1]
            item6 = self.rate.text()

            if self.orna == 'GOLD':

                making = (int(item6) * int(m_c))/100
                item7 = (float(item3) * int(item4) * int(item6)) + (float(item3) * int(item4) * making)
                self.amount.setText(str(item7))
                i_2 = QStandardItem(item2)
                i_2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                i_2.setBackground(QBrush(QColor('lightblue')))
                self.model.setItem(self.row,1,i_2)
                i_6 = QStandardItem(item6)
                i_6.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                i_6.setBackground(QBrush(QColor('lightblue')))
                self.model.setItem(self.row,5,i_6)
                r=self.search_fields(item1,item2)
                if r is not None and r>=0:
                     v1 = self.db_model.index(r,3).data()
                     v2 = self.db_model.index(r,4).data()
                     v1 = v1 - float(item3)
                     v2 = v2 - int(item4)
                     self.db_model.setData(self.db_model.index(r,3),v1)
                     self.db_model.setData(self.db_model.index(r,4),v2)
                     self.db_model.submitAll()
                     self.db_model.select()
                     while self.db_model.canFetchMore():
                         self.db_model.fetchMore()
                else:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Missing row in database")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("The product or carat is not available in Datatabase")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()

            else :

                if item5 == '30%':

                    m_c = item5[:-1]
                    rate = int(item6) - ((int(item6) * 30)/100)
                    making = (rate * int(m_c))/100
                    item7 = (float(item3) * int(item4) * rate) + (float(item3) * int(item4) * making)
                    i_6 = QStandardItem(str(rate))

                elif item5 == '200B':

                    m_c = item5[:-1]
                    item7 = (int(item3) * int(item4) * int(item6)) + (int(m_c)* int(item3)/10)
                    i_6 = QStandardItem(str(item6))

                elif item5 == '350P':

                    m_c = item5[:-1]
                    item7 = (int(item3) * int(item4) * int(item6)) + int(m_c)
                    i_6 = QStandardItem(str(m_c))

                else:

                    m_c = item5[:-1]
                    item7 = (float(item3) * int(m_c)) * int(item4)
                    i_6 = QStandardItem(str(m_c))

                i_2 = QStandardItem(item1[-3:])
                i_2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)     #item2 and item6 are changed according to gold and silver
                i_2.setBackground(QBrush(QColor("lightblue")))
                self.model.setItem(self.row,1,i_2)
                i_6.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                i_6.setBackground(QBrush(QColor('lightblue')))
                self.model.setItem(self.row,5,i_6)

            i_1 = QStandardItem(item1)                        
            i_1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            i_1.setBackground(QBrush(QColor("lightblue")))
            self.model.setItem(self.row,0,i_1)
            i_3 = QStandardItem(item3)
            i_3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            i_3.setBackground(QBrush(QColor("lightblue")))
            self.model.setItem(self.row,2,i_3)
            i_4 = QStandardItem(item4)
            i_4.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            i_4.setBackground(QBrush(QColor("lightblue")))
            self.model.setItem(self.row,3,i_4)
            i_5 = QStandardItem(item5)
            i_5.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            i_5.setBackground(QBrush(QColor("lightblue")))
            self.model.setItem(self.row,4,i_5) 
            i_7 = QStandardItem(str(item7))
            i_7.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            i_7.setBackground(QBrush(QColor("lightblue")))
            self.model.setItem(self.row,6,i_7)
            self.row+=1

            for i in range(self.row):

                item_ = self.model.item(i,6)

                if item_ is not None and item_.text():

                    total = total + float(item_.text())
                    t=QStandardItem(str(total))
                    t.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    t.setBackground(QBrush(QColor('#c3d2d9')))
                    self.model.setItem(10,6,t)

                tt = QStandardItem("Total")
                tt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tt.setBackground(QBrush(QColor('#c3d2d9')))
                self.model.setItem(10,5,tt)


    #-----------------------function to create bill--------------------------------

    def create_bill_function(self):

        a = self.cus_name.text()
        b = self.cus_contact.text()
        c = self.cus_address.text()

        if a and b and c :
            self.container_widget.hide()
            self.p_widget_function()
            
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle('Empty Field')
            msg.setText("Enter the Necessary details\nAll Fields Should be filled up")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


    #-----------------------function to clear fields after printing to table-----------------

    def clear_field_function(self):
        self.product_weight.clear()
        self.product_quantity.clear()
        self.product_list.setCurrentIndex(0)
        self.product_carat.setCurrentIndex(0)
        self.payment_mode.setCurrentIndex(0)
        self.m_c.setCurrentIndex(0)
        self.amount.clear()
            

    #-----------------------function to reset details-------------------

    def reset_function(self):
        self.cus_name.clear()
        self.cus_contact.clear()
        self.cus_address.clear()
        self.product_weight.clear()
        self.product_quantity.clear()
        self.product_list.setCurrentIndex(0)
        self.product_carat.setCurrentIndex(0)
        self.payment_mode.setCurrentIndex(0)
        self.m_c.setCurrentIndex(0)
        self.amount.clear()
        self.model.removeRows(0,self.model.rowCount())   #clearing model
        self.row = 0

    #-------------------------function for adding row in table view--------------------

    def add_button_function(self):
        pass

    #--------------------------Setting the Widgets according to radio button selection------------------------

    def gold_silver_toggle_function(self):
        comodity = self.sender()
        if comodity.isChecked():
            text = comodity.text()
            self.orna = text
            self.product_list.blockSignals(True)
            self.m_c.blockSignals(True)
            self.product_list.clear()                  #when button toggled the fields get appended with new list
            self.m_c.clear()                           #Signals are blocked to avoid any changes or interrupt in program                      
            self.rate.clear()
            if text == 'GOLD':
                self.product_list.addItems(self.gold_list)
                self.m_c.addItems(self.gold_making)
                self.rate.setText(self.g_rate)
                self.product_carat.setVisible(True)
                self.product_carat_label.setVisible(True)
            else:
                self.product_list.addItems(self.silver_list)
                self.m_c.addItems(self.silver_making)
                self.product_carat_label.setVisible(False)
                self.product_carat.hide()
                #self.product_carat.setVisible(False)
                self.rate.setText(self.s_rate)
        self.product_list.blockSignals(False)
        self.m_c.blockSignals(False)

#---------------------------------Class for sell section------------------------------------

class Sell(QWidget):
    def __init__(self, parent =None):
        super().__init__()
        header_widget = QFrame()
        header_widget.setFrameStyle(QFrame.Plain | QFrame.Panel)
        header_widget.setLineWidth(2)
        details_widget = QFrame()
        details_widget.setFrameStyle(QFrame.Plain | QFrame.Panel)
        details_widget.setLineWidth(1)
        product_widget = QFrame()
        product_widget.setFrameStyle(QFrame.Panel | QFrame.Plain)
        product_widget.setLineWidth(1)
        billing_widget = QFrame()
        billing_widget.setFrameStyle(QFrame.Panel | QFrame.Plain)

        self.head = QLabel("Ranakpur Jewellers")
        self.gold = QRadioButton('GOLD')
        self.silver = QRadioButton('SILVER')
        self.head.setStyleSheet('font:30pt')
        self.cus_name_label = QLabel('Name')
        self.cus_name = QLineEdit()
        self.cus_address_label = QLabel('Address')
        self.cus_address = QLineEdit()
        self.cus_contact_label = QLabel('Contact')
        self.cus_contact = QLineEdit()
        self.date_label = QLabel('Date')
        today = date.today()
        d=today.strftime("%d-%m-%Y")
        self.date_ = QLabel(d)
        self.product_list_label = QLabel('Product')
        self.product_list = QComboBox()
        self.product_list.setEditable(True)                 #Editing checkbox
        self.product_quantity_label = QLabel('Quantity')
        self.product_quantity = QLineEdit()
        self.product_weight_label = QLabel('Weight')
        self.product_weight = QLineEdit()
        self.amount_label = QLabel('Amount')
        self.amount = QLineEdit()
        self.payment_mode_label = QLabel('Payment Mode')
        self.payment_mode = QComboBox()
        mode=['Cash','UPI','Cheque','RTGS/NEFT']
        self.payment_mode.addItems(mode)
        self.payment_mode.setEditable(True)
        self.print_button = QPushButton("PRINT")
        #self.print_button.setContentsMargins(20,20,20,20)
        self.reset_button = QPushButton("RESET")
        #self.reset_button.setContentsMargins(20,20,20,20)
        self.add_button = QPushButton("ADD")
        #self.add_button.setContentsMargins(20,20,20,20)
        
        #----------------------Events---------------------------------

        self.print_button.clicked.connect(self.create_bill_function)
        #self.print_button.released.connect(self.clear_field_function)
        self.reset_button.clicked.connect(self.reset_function)
        self.add_button.pressed.connect(self.print_function)
        self.add_button.released.connect(self.clear_field_function)
        self.gold.toggled.connect(self.gold_silver_toggle_function)
        self.silver.toggled.connect(self.gold_silver_toggle_function)

        #------------------------Header Layout-------------------------

        header = QHBoxLayout()
        header.addWidget(self.head,alignment=Qt.AlignmentFlag.AlignCenter)
        header.addWidget(self.gold,alignment=Qt.AlignmentFlag.AlignRight)
        header.addWidget(self.silver,alignment=Qt.AlignmentFlag.AlignRight)
        header_widget.setLayout(header)
        header_widget.setContentsMargins(20,20,20,20)

        #----------------Customer details layout--------------------

        name_layout = QHBoxLayout()
        name_layout.addWidget(self.cus_name_label,stretch=30)
        name_layout.addWidget(self.cus_name,stretch=70)
        address_layout = QHBoxLayout()
        address_layout.addWidget(self.cus_address_label,stretch=30)
        address_layout.addWidget(self.cus_address,stretch=70)
        contact_layout = QHBoxLayout()
        contact_layout.addWidget(self.cus_contact_label,stretch=30)
        contact_layout.addWidget(self.cus_contact,stretch=70)
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_label,stretch=30)
        date_layout.addWidget(self.date_,stretch=70)
        details_layout = QVBoxLayout()
        details_layout.addLayout(name_layout)
        details_layout.addLayout(address_layout)
        details_layout.addLayout(contact_layout)
        details_layout.addLayout(date_layout)
        details_widget.setLayout(details_layout)
        details_widget.setContentsMargins(30,20,30,20)

        #-----------------Product information layout------------------

        product_list_layout = QHBoxLayout()
        product_list_layout.addWidget(self.product_list_label,stretch=30)
        product_list_layout.addWidget(self.product_list,stretch=70)
        product_quantity_layout = QHBoxLayout()
        product_quantity_layout.addWidget(self.product_quantity_label,stretch=30)
        product_quantity_layout.addWidget(self.product_quantity,stretch=70)
        product_weight_layout = QHBoxLayout()
        product_weight_layout.addWidget(self.product_weight_label,stretch=30)
        product_weight_layout.addWidget(self.product_weight,stretch=70)
        product_layout = QVBoxLayout()
        product_layout.addLayout(product_list_layout)
        product_layout.addLayout(product_quantity_layout)
        product_layout.addLayout(product_weight_layout)
        product_widget.setLayout(product_layout)
        product_widget.setContentsMargins(30,20,30,20)

        #------------------Billing Layout--------------------------

        amount_layout = QHBoxLayout()
        amount_layout.addWidget(self.amount_label,stretch=30)
        amount_layout.addWidget(self.amount,stretch=70)
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.payment_mode_label,stretch=30)
        mode_layout.addWidget(self.payment_mode,stretch=70)
        billing_layout = QVBoxLayout()
        billing_layout.addLayout(amount_layout)
        billing_layout.addLayout(mode_layout)
        billing_widget.setLayout(billing_layout)
        billing_widget.setContentsMargins(30,20,30,20)

        #------------------button layout-----------------------

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.print_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.add_button)
        button_layout.setContentsMargins(20,20,20,20)
        button_layout.setAlignment(Qt.AlignRight)

        #-------------------Table View Layout----------------------

        self.view = QTableView()
        self.row=0
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Product','weight','Quantity','Amount','Mode'])
        self.view.setModel(self.model)
        self.view.setShowGrid(False)
        #self.view.setContentsMargins(30,30,30,30)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.view.setBackgroundRole

        #------------------Final Window Page Layout--------------------

        part_1_layout = QVBoxLayout()
        part_2_layout = QVBoxLayout()
        final_layout = QHBoxLayout()
        part_1_layout.addWidget(header_widget)
        part_1_layout.addWidget(details_widget)
        part_1_layout.addWidget(product_widget)
        part_1_layout.addWidget(billing_widget)
        part_1_layout.addLayout(button_layout)
        part_2_layout.addWidget(self.view)
        final_layout.addLayout(part_1_layout)
        final_layout.addLayout(part_2_layout)
        self.setLayout(final_layout)
        self.layout_design()
        self.setWindowTitle('Billing v1.0')
        self.showMaximized()

    def layout_design(self):
           design = """QLabel{font:18pt;
                              color:#0c315b;
                              background:#c3d2d9}
                        QLineEdit{font:16pt;
                                  color:#0c315b;
                                  background:#e6dada}
                        QComboBox{font:16pt;
                                  color:#0c315b;
                                  background:#e6dada}
                        QPushButton{font:16pt;
                                    background:#0a6ba0}""" 
           self.setStyleSheet(design)

    #--------------------------Event listeners functions of sell class------------------------

    def create_bill_function(self):
        pass

    def reset_function(self):
        pass

    def print_function(self):
        pass

    def clear_field_function(self):
        pass

    def gold_silver_toggle_function(self):
        pass


if __name__ == '__main__':
    app = QApplication([])
    p = Pilot()
    p.show()
    app.exec_()
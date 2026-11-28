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
                             QAction,
                             QMenu,
                             QHeaderView,
                             QStackedWidget,
                             QStyledItemDelegate,
                             QDateEdit
                             )

from PyQt5.QtCore import Qt ,QDate , pyqtSignal , QItemSelectionModel
from PyQt5.QtGui import (QFont,
                         QStandardItemModel, 
                         QStandardItem,
                         QBrush,
                         QColor,
                         )

from PyQt5.QtSql import QSqlTableModel , QSqlDatabase , QSqlQuery
from datetime import date,datetime
import json ,sys ,os
from pathlib import Path
from Stock.stock import Bill , Detail
from Stock.db import Db_Manager

class Admin(QMainWindow):

    home = pyqtSignal()
    def __init__(self):
        super().__init__()
        if self.init_db() is False:
            sys.exit(1)
        self.create_menu_bar()
        self.set_layout()
        self.setStyleSheet("""QHeaderView::section {
                            background-color: #2C3E50;
                            color: #FFFFFF;
                            font-weight: bold;
                            padding: 6px;
                            border: 1px solid #1A252F;
                        }""")
        self.showMaximized()

    def create_menu_bar(self):
        """Generates a native menu bar at the top of the QMainWindow."""
        # 1. Create the main menu bar manager object hook
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color:#c2c9cc
            }
            QMenuBar::item {
                padding-left: 15px;
                padding-right: 15px;
                padding-top: 5px;
                padding-bottom: 5px;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0; 
            }
        """)
        # 2. Add top-level menu categories
        home_menu = menu_bar.addMenu('&Home')
        file_menu = menu_bar.addMenu('&File')
        detail_menu =menu_bar.addMenu('&Details')
        search_menu = menu_bar.addMenu('&Search')
        update_menu = menu_bar.addMenu('&Update')
        add_menu = menu_bar.addMenu('&Add')
        remove_menu = menu_bar.addMenu('&Remove')
        vyapari_menu = menu_bar.addMenu('&Vyapari')
        karagir_menu = menu_bar.addMenu('&Karagir')
        exit_menu = menu_bar.addMenu('&Exit')

        # 3. Create clickable Actions for the 'File' menu
        # Using & before a letter creates a quick keyboard Alt shortcut (e.g., Alt+F)

        h_action = QAction('&Home',self)
        h_action.triggered.connect(self.home_function)
        home_menu.addAction(h_action)

        c_r_menu = QMenu('&Customer Record',self)
        c_r_action = QAction('&Gold Purchase',self)
        c_r_action.setShortcut('Ctrl+R')                           
        c_r_action.triggered.connect(self.customer_record_function)  

        c_r_s_action  = QAction('& Gold Sell',self)
        c_r_s_action.setShortcut('Ctrl+Y')
        c_r_s_action.triggered.connect(self.customer_record_function)

        c_r_si_action = QAction('&Silver Purchase',self)
        c_r_si_action.triggered.connect(self.customer_record_function)

        c_r_si_s_action = QAction('&Silver Sell',self)
        c_r_si_s_action.triggered.connect(self.customer_record_function)

        gst_g_action = QAction('&Gold GST',self)
        gst_g_action.triggered.connect(self.customer_record_function)

        gst_s_action = QAction('&Silver GST',self)
        gst_s_action.triggered.connect(self.customer_record_function)

        c_r_menu.addAction(c_r_action)
        c_r_menu.addSeparator()
        c_r_menu.addAction(c_r_s_action)
        c_r_menu.addSeparator()    
        c_r_menu.addAction(c_r_si_action)
        c_r_menu.addSeparator()
        c_r_menu.addAction(c_r_si_s_action)
        c_r_menu.addSeparator()
        c_r_menu.addAction(gst_g_action)
        c_r_menu.addSeparator()
        c_r_menu.addAction(gst_s_action)

        g_b_d_action = QAction('&Gold purchase detail',self)
        g_b_d_action.triggered.connect(self.customer_record_function)

        g_s_d_action = QAction('&Gold sell detail',self)
        g_s_d_action.triggered.connect(self.customer_record_function)

        s_b_d_action = QAction('&Silver purchase detail',self)
        s_b_d_action.triggered.connect(self.customer_record_function)

        s_s_d_action = QAction('&Silver sell detail',self)
        s_s_d_action.triggered.connect(self.customer_record_function)

        detail_menu.addAction(g_b_d_action)
        detail_menu.addSeparator()
        detail_menu.addAction(g_s_d_action)
        detail_menu.addSeparator()
        detail_menu.addAction(s_b_d_action)
        detail_menu.addSeparator()
        detail_menu.addAction(s_s_d_action)

        s_r_action = QAction('&Stock Record', self)
        s_r_action.setShortcut('Ctrl+E')
        s_r_action.triggered.connect(self.stock_record_function)                    

        # Append choices to the File dropdown column list
        file_menu.addMenu(c_r_menu)
        file_menu.addSeparator() # Visual dividing line decoration spacer
        file_menu.addAction(s_r_action)


        # 4. Create actions for the 'Search' menu

        gst_action = QAction('&GST', self)
        gst_action.triggered.connect(self.search_function)

        bill_action = QAction('&Customer',self)
        bill_action.triggered.connect(self.search_function)

        search_menu.addAction(gst_action)
        search_menu.addSeparator()
        search_menu.addAction(bill_action)

        gold_rate = QAction('&Gold Rate',self)
        gold_rate.setShortcut('Ctrl+G')
        gold_rate.triggered.connect(self.gold_rate_function)
        silver_rate = QAction('&Silver Rate',self)
        silver_rate.setShortcut('Ctrl+F')
        silver_rate.triggered.connect(self.silver_rate_function)
        shop_details = QAction('&Shop details',self)
        shop_details.triggered.connect(self.shop_details_function)

        update_menu.addAction(gold_rate)
        update_menu.addSeparator()
        update_menu.addAction(silver_rate)
        update_menu.addSeparator()
        update_menu.addAction(shop_details)

        add_p_d = QAction('&New Product',self)
        add_p_d.triggered.connect(self.add_product_function)

        add_menu.addAction(add_p_d)

        remove_p_d = QAction('&Remove Product',self) 
        remove_p_d.triggered.connect(self.remove_product_function)

        remove_menu.addAction(remove_p_d)

        enter_b_action = QAction('&Beneficiary',self)
        enter_b_action.triggered.connect(self.vyapari_list_function)
        add_b_action = QAction('&Add Beneficiary',self)
        add_b_action.triggered.connect(self.add_vyapari_function)
        lot_action = QAction('&Lot',self)
        lot_action.triggered.connect(self.add_lot_function)

        vyapari_menu.addAction(enter_b_action)
        vyapari_menu.addSeparator()
        vyapari_menu.addAction(add_b_action)
        vyapari_menu.addSeparator()
        vyapari_menu.addAction(lot_action)

        enter_k_action = QAction('&Beneficiary',self)
        enter_k_action.triggered.connect(self.karagir_list_function)
        add_k_action = QAction('&Add Beneficiary',self)
        add_k_action.triggered.connect(self.add_karagir_function)
        dhadi_action = QAction('&Dhadi',self)
        dhadi_action.triggered.connect(self.add_dhadi_function)
        dhadi_status_action = QAction('&Dhadi Status',self)
        dhadi_status_action.triggered.connect(self.status_function)
        update_status_action = QAction('&Update Status',self)
        update_status_action.triggered.connect(self.update_status_function)

        karagir_menu.addAction(enter_k_action)
        karagir_menu.addSeparator()
        karagir_menu.addAction(add_k_action)
        karagir_menu.addSeparator()
        karagir_menu.addAction(dhadi_action)
        karagir_menu.addSeparator()
        karagir_menu.addAction(dhadi_status_action)
        karagir_menu.addSeparator()
        karagir_menu.addAction(update_status_action)

        exit_action = QAction('&Exit',self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close_win)

        exit_menu.addAction(exit_action)


    # ---------------- EVENT LISTENERS FOR THE MENU OPTIONS --------------------------------

    #--------------------------------Search for gst & customer bill-------------------------------------------

    def search_table_function(self):
        frame = self.stack_.currentWidget()
        c = self.category.currentText()
        c1 = self.cat.currentText()
        m = QSqlTableModel()
        m.clear()
        self.item = self.search_.currentText()
        center_item = AlignedItem(Qt.AlignmentFlag.AlignCenter)
        if frame is self.frame5:
            a = self.name.text().strip().lower().replace("'","''")
            b = self.billno.text().strip()
            if b != '' :
                b = int(b)
            d = self.datee.date().toString('dd-MM-yyyy')
            if c == 'Gold':
                m.setTable('buy')
                field = m.fieldIndex('bill_no')
                m.setSort(field,Qt.DescendingOrder)
            else:
                m.setTable('buy_silver')
                field = m.fieldIndex('bill_no')
                m.setSort(field,Qt.DescendingOrder)
            m.select()
            self.result_table.setModel(m)
            self.result_table.setItemDelegate(center_item)
            if self.item == 'Name' or self.item == 'name':
                m.setFilter(f"LOWER(name) LIKE '%{a}%'")
            elif self.item == 'Bill number' or self.item == 'Bill number' or self.item == 'billno':
                m.setFilter(f"bill_no LIKE '%{b}%'")
            elif self.item == 'Date' or self.item == 'date':
                m.setFilter(f"date LIKE '%{d}%'")
            else:
                return
            m.select()
        elif frame is self.frame6:
            a = self.start_date.date().toString('yyyy-MM-dd')
            b = self.end_date.date().toString('yyyy-MM-dd')
            if c1 == 'Gold':
                m.setTable('gst_gold')
            else:
                m.setTable('gst_silver')
            field = m.fieldIndex('bill_no')
            m.setSort(field,Qt.DescendingOrder)
            m.select()
            self.result_t.setModel(m)
            self.result_t.setItemDelegate(center_item)
            expression = "substr(date,7,4)|| '-' ||substr(date,4,2)|| '-' ||substr(date,1,2)"
            m.setFilter(f"{expression} BETWEEN '{a}' AND '{b}'")
            m.select()          
        else:
            return
        
    def refresh_function(self):
        self.search_reset_function()
        self.result_table.setModel(None)
        self.result_t.setModel(None)

    def search_reset_function(self):
        current_widget = self.stack_.currentWidget()
        if current_widget == self.frame5:
            self.category.setCurrentIndex(0)
            self.search_.setCurrentIndex(-1)
            self.name_label.hide()
            self.name.clear()
            self.name.hide()
            self.billno_label.hide()
            self.billno.clear()
            self.billno.hide()
            self.datee.setDate(self.temp_date)
            self.date_label.hide()
            self.datee.hide()
        else:
            self.cat.setCurrentIndex(0)
            self.start_date.setDate(self.temp_date)
            self.end_date.setDate(self.temp_date)

    def home_function(self):
        self.home.emit()
    
    def customer_record_function(self):
        category = None
        category = self.sender()
        t = QTableView()
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        m = QSqlTableModel()
        m.clear()
        center_item = AlignedItem(Qt.AlignmentFlag.AlignCenter)
        if category is not None:
            name = category.text()
            req = name[1:]
        else:
            return
        d = Detail()
        if req == 'Gold Purchase':
            m = d.show_table('buy')  
        elif req == 'Gold Sell':
            m = d.show_table('sell')
        elif req == 'Silver Purchase':
            m = d.show_table('buy_silver')
        elif req == 'Silver Sell':
            m = d.show_table('sell_silver')
        elif req == 'Gold purchase detail':
            m = d.show_table('buy_detail')
        elif req == 'Gold sell detail':
            m = d.show_table('sell_detail')
        elif req == 'Silver purchase detail':
            m = d.show_table('buy_silver_detail')
        elif req == 'Silver sell detail':
            m =d.show_table('sell_silver_detail')
        elif req == 'Gold GST':
            m = d.show_table('gst_gold')
        elif req == 'Silver GST':
            m = d.show_table('gst_silver')
        field = m.fieldIndex('bill_no')
        m.setSort(field,Qt.DescendingOrder) 
        t.setModel(m)
        t.setItemDelegate(center_item)
        self.stack_.addWidget(t)
        self.stack_.setCurrentWidget(t)

    def stock_record_function(self):
        self.stack_.setCurrentWidget(self.frame4)

    def search_function(self):
        temp = None
        temp = self.sender()
        text = temp.text()
        req = text[1:]
        m = QSqlTableModel()
        m.select()
        m.clear()
        self.result_table.setModel(m)
        if req == 'Customer':
            self.stack_.setCurrentWidget(self.frame5)
        else:
            self.stack_.setCurrentWidget(self.frame6)

    #------------------------Combobox event slot---------------------------------------------------

    def show_search_list(self):
        self.item = ''
        select_item = self.search_.currentText()
        self.item = select_item
        if select_item == 'Name' or select_item == 'name':
            self.name.show()
            self.name_label.show()
            self.billno.hide()
            self.billno_label.hide()
            self.date_label.hide()
            self.datee.hide()
        elif select_item == 'Bill number' or select_item == 'bill number' or select_item == 'billno':
            self.billno_label.show()
            self.billno.show()
            self.name_label.hide()
            self.name.hide()
            self.date_label.hide()
            self.datee.hide()
        elif select_item == 'Date' or select_item == 'date':
            self.date_label.show()
            self.datee.show()
            self.name.hide()
            self.name_label.hide()
            self.billno.hide()
            self.billno_label.hide()
        else:
            self.name_label.hide()
            self.name.hide()
            self.date_label.hide()
            self.datee.hide()
            self.billno_label.hide()
            self.billno.hide()

    def validate_text(self,value):

        if not value:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Null Value')
            msg.setText("Enter Gold Rate")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False
        else:
            try:
                int_try = int(value)
                return True
            except ValueError:
                self.show_warning("Invalid number entered")
                return False

    def success_msg(self,t):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Success')
        msg.setText(f"Successfully updated {t}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_warning(self,t):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Invalid')
        msg.setText(t)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def gold_rate_function(self):
        self.stack_.setCurrentWidget(self.frame1)
        data = self.load_config()
        self.curr_g_r.setText(data.get('Gold_Rate'))

    def update_g_r_function(self):
        if self.validate_text(self.g_r_.text()):
            data = self.load_config()
            data['Gold_Rate'] = self.g_r_.text()
            self.write_config(data)
            self.success_msg('Gold Rate')
            return True

    def silver_rate_function(self):
        self.stack_.setCurrentWidget(self.frame2)
        data = self.load_config()
        self.curr_s_r.setText(data.get('Silver_Rate'))

    def update_s_r_function(self):
        if self.validate_text(self.s_r_.text()):
            data = self.load_config()
            data['Silver_Rate'] = self.s_r_.text()
            self.write_config(data)
            self.success_msg('Silver Rate')
            return True

    def clear_fields(self):
        self.g_r_.clear()
        self.s_r_.clear()
        self.curr_g_r.setText('')
        self.curr_s_r.setText('')

    def shop_details_function(self):
        pass

    def add_product_function(self):
        a_widget = Bill()
        a_widget.d_btn.hide()
        self.stack_.addWidget(a_widget)
        self.stack_.setCurrentWidget(a_widget)

    def remove_product_function(self):
        r_widget = Bill()
        r_widget.a_btn.hide()
        self.stack_.addWidget(r_widget)
        self.stack_.setCurrentWidget(r_widget)

    #--------------------------------------Vyapari functions----------------------------------------------

    def vyapari_list_function(self):
        d = Detail()
        self.m7 = QSqlTableModel()
        self.temp_t = QTableView()
        self.s7 = QComboBox()
        self.s7.addItems(['','Name','Firm'])
        self.s7.setEditable(True)
        self.s7.currentTextChanged.connect(self.label_change)
        self.s7_label = QLabel('Search by :')
        s7_l = QHBoxLayout()
        s7_l.addWidget(self.s7_label,stretch=30)
        s7_l.addWidget(self.s7,stretch=70),
        box_l = QHBoxLayout()
        self.ss_label = QLabel('')
        self.ss_label.hide()
        self.ss = QLineEdit()
        self.ss.hide()
        box_l.addWidget(self.ss_label,stretch=30)
        box_l.addWidget(self.ss,stretch=70)
        btn_l =QHBoxLayout()
        self.search7 = QPushButton('Search')
        self.search7.clicked.connect(self.search_vyapari_function)
        self.reset7 = QPushButton('Reset')
        self.reset7.clicked.connect(self.reset7_function)
        btn_l.addWidget(self.search7)
        btn_l.addWidget(self.reset7)
        final = QVBoxLayout()
        final.addLayout(s7_l)
        final.addLayout(box_l)
        final.addLayout(btn_l)
        self.temp_t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        center = AlignedItem(Qt.AlignmentFlag.AlignCenter)
        self.temp_t.setItemDelegate(center)
        self.m7 = d.show_table('vyapari')
        self.m7.select()
        self.temp_t.setModel(self.m7)
        final.addWidget(self.temp_t)
        self.frame7.setLayout(final)
        self.stack_.addWidget(self.frame7)
        self.stack_.setCurrentWidget(self.frame7)

    def add_vyapari_function(self):
        self.reset_vyapari_detail()
        self.stack_.setCurrentWidget(self.frame8)

    def add_vyapari_detail(self):
        a = self.f8.text()
        b = self.n8.text()
        c = self.a8.text()
        d = self.c8.text()
        e = self.g8.text()
        f = self.b8.text()
        g = self.b8_b.text()
        h = self.ifsc8.text()
        i = self.ac8.text()
        j = self.cat8.currentText()

        if a == '' and b == '' and c == '' and d == '' and e == '' and f == '' and g == '' and h == '' and i == '':
            self.show_warning("Nothing to add")
            return
        else:
            self.d.insert_into_vyapari(a,b,c,d,e,f,g,h,i,j)
            self.success_msg("Vyapari")
            self.reset_vyapari_detail()

    def reset_vyapari_detail(self):
        self.f8.clear()
        self.n8.clear()
        self.a8.clear()
        self.c8.clear()
        self.g8.clear()
        self.b8.clear()
        self.b8_b.clear()
        self.ifsc8.clear()
        self.ac8.clear()
        self.cat8.setCurrentIndex(0)

    def add_lot_function(self):
        pass

    def search_vyapari_function(self):
        self.temp_t.clearSelection()
        a = self.s7.currentText()
        if a == 'Name':
            b = self.ss.text()
            if b == '':
                self.validate_text("Enter value to search")
                return
            else:
                for r in range(self.m7.rowCount()):
                    c = self.m7.index(r,1).data()
                    if b == c:
                        i = self.m7.index(r,0)
                        s_m = self.temp_t.selectionModel()
                        s_m.select(i,QItemSelectionModel.Select | QItemSelectionModel.Rows)
                        self.temp_t.scrollTo(i)
                        return
        else:
            b = self.ss.text()
            if b == '':
                self.validate_text("Enter value to search")
                return
            else:
                for r in range(self.m7.rowCount()):
                    c = self.m7.index(r,0).data()
                    if b == c:
                        i = self.m7.index(r,0)
                        s_m = self.temp_t.selectionModel()
                        s_m.select(i,QItemSelectionModel.Select | QItemSelectionModel.Rows)
                        self.temp_t.scrollTo(i)
                        return


    def reset7_function(self):
        self.temp_t.clearSelection()
        self.ss.clear()
        self.ss.hide()
        self.ss_label.hide()
        self.s7.setCurrentIndex(0)

    def label_change(self):
        a = self.s7.currentText()
        a = a if a else self.s7.setCurrentIndex(1)
        a = self.s7.currentText()
        self.ss_label.setText(a)
        self.ss_label.show()
        self.ss.show()

    #------------------------------------------Karagir functions---------------------------------------------

    def karagir_list_function(self):
        pass

    def add_karagir_function(self):
        pass

    def add_dhadi_function(self):
        pass

    def status_function(self):
        pass

    def update_status_function(self):
        pass

    def close_win(self):
        sys.exit()

    #------------------------------initialising database-----------------------

    def init_db(self):

        """ if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else: """
        """ db = QSqlDatabase.addDatabase('QSQLITE')
        cur_dir = Path(__file__).resolve().parent
        db_path = cur_dir/"Stock"/"Stock_database.db"
        db.setDatabaseName(str(db_path))
        if not db.open():
            QMessageBox.critical(self,db.lastError().text())
            return False 
        else:"""
        self.d = Db_Manager()
        self.table_model = QSqlTableModel(self)
        self.table_model.setTable('stock')
        self.table_model.select()
        while self.table_model.canFetchMore():
                    self.table_model.fetchMore()
        return True

    #----------------------Path for json file-----------------------------

    def path_check(self):
        cur_dir = Path(__file__).resolve().parent
        config_path = cur_dir/"Data"/"config.json"
        return config_path

    #-----------------------loading configuration file-------------------------

    def load_config(self):
        p = self.path_check()
        if p.exists():
            try:
                with open(str(p),'r') as file:
                    file_data = json.load(file)
                    return file_data
            except Exception as e:
                print(e)
        else:
            return {}

    #------------------------Writing back to file-----------------------------

    def write_config(self,file_data):
         p = self.path_check()
         if p.exists():
             try:
                 with open(str(p),'w',encoding='utf-8') as file:
                     json.dump(file_data,file,indent=4)
             except Exception as e:
                 print(e)
                     
    #--------------------------Designing layout--------------------------------

    def set_layout(self):
        container_widget = QWidget()
        self.stack_ = QStackedWidget()
        self.frame1 = QFrame()
        self.frame1.setFrameStyle(QFrame.Panel|QFrame.Plain)
        self.frame1.setLineWidth(2)
        self.frame2 = QFrame()
        self.frame2.setFrameStyle(QFrame.Panel|QFrame.Plain)
        self.frame2.setLineWidth(2)
        self.frame3 = QFrame()
        self.frame3.setFrameStyle(QFrame.Panel|QFrame.Plain)
        self.frame3.setLineWidth(2)
        self.frame4 = QFrame()
        self.frame4.setFrameStyle(QFrame.Panel|QFrame.Plain)
        self.frame4.setLineWidth(2)
        self.frame5 = QFrame()
        self.frame5.setFrameStyle(QFrame.Panel|QFrame.Plain)
        self.frame5.setLineWidth(2)
        self.frame6 = QFrame()
        self.frame5.setFrameStyle(QFrame.Panel|QFrame.Plain)
        self.frame6.setLineWidth(2)
        self.gold_rate_label = QLabel('Enter Gold Rate')
        self.g_r_ = QLineEdit()
        self.g_r_.setPlaceholderText('Enter New Gold Rate')
        self.curr_g_r = QLabel()
        self.update_g_r = QPushButton('Update Rate')
        self.update_g_r.pressed.connect(self.update_g_r_function)
        self.update_g_r.released.connect(self.clear_fields)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.gold_rate_label,stretch=20)
        layout1.addWidget(self.g_r_,stretch=20)
        layout1.addWidget(self.curr_g_r,stretch=20)
        layout1.addWidget(self.update_g_r,stretch=20)
        self.frame1.setLayout(layout1)
        self.silver_rate_label = QLabel('Enter Silver Rate')
        self.s_r_ = QLineEdit()
        self.s_r_.setPlaceholderText('Enter new Silver Rate')
        self.curr_s_r = QLabel()
        self.update_s_r = QPushButton('Update Rate')
        self.update_s_r.pressed.connect(self.update_s_r_function)
        self.update_s_r.pressed.connect(self.clear_fields)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.silver_rate_label,stretch=20)
        layout2.addWidget(self.s_r_,stretch=20)
        layout2.addWidget(self.curr_s_r,stretch=20)
        layout2.addWidget(self.update_s_r,stretch=20)
        self.frame2.setLayout(layout2)
        layout3 = QVBoxLayout()
        self.table = QTableView()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        center_item = AlignedItem(Qt.AlignmentFlag.AlignCenter)
        self.table.setItemDelegate(center_item)
        self.table.setModel(self.table_model)
        self.table_model.select()
        layout3.addWidget(self.table)
        self.frame3.setLayout(layout3)
        layout4 = QVBoxLayout()
        self.b = Bill(self)
        layout4.addWidget(self.b)
        self.frame4.setLayout(layout4)
        main_layout = QVBoxLayout()
        layout5 = QVBoxLayout()
        category_layout = QHBoxLayout()
        self.category_label = QLabel('Category :')
        self.category = QComboBox()
        self.category.addItems(['Gold','Silver'])
        category_layout.addWidget(self.category_label,stretch=30)
        category_layout.addWidget(self.category,stretch=70)
        search_by_layout = QHBoxLayout()
        self.search_label = QLabel('Search by :')
        self.search_ = QComboBox()
        self.search_.setEditable(True)
        self.search_.lineEdit().setPlaceholderText('Select from list')
        self.search_.addItems(['Name','Bill number','Date'])
        self.search_.setCurrentIndex(-1)
        self.search_.currentTextChanged.connect(self.show_search_list)
        search_by_layout.addWidget(self.search_label,stretch=30)
        search_by_layout.addWidget(self.search_,stretch=70)
        name_layout = QHBoxLayout()
        self.name_label = QLabel('Name :')
        self.name = QLineEdit()
        name_layout.addWidget(self.name_label,stretch=30)
        name_layout.addWidget(self.name,stretch=70)
        self.name_label.hide()
        self.name.hide()
        bill_layout = QHBoxLayout()
        self.billno_label = QLabel('Bill no. :')
        self.billno = QLineEdit()
        bill_layout.addWidget(self.billno_label,stretch=30)
        bill_layout.addWidget(self.billno,stretch=70)
        self.billno_label.hide()
        self.billno.hide()
        date_layout = QHBoxLayout()
        self.date_label = QLabel('Date :')
        self.datee = QDateEdit()
        self.datee.setCalendarPopup(True)
        self.datee.setDisplayFormat("dd-MM-yyyy")
        din = date.today()
        d = din.day
        m = din.month
        y = din.year
        self.temp_date = QDate(y,m,d)
        self.datee.setDate(self.temp_date)
        date_layout.addWidget(self.date_label,stretch=30)
        date_layout.addWidget(self.datee,stretch=70)
        self.date_label.hide()
        self.datee.hide()
        button_layout = QHBoxLayout()
        button_layout_6 = QHBoxLayout()
        self.s_btn = QPushButton('Search')
        self.ss_btn = QPushButton('Search')
        self.s_btn.clicked.connect(self.search_table_function)
        self.ss_btn.clicked.connect(self.search_table_function)
        self.r_btn = QPushButton('Refresh')
        self.rr_btn = QPushButton('Refresh')
        self.r_btn.clicked.connect(self.refresh_function)
        self.rr_btn.clicked.connect(self.refresh_function)
        self.reset_btn = QPushButton('Reset')
        self.resett_btn = QPushButton('Reset')
        self.reset_btn.clicked.connect(self.search_reset_function)
        self.resett_btn.clicked.connect(self.search_reset_function)
        button_layout.addWidget(self.s_btn)
        button_layout.addWidget(self.r_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout_6.addWidget(self.ss_btn)
        button_layout_6.addWidget(self.rr_btn)
        button_layout_6.addWidget(self.resett_btn)
        result_table_layout = QVBoxLayout()
        self.result_table = QTableView()
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setItemDelegate(center_item)
        result_table_layout.addWidget(self.result_table)
        self.r_t_frame = QFrame()
        self.r_t_frame.setFrameStyle(QFrame.Panel|QFrame.Plain)
        self.r_t_frame.setLineWidth(2)
        self.r_t_frame.setLayout(result_table_layout)
        layout5.addLayout(category_layout)
        layout5.addLayout(search_by_layout)
        layout5.addLayout(name_layout)
        layout5.addLayout(bill_layout)
        layout5.addLayout(date_layout)
        layout5.addLayout(button_layout)
        layout5.addWidget(self.r_t_frame)
        self.frame5.setLayout(layout5)
        layout6 = QVBoxLayout()
        cat_l = QHBoxLayout()
        self.cat_label = QLabel('Category :')
        self.cat = QComboBox()
        self.cat.addItems(['Gold','Silver'])
        cat_l.addWidget(self.cat_label,stretch=30)
        cat_l.addWidget(self.cat,stretch=70)
        start_layout = QHBoxLayout()
        self.start_date_label = QLabel('Start_Date :')
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("dd-MM-yyyy")
        self.start_date.setDate(QDate(y,m,d))
        start_layout.addWidget(self.start_date_label,stretch=30)
        start_layout.addWidget(self.start_date,stretch=70)
        end_layout = QHBoxLayout()
        self.end_date_label = QLabel('End_Date :')
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("dd-MM-yyyy")
        self.end_date.setDate(QDate(y,m,d))
        end_layout.addWidget(self.end_date_label,stretch=30)
        end_layout.addWidget(self.end_date,stretch=70)
        r_l = QVBoxLayout()
        self.result_t = QTableView()
        self.result_t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_t.setItemDelegate(center_item)
        r_l.addWidget(self.result_t)
        layout6.addLayout(cat_l)
        layout6.addLayout(start_layout)
        layout6.addLayout(end_layout)
        layout6.addLayout(button_layout_6)
        layout6.addLayout(r_l)
        self.frame6.setLayout(layout6)
        for i in range(7, 16):  # Generates numbers 7 through 15
            frame = QFrame()
            frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
            frame.setLineWidth(2)
            # Assigns the configured QFrame to self.frame7, self.frame8, ..., self.frame15
            setattr(self, f"frame{i}", frame)
        f8_l = QHBoxLayout()
        self.f8_label = QLabel('Firm :')
        self.f8 = QLineEdit()
        self.f8.setPlaceholderText("Enter the name of firm if exists")
        f8_l.addWidget(self.f8_label,stretch=30)
        f8_l.addWidget(self.f8,stretch=70)
        n8_l = QHBoxLayout()
        self.n8_label = QLabel('Name :')
        self.n8 = QLineEdit()
        self.n8.setPlaceholderText("Enter name of dealer of firm")
        n8_l.addWidget(self.n8_label,stretch=30)
        n8_l.addWidget(self.n8,stretch=70)
        a8_l = QHBoxLayout()
        self.a8_label = QLabel('Address :')
        self.a8 = QLineEdit()
        a8_l.addWidget(self.a8_label,stretch=30)
        a8_l.addWidget(self.a8,stretch=70)
        c8_l = QHBoxLayout()
        self.c8_label = QLabel('Contact :')
        self.c8 = QLineEdit()
        c8_l.addWidget(self.c8_label,stretch=30)
        c8_l.addWidget(self.c8,stretch=70)
        g8_l = QHBoxLayout()
        self.g8_label = QLabel('GST :')
        self.g8 = QLineEdit()
        g8_l.addWidget(self.g8_label,stretch=30)
        g8_l.addWidget(self.g8,stretch=70)
        b8_l = QHBoxLayout()
        self.b8_label = QLabel('Bank Name :')
        self.b8 = QLineEdit()
        b8_l.addWidget(self.b8_label,stretch=30)
        b8_l.addWidget(self.b8,stretch=70)
        b8_b_l = QHBoxLayout()
        self.b8_b_label = QLabel('Branch :')
        self.b8_b = QLineEdit()
        b8_b_l.addWidget(self.b8_b_label,stretch=30)
        b8_b_l.addWidget(self.b8_b,stretch=70)
        ifsc8_l = QHBoxLayout()
        self.ifsc8_label = QLabel('IFSC code :')
        self.ifsc8 = QLineEdit()
        ifsc8_l.addWidget(self.ifsc8_label,stretch=30)
        ifsc8_l.addWidget(self.ifsc8,stretch=70)
        ac8_l = QHBoxLayout()
        self.ac8_label = QLabel('A/C no. :')
        self.ac8 = QLineEdit()
        self.ac8.setPlaceholderText('Enter Account number')
        ac8_l.addWidget(self.ac8_label,stretch=30)
        ac8_l.addWidget(self.ac8,stretch=70)
        cat8_l = QHBoxLayout()
        self.cat8_label = QLabel('Category :')
        self.cat8 = QComboBox()
        self.cat8.addItems(['GOLD','SILVER'])
        cat8_l.addWidget(self.cat8_label,stretch=30)
        cat8_l.addWidget(self.cat8,stretch=70)
        btn8_l = QHBoxLayout()
        self.add_btn8 = QPushButton('ADD')
        self.add_btn8.clicked.connect(self.add_vyapari_detail)
        self.reset_btn8 = QPushButton('RESET')
        self.reset_btn8.clicked.connect(self.reset_vyapari_detail)
        btn8_l.addWidget(self.add_btn8)
        btn8_l.addWidget(self.reset_btn8)
        final8 = QVBoxLayout()
        final8.addLayout(f8_l)
        final8.addLayout(n8_l)
        final8.addLayout(a8_l)
        final8.addLayout(c8_l)
        final8.addLayout(g8_l)
        final8.addLayout(b8_l)
        final8.addLayout(b8_b_l)
        final8.addLayout(ifsc8_l)
        final8.addLayout(ac8_l)
        final8.addLayout(cat8_l)
        final8.addLayout(btn8_l)
        self.frame8.setLayout(final8)
        self.stack_.addWidget(self.frame1)
        self.stack_.addWidget(self.frame2)
        self.stack_.addWidget(self.frame3)
        self.stack_.addWidget(self.frame4)
        self.stack_.addWidget(self.frame5)
        self.stack_.addWidget(self.frame6)
        self.stack_.addWidget(self.frame8)
        main_layout.addWidget(self.stack_)
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

class AlignedItem(QStyledItemDelegate):
    def __init__(self, alignment,parent = None):
        super().__init__()
        self.alignment = alignment

    def initStyleOption(self, option, index):                            #Override exsisting initStyleOption method
        super().initStyleOption(option, index)
        # Override the default text alignment for this cell/column
        option.displayAlignment = self.alignment

""" if __name__ == '__main__':
    app =QApplication([])
    a = Admin()
    a.show()
    app.exec_() """
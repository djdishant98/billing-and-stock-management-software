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
                             QStackedWidget,
                             QStyledItemDelegate
                             )

from PyQt5.QtCore import Qt

from PyQt5.QtGui import (QFont,
                         QStandardItemModel, 
                         QStandardItem,
                         QBrush,
                         QColor,
                         )

from PyQt5.QtSql import QSqlTableModel , QSqlDatabase , QSqlQuery
import json
from pathlib import Path
from Stock.stock import Bill

class Admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.create_menu_bar()
        self.set_layout()
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
        file_menu = menu_bar.addMenu('&File')
        search_menu = menu_bar.addMenu('&Search')
        update_menu = menu_bar.addMenu('&Update')
        add_menu = menu_bar.addMenu('&Add')
        remove_menu = menu_bar.addMenu('&Remove')
        exit_menu = menu_bar.addMenu('&Exit')

        # 3. Create clickable Actions for the 'File' menu
        # Using & before a letter creates a quick keyboard Alt shortcut (e.g., Alt+F)

        c_r_action = QAction('&Customer Record', self)
        c_r_action.setShortcut('Ctrl+R')                           
        c_r_action.triggered.connect(self.customer_record_function)      

        s_r_action = QAction('&Stock Record', self)
        s_r_action.setShortcut('Ctrl+E')
        s_r_action.triggered.connect(self.stock_record_function)                    

        # Append choices to the File dropdown column list
        file_menu.addAction(c_r_action)
        file_menu.addSeparator() # Visual dividing line decoration spacer
        file_menu.addAction(s_r_action)

        # 4. Create actions for the 'Search' menu

        search_action = QAction('&Records', self)
        search_action.triggered.connect(self.search_function)
        search_menu.addAction(search_action)

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

        exit_action = QAction('&Exit',self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)


    # ---------------- EVENT LISTENERS FOR THE MENU OPTIONS --------------------------------
    
    def customer_record_function(self):
        pass

    def stock_record_function(self):
        self.stack_.setCurrentWidget(self.frame4)

    def search_function(self):
        pass

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
        pass

    def remove_product_function(self):
        pass

    #------------------------------initialising database-----------------------

    def init_db(self):

        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase('QSQLITE')
            cur_dir = Path(__file__).resolve().parent
            db_path = cur_dir/"Stock"/"Stock_database.db"
            db.setDatabaseName(str(db_path))
        if not db.open():
            QMessageBox.critical(self,db.lastError().text())
            return False
        else:
            self.table_model = QSqlTableModel(self,db)
            self.table_model.setTable('stock')
            self.table_model.select()
            while self.table_model.canFetchMore():
                        self.table_model.fetchMore()

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
        self.stack_.addWidget(self.frame1)
        self.stack_.addWidget(self.frame2)
        self.stack_.addWidget(self.frame3)
        self.stack_.addWidget(self.frame4)
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

if __name__ == '__main__':
    app =QApplication([])
    a = Admin()
    a.show()
    app.exec_()
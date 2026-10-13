from PyQt5.QtCore import Qt ,QItemSelectionModel

from PyQt5.QtSql import (QSqlDatabase, 
                         QSqlQuery,
                         QSqlTableModel)

from PyQt5.QtWidgets import (QTableView,
                              QLabel,
                              QLineEdit, 
                              QComboBox,
                              QPushButton,
                              QMainWindow,
                              QApplication,
                              QHBoxLayout,
                              QVBoxLayout,
                              QMessageBox,
                              QWidget,
                              QHeaderView,
                              QStyledItemDelegate,
                              QAbstractItemView)

from datetime import datetime , date
import json , os
from pathlib import Path

class Bill(QMainWindow):
    def __init__(self):
        super().__init__()
        cur_dict = Path(__file__).resolve().parent.parent
        config_path = cur_dict/"Data"/"config.json"
        if config_path.exists():
            try:
                with open(str(config_path),'r') as file:
                    data = json.load(file)
                    p_list = data.get("Gold_List")
                    c_list = data.get("Carat")
            except Exception as e:
                print(e)
        else:
            data={}
        #---------------------setting widgets------------------------
        container = QWidget()
        self.p_l = QLabel('Product')
        self.p_ = QComboBox()
        self.p_.addItems(p_list)
        self.c_l = QLabel('Carat')
        self.c_ = QComboBox()
        self.c_.addItems(c_list)
        self.t_l = QLabel('Total Weight')
        self.t_ = QLineEdit()
        self.t_.setPlaceholderText('Enter the weight of dhadi')
        self.q_l = QLabel('Quantity')
        self.q_ = QLineEdit()
        self.q_.setPlaceholderText('Enter number of total pieces')
        self.d_l = QLabel('Date')
        din = date.today()
        din_ = din.strftime('%d-%m-%Y')
        self.d_ = QLabel(din_)
        self.table = QTableView()
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setStyleSheet("""
                QTableView::item:selected {
                                            background-color: #3498db;  
                                            color: #ffffff;              
            }
        """)
        self.a_btn = QPushButton('ADD')
        self.s_btn = QPushButton('SEARCH')
        self.r_btn = QPushButton('RESET')
        self.d_btn = QPushButton('DELETE')

        #----------------------------adding event listener-----------------------------

        self.a_btn.pressed.connect(self.a_function)
        self.a_btn.released.connect(self.a_clear_function)
        self.d_btn.released.connect(self.d_function)
        self.d_btn.released.connect(self.a_clear_function)
        self.s_btn.clicked.connect(self.s_function)
        self.r_btn.clicked.connect(self.r_function)

        self.init_db()
        self.init_model()
        l = QVBoxLayout()
        b_l = QHBoxLayout()
        b_l.addWidget(self.a_btn)
        b_l.addWidget(self.d_btn)
        b_l.addWidget(self.s_btn)
        b_l.addWidget(self.r_btn)
        p_l = QHBoxLayout()
        p_l.addWidget(self.p_l)
        p_l.addWidget(self.p_)
        c_l = QHBoxLayout()
        c_l.addWidget(self.c_l)
        c_l.addWidget(self.c_)
        w_l = QHBoxLayout()
        w_l.addWidget(self.t_l)
        w_l.addWidget(self.t_)
        q_l = QHBoxLayout()
        q_l.addWidget(self.q_l)
        q_l.addWidget(self.q_)
        d_l = QHBoxLayout()
        d_l.addWidget(self.d_l)
        d_l.addWidget(self.d_)
        l.addLayout(p_l)
        l.addLayout(c_l)
        l.addLayout(w_l)
        l.addLayout(q_l)
        l.addLayout(d_l)
        l.addLayout(b_l)
        l.addWidget(self.table)
        container.setLayout(l)
        self.setCentralWidget(container)
        self.showMaximized()

#---------------------------event listener--------------------------------

    def a_function(self):

        a = self.p_.currentText()
        b = self.c_.currentText()
        c = self.q_.text().strip()
        d = self.t_.text().strip()
        dd = self.d_.text()
        flag=0

        if not (a and b and c and d):

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Empty Fields')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText('Enter All Fields')
            msg.exec_()

        else:

            r = self.m.rowCount()

            for r_count in range(r):

                data1 = self.m.index(r_count,1).data()
                data2 = self.m.index(r_count,2).data()

                if data1 == a and data2 == b:

                    data3 = self.m.index(r_count,4).data()
                    data4 = self.m.index(r_count,3).data()
                    data3 = data3 + int(c)
                    data4 = data4 + float(d)
                    self.m.setData(self.m.index(r_count,4),data3)
                    self.m.setData(self.m.index(r_count,3),data4)
                    self.m.setData(self.m.index(r_count,6),self.m.index(r_count,5).data())
                    self.m.setData(self.m.index(r_count,5),dd)
                    flag=1
                    break
                
                else:
                    #self.m.setData(self.m.index(r_count,6),'-')
                    continue
            if flag == 0:    
                self.m.insertRows(r,1)                          #inserting 1 row at r row position
                self.m.setData(self.m.index(r,1),a)
                self.m.setData(self.m.index(r,2),b)
                self.m.setData(self.m.index(r,3),float(d))
                self.m.setData(self.m.index(r,4),int(c))
                self.m.setData(self.m.index(r,5),dd)
                self.m.setData(self.m.index(r,6),'-')
            self.m.submitAll()                                          #commit the records to actual database
            self.m.select()                                             #refresh table view mapping                
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Fields added sucessfully")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Success")
            msg.exec_()

    def a_clear_function(self):
        self.p_.setCurrentIndex(0)
        self.c_.setCurrentIndex(0)
        self.q_.clear()
        self.t_.clear()

#--------------------------------function to search the item in model-------------------

    def s_function(self):
        a = self.p_.currentText()
        b = self.c_.currentText()

        self.table.clearSelection()

        if not (a and b):

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Empty Fields')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText('Nothing to search')
            msg.exec_()

        else:

            for r in range(self.m.rowCount()):
                data1 = self.m.index(r,1).data()
                data2 = self.m.index(r,2).data()    
                if data1 == a and data2 == b:
                    index = self.m.index(r,0)
                    selection_model = self.table.selectionModel()
                    selection_model.select(index,QItemSelectionModel.Select | QItemSelectionModel.Rows)
                    self.table.scrollTo(index)
                    break
                

#-------------------------function to delete item from database---------------------

    def d_function(self):
        pass

#--------------------------------function to reset the fields-------------------

    def r_function(self):
        a = self.p_.currentText()
        b = self.c_.currentText()
        c = self.q_.text().strip()
        d = self.t_.text().strip()
        dd = self.d_.text()

        if not (a and b and c and d):

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('Empty Fields')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText('Fields are already Empty')
            msg.exec_()

        else:

            self.p_.setCurrentIndex(0)
            self.c_.setCurrentIndex(0)
            self.q_.clear()
            self.t_.clear()
            self.table.clearSelection()
            
#-------------------Initialising Database---------------------------------------

    def init_db(self):

        if QSqlDatabase.contains("qt_sql_default_connection"):
            # Re-use the existing active database connection pointer safely
            db = QSqlDatabase.database("qt_sql_default_connection")
        else:
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('Stock_database.db')
        if not db.open():
            QMessageBox.critical(self,db.lastError().text())
            return False
        else:
            query = QSqlQuery()
            query.exec_("""CREATE TABLE IF NOT EXISTS stock(
                            p_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product TEXT,
                            carat TEXT,
                            weight REAL,
                            quantity INT,
                            entry_date TEXT,
                            previous_date TEXT)""")
            #query1 = QSqlQuery()
            #query1.exec_("""ALTER TABLE stock ADD COLUMN previous_date TEXT""")
            return True
        
    def init_model(self):

        self.m = QSqlTableModel(self)
        self.m.setTable('stock')
        self.m.setEditStrategy(QSqlTableModel.OnFieldChange)   #Automatically save changes to the field
        self.m.select()
        self.m.setHeaderData(0,Qt.Horizontal,'p_id')
        self.m.setHeaderData(1,Qt.Horizontal,'product')
        self.m.setHeaderData(2,Qt.Horizontal,'carat')
        self.m.setHeaderData(3,Qt.Horizontal,'weight')
        self.m.setHeaderData(4,Qt.Horizontal,'quantity')
        self.m.setHeaderData(5,Qt.Horizontal,'entry_date')
        self.m.setHeaderData(6,Qt.Horizontal,'previous_date')
        self.table.setModel(self.m)
        center_item = AlignedItem(Qt.AlignmentFlag.AlignCenter,self)
        self.table.setItemDelegate(center_item)


#----------------------creating delegate class for viewing items in table aligned---------------------

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
    b = Bill()
    b.show()
    app.exec_()

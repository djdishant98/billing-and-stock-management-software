from PyQt5.QtCore import Qt ,QItemSelectionModel,QDate

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
                              QAbstractItemView,
                              QStackedWidget)

from datetime import datetime , date
import json , os
from pathlib import Path
from Stock.db import Db_Manager

class Bill(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        cur_dict = Path(__file__).resolve().parent.parent
        config_path = cur_dict/"Data"/"config.json"
        if config_path.exists():
            try:
                with open(str(config_path),'r') as file:
                    data = json.load(file)
                    self.p_list = data.get("Gold_List")
                    self.s_list = data.get("Silver_List")
                    self.c_list = data.get("Carat")
                    self.pt_list = data.get("Purity")
            except Exception as e:
                print(e)
        else:
            data={}
        #---------------------setting widgets------------------------
        container = QWidget()
        self.category_l = QLabel('Category')
        self.category = QComboBox()
        self.category.addItems(['Gold','Silver'])
        self.p_l = QLabel('Product')
        self.p_ = QComboBox()
        self.p_.addItems(self.p_list)
        self.c_l = QLabel('Carat')
        self.c_ = QComboBox()
        self.c_.addItems(self.c_list)
        self.pt_label = QLabel('Purity')
        self.pt_ = QComboBox()
        self.pt_.addItems(self.pt_list)
        self.pt_label.hide()
        self.pt_.hide()
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
        self.d_btn.pressed.connect(self.d_function)
        self.d_btn.released.connect(self.d_clear_function)
        self.d_btn.released.connect(self.a_clear_function)
        self.s_btn.clicked.connect(self.s_function)
        self.r_btn.clicked.connect(self.r_function)
        self.category.currentTextChanged.connect(self.category_change_function)

        self.d = Db_Manager()
        self.m = QSqlTableModel(self)
        self.init_model()
        l = QVBoxLayout()
        b_l = QHBoxLayout()
        b_l.addWidget(self.a_btn)
        b_l.addWidget(self.d_btn)
        b_l.addWidget(self.s_btn)
        b_l.addWidget(self.r_btn)
        cat_l = QHBoxLayout()
        cat_l.addWidget(self.category_l)
        cat_l.addWidget(self.category)
        pt_l = QHBoxLayout()
        pt_l.addWidget(self.pt_label)
        pt_l.addWidget(self.pt_)
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
        l.addLayout(cat_l)
        l.addLayout(p_l)
        l.addLayout(c_l)
        l.addLayout(pt_l)
        l.addLayout(w_l)
        l.addLayout(q_l)
        l.addLayout(d_l)
        l.addLayout(b_l)
        l.addWidget(self.table)
        self.setLayout(l)
        self.showMaximized()

#---------------------------event listener--------------------------------

#--------------------------------Categorize Database acordingly------------------------

    def category_change_function(self):
        category = self.category.currentText()
        self.p_.clear()
        if category == 'Gold':
            self.p_.addItems(self.p_list)
            self.c_l.show()
            self.c_.show()
            self.pt_label.hide()
            self.pt_.hide()
        else:
            self.p_.addItems(self.s_list)
            self.pt_label.show()
            self.pt_.show()
            self.c_l.hide()
            self.c_.hide()
        self.init_model()

    def a_function(self):

        a = self.p_.currentText()
        if self.category.currentText() == 'Gold':
            b = self.c_.currentText()
        else:
            b = self.pt_.currentText()
        c = self.q_.text().strip()
        d = self.t_.text().strip()
        dd = self.d_.text()
        flag=0

        if not (a and b and c and d):
            self.show_msg('Empty Fields','Enter All Fields')
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
            self.show_msg("Success","Fields added sucessfully")

    def a_clear_function(self):
        self.p_.setCurrentIndex(0)
        self.pt_.setCurrentIndex(0)
        self.c_.setCurrentIndex(0)
        self.q_.clear()
        self.t_.clear()

#--------------------------------function to search the item in model-------------------

    def s_function(self):
        a = self.p_.currentText()
        if self.category.currentText() == 'Gold':
            b = self.c_.currentText()
        else:
            b = self.pt_.currentText()
        self.table.clearSelection()
        if not (a and b):
            self.show_msg('Empty Fields','Nothing to search') 
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

#-----------------------display message---------------------------------------

    def show_msg(self,title,message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setText(message)
        msg.exec_()

#-------------------------function to delete item from database---------------------

    def d_function(self):
        a = self.p_.currentText()
        if self.category.currentText() == 'Gold':
            b = self.c_.currentText()
        else:
            b = self.pt_.currentText()
        c = self.q_.text().strip()
        d = self.t_.text().strip()
        dd = self.d_.text()
        flag=0

        if not (a and b and c and d):

            self.show_msg('Empty Fields','Enter All Fields')

        else:

            r = self.m.rowCount()

            for r_count in range(r):

                data1 = self.m.index(r_count,1).data()
                data2 = self.m.index(r_count,2).data()

                if data1 == a and data2 == b:

                    data3 = self.m.index(r_count,4).data()
                    data4 = self.m.index(r_count,3).data()
                    if int(c)<=data3:
                        data3 = data3 - int(c)
                    else:
                        self.show_msg('Empty Fields','Quantity entered is greater than records')
                        self.r_function()                                                   #reset fields for entering valid values
                        return
                    if float(d)<=data4:
                        data4 = data4 - float(d)
                    else:
                        self.show_msg('Empty Fields','Weight entered is greater than records')
                        self.r_function()
                        return
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
            self.show_msg("Success","Deletion successful")

    def d_clear_function(self):
        self.p_.setCurrentIndex(0)
        self.c_.setCurrentIndex(0)
        self.pt_.setCurrentIndex(0)
        self.q_.clear()
        self.t_.clear()

#--------------------------------function to reset the fields-------------------

    def r_function(self):
        a = self.p_.currentText()
        b = self.c_.currentText()
        c = self.q_.text().strip()
        d = self.t_.text().strip()
        dd = self.d_.text()
        if not (c and d):
            self.show_msg('Empty Fields','Fields are already Empty')
        self.p_.setCurrentIndex(0)
        self.c_.setCurrentIndex(0)
        self.q_.clear()
        self.t_.clear()
        self.table.selectionModel().clearSelection()
        self.table.scrollTo(self.m.index(0,0))
            
#-------------------Initialising Database model---------------------------------------

    def init_model(self):

        category = self.category.currentText()
        if category == 'Gold':
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
        else:
            self.m.setTable('stock_silver')
            self.m.setEditStrategy(QSqlTableModel.OnFieldChange)   #Automatically save changes to the field
            self.m.select()
            self.m.setHeaderData(0,Qt.Horizontal,'p_id')
            self.m.setHeaderData(1,Qt.Horizontal,'product')
            self.m.setHeaderData(2,Qt.Horizontal,'Purity')
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


class Detail(QMainWindow):
    def __init__(self):
        super().__init__()
        self.d = Db_Manager()
        self.table = QTableView()
        self.sell = QSqlTableModel()
        self.sell_detail = QSqlTableModel()
        self.buy = QSqlTableModel()
        self.buy_detail = QSqlTableModel()
        self.buy_silver = QSqlTableModel()
        self.buy_silver_detail = QSqlTableModel()
        self.sell_silver = QSqlTableModel()
        self.sell_silver_detail = QSqlTableModel()
        self.gst_gold = QSqlTableModel()
        self.gst_silver = QSqlTableModel()
        self.buy.setTable('buy')
        a = self.buy.fieldIndex('bill_no')
        self.buy.setSort(a,Qt.DescendingOrder)
        self.buy_detail.setTable('buy_detail')
        b = self.buy_detail.fieldIndex('bill_no')
        self.buy_detail.setSort(b,Qt.DescendingOrder)
        self.sell.setTable('sell')
        c = self.sell.fieldIndex('bill_no')
        self.sell.setSort(c,Qt.DescendingOrder)
        self.sell_detail.setTable('sell_detail')
        d = self.sell_detail.fieldIndex('bill_no')
        self.sell_detail.setSort(d,Qt.DescendingOrder)
        self.buy_silver.setTable('buy_silver')
        e = self.buy_silver.fieldIndex('bill_no')
        self.buy_silver.setSort(e,Qt.DescendingOrder)
        self.buy_silver_detail.setTable('buy_silver_detail')
        f = self.buy_silver_detail.fieldIndex('bill_no')
        self.buy_silver_detail.setSort(f,Qt.DescendingOrder)
        self.sell_silver.setTable('sell_silver')
        g = self.sell_silver.fieldIndex('bill_no')
        self.sell_silver.setSort(g,Qt.DescendingOrder)
        self.sell_silver_detail.setTable('sell_silver_detail')
        h = self.sell_silver_detail.fieldIndex('bill_no')
        self.sell_silver_detail.setSort(h,Qt.DescendingOrder)
        self.gst_gold.setTable('gst_gold')
        i = self.gst_gold.fieldIndex('bill_no')
        self.gst_gold.setSort(i,Qt.DescendingOrder)
        self.gst_silver.setTable('gst_silver')
        j = self.gst_silver.fieldIndex('bill_no')
        self.gst_silver.setSort(j,Qt.DescendingOrder)
        self.stack_ = QStackedWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        container_widget = QWidget()
        container_widget.setLayout(layout)
        self.stack_.addWidget(container_widget)
        self.setCentralWidget(self.stack_)

    def show_table(self,table_name):
       
        if table_name == 'buy':
            self.buy.select()
            return self.buy
        elif table_name == 'sell':
            self.sell.select()
            return self.sell
        elif table_name == 'buy_silver':
            self.buy_silver.select()
            return self.buy_silver
        elif table_name == 'sell_silver':
            self.sell_silver.select()
            return self.sell_silver
        elif table_name == 'buy_detail':
            self.buy_detail.select()
            return self.buy_detail
        elif table_name == 'sell_detail':
            self.sell_detail.select()
            return self.sell_detail
        elif table_name == 'buy_silver_detail':
            self.buy_silver_detail.select()
            return self.buy_silver_detail
        elif table_name == 'sell_silver_detail':
            self.sell_silver_detail.select()
            return self.sell_silver_detail
        elif table_name == 'gst_gold':
            self.gst_gold.select()
            return self.gst_gold
        elif table_name == 'gst_silver':
            self.gst_silver.select()
            return self.gst_silver
        else:
            return

    def search_gst(self,table_name):
        pass

    def search_customer(self,table_name):
        pass
    

""" if __name__ == '__main__':
    app =QApplication([])
    b = Bill()
    b.show()
    app.exec_() """

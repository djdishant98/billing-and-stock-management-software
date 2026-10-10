from PyQt5.QtCore import Qt ,QAbstractTableModel
from PyQt5.QtGui import QStandardItemModel , QStandardItem
from PyQt5.QtWidgets import QTableView ,QMainWindow ,QWidget , QApplication
import os
from pathlib import Path

"""class TableModal(QAbstractTableModel):
    def __init__(self,data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        data =[[1,2,3],
               [4,2,7],
               [0,6,8],
               [9,5,7]]
        self.view = QTableView()
        self.m = TableModal(data)
        self.view.setModel(self.m)
        self.resize(400,600)
        self.setCentralidget(self.view)"""

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        data =[[1,2,3],
               [4,2,7],
               [0,6,8],
               [9,5,7]]
        self.view  = QTableView()
        self.m = QStandardItemModel()
        self.m.setHorizontalHeaderLabels(['One','Two','Three'])
        for row , row_data in enumerate(data):
            for col , col_data in enumerate(row_data):
                item = QStandardItem(str(col_data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.m.setItem(row,col,item)
        self.view.setModel(self.m)
        self.setCentralWidget(self.view)
        self.view.setShowGrid(False)
        self.resize(500,700)

if __name__ == '__main__':
    app =QApplication([])
    m = Main()
    m.show()
    print(Path.cwd())
    app.exec_()

from PyQt5.QtWidgets import (QWidget,
                             QMainWindow,
                             QApplication,
                             QLabel,
                             QPushButton,
                             QVBoxLayout,
                             QHBoxLayout)

from PyQt5.QtCore import Qt
from staff import Pilot

class User(QMainWindow):
    def __init__(self):
        super().__init__()
        self.a = QPushButton('Admin')
        self.s = QPushButton('Staff')
        c = QWidget()
        l = QHBoxLayout()
        l.addWidget(self.a)
        l.addWidget(self.s)
        c.setLayout(l)
        self.setCentralWidget(c)
        self.showMaximized()
        self.setStyleSheet("""
                                QPushButton{
                                width:50px;
                                height:50px;
                                background:#0a6ba0;
                                font:50px}""")
        self.second_win = None
    #--------------------------Adding events to button-------------------------------

        self.a.clicked.connect(self.admin_function)
        self.s.clicked.connect(self.staff_function)

    #-------------------------admin function-----------------------------------------

    def admin_function(self):
        pass

    def staff_function(self):

        if self.second_win is None:
            self.second_win = Pilot()
            self.second_win.show()

if __name__ == '__main__':
    app = QApplication([])
    u = User()
    u.show()
    app.exec_()

    
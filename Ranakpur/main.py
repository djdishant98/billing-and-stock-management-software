from PyQt5.QtWidgets import (QWidget,
                             QMainWindow,
                             QApplication,
                             QLabel,
                             QPushButton,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLineEdit,
                             QDesktopWidget,
                             QMessageBox)

from PyQt5.QtCore import Qt
from pathlib import Path
from staff import Pilot
from admin import Admin
import json
import os

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

    #--------------------------layout for admin widget------------------------------

    def admin_layout(self):
         c1 = QWidget()
         self.n_l = QLabel('Username')
         self.n_ = QLineEdit()
         self.p_l = QLabel('Password')
         self.p_ = QLineEdit()
         self.e_btn = QPushButton('Enter')
         n_layout = QHBoxLayout()
         p_layout = QHBoxLayout()
         f_layout = QVBoxLayout()
         n_layout.addWidget(self.n_l)
         n_layout.addWidget(self.n_)
         p_layout.addWidget(self.p_l)
         p_layout.addWidget(self.p_)
         f_layout.addLayout(n_layout)
         f_layout.addLayout(p_layout)
         f_layout.addWidget(self.e_btn)
         self.e_btn.clicked.connect(self.admin_win_function)
         c1.setLayout(f_layout)
         self.showNormal()
         self.setCentralWidget(c1)
         self.resize(500,500)
         self.center_screen_function()

    #-------------------------admin function to display the layout-----------------------------------------

    def admin_function(self):
        self.admin_layout()    

    #------------------------placing the widget to center of screen-------------------

    def center_screen_function(self):
        win_geom = self.frameGeometry()                                          #Get the geometry of the main window framework
        screen_center = QDesktopWidget().availableGeometry().center()            #Find the center point of the current monitor/screen 
        win_geom.moveCenter(screen_center)                                       #Move the center point of the window's geometry to match the screen's center
        self.move(win_geom.topLeft())                                            #Move the actual window to the top-left coordinate of that centered geometry box

    #-----------------------function to display the staff widget layout----------------------------

    def staff_function(self):

        if self.second_win is None:
            self.second_win = Pilot()
            self.second_win.show()

    #-----------------------function to enter admin window--------------------------------

    def admin_win_function(self):
        a = self.n_.text().strip()
        b = self.p_.text().strip()

        if not (a and b):
            
            msg  = QMessageBox(self)
            msg.setWindowTitle('Credentials')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText('Fill all Credentials')
            msg.exec_()

        else:

            try:
                p = r"C:\Users\Da\OneDrive\Desktop\PyQt5\credential.json"

                if not os.path.exists(p):
                    QMessageBox.critical(self, "Error", f"Credential file not found at path:\n{p}")
                    return
                
                with open(p,'r') as file:
                    data = json.load(file)
                    user = data.get('admin_username')
                    passw = data.get('admin_password')

            except json.JSONDecodeError:
                QMessageBox.critical(self, "Error", "Credentials file layout is corrupted.")
                return

            if a == user and b == passw:

                msg  = QMessageBox(self)
                msg.setWindowTitle('Credentials')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setText('Success')
                msg.exec_()
                if self.second_win is None:                           #displaying admin window
                    self.second_win = Admin()
                    self.hide()
                    self.second_win.show()
                    True

            else:

                msg  = QMessageBox(self)
                msg.setWindowTitle('Credentials')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setText('Enter correct details')
                msg.exec_()

                

if __name__ == '__main__':
    app = QApplication([])
    u = User()
    u.show()
    app.exec_()

    
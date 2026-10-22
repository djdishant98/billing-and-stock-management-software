"""from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication , QWidget , QLabel ,QPushButton ,QVBoxLayout ,QHBoxLayout
from random import choice
from PyQt5.QtGui import QFont

class Random(QWidget):
    def __init__(self):
        super().__init__()
        self.colors = ['#015F78','#C11007','#FFDF20','#497D15']
        self.t = QLabel("hello")
        self.b1 = QPushButton("Change Color")
        self.b2 = QPushButton("Reset")
        self.r1 = QHBoxLayout()
        self.r2 = QHBoxLayout()
        self.c1 = QVBoxLayout()
        self.b1.clicked.connect(self.change_color)
        self.b2.clicked.connect(self.reset_b)
        self.r1.addWidget(self.t , alignment=Qt.AlignCenter)
        self.r2.addWidget(self.b1 , alignment=Qt.AlignCenter)
        self.r2.addWidget(self.b2 , alignment=Qt.AlignCenter)
        self.c1.addLayout(self.r1)
        self.c1.addLayout(self.r2)
        #self.c1.setContentsMargins()
        self.setLayout(self.c1)
        self.resize(500,500)

    def change_color(self):
        sss = f'QLabel{{color:{choice(self.colors)}}}'
        self.t.setStyleSheet(sss)

    def reset_b(self):
        self.t.setStyleSheet('QLabel{color:black}')

app=QApplication([])
ra = Random()
ra.setStyleSheet('QWidget{background-color:#F7EEE7} QLabel{font-size:24pt}')
ra.show()
app.exec_()"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QVBoxLayout, QLabel

class RadioExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Select your preference:")
        layout.addWidget(self.label)
        
        # Create radio buttons
        self.radio1 = QRadioButton("Option A")
        self.radio2 = QRadioButton("Option B")
        
        # Connect the toggled signal to a function
        self.radio1.toggled.connect(self.on_toggle)
        self.radio2.toggled.connect(self.on_toggle)
        
        layout.addWidget(self.radio1)
        layout.addWidget(self.radio2)
        
        self.setLayout(layout)
        self.setWindowTitle('PyQt5 Radio Button Example')
        self.show()
        
    def on_toggle(self):
        # Determine which button sent the signal
        button = self.sender()
        if button.isChecked():
            self.label.setText(f"You selected: {button.text()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RadioExample()
    sys.exit(app.exec_())
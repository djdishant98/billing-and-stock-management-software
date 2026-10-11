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
                             QHeaderView)
from PyQt5.QtGui import (QFont,
                         QStandardItemModel, 
                         QStandardItem,
                         QBrush,
                         QColor)

from PyQt5.QtWidgets import QAction, QMessageBox

class Admin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_menu_bar()

    def create_menu_bar(self):
        """Generates a native menu bar at the top of the QMainWindow."""
        # 1. Create the main menu bar manager object hook
        menu_bar = self.menuBar()

        # 2. Add top-level menu categories
        file_menu = menu_bar.addMenu('&File')
        help_menu = menu_bar.addMenu('&Help')

        # 3. Create clickable Actions for the 'File' menu
        # Using & before a letter creates a quick keyboard Alt shortcut (e.g., Alt+F)
        reset_action = QAction('&Reset Form', self)
        reset_action.setShortcut('Ctrl+R') # Optional keyboard shortcut
        reset_action.triggered.connect(self.menu_reset_trigger) # Connect to event listener

        exit_action = QAction('&Exit Application', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close) # Native window close function

        # Append choices to the File dropdown column list
        file_menu.addAction(reset_action)
        file_menu.addSeparator() # Visual dividing line decoration spacer
        file_menu.addAction(exit_action)

        # 4. Create actions for the 'Help' menu
        about_action = QAction('&About Software', self)
        about_action.triggered.connect(self.menu_about_trigger)
        help_menu.addAction(about_action)

    # --- EVENT LISTENERS FOR THE MENU OPTIONS ---
    def menu_reset_trigger(self):
        """Example function called when clicking 'Reset Form' inside the menu bar."""
        # If adding this to your login screen, clear inputs:
        if hasattr(self, 'n_') and hasattr(self, 'p_'):
            self.n_.clear()
            self.p_.clear()

    def menu_about_trigger(self):
        """Example popup alert called when clicking 'About Software'."""
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Billing & Stock Management Software\nVersion 1.0.0")
        msg.exec_()

if __name__ == '__main__':
    app =QApplication([])
    a = Admin()
    a.show()
    app.exec_()
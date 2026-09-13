import sys
from PyQt5.QtWidgets import (QApplication)
from UI import Expense_Tracker

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Expense_Tracker()
    window.show()
    sys.exit(app.exec_())
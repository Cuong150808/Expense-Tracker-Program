import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTableWidget, QMessageBox,
                             QTableWidgetItem, QMenu)
from PyQt5.QtCore import Qt

class Expense_Tracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title_label = QLabel("Expense Tracker")
        self.select_category = QComboBox(self)
        self.input_amount = QLineEdit(self)
        self.save_button =QPushButton("Save", self)

        self.add_another_button = QPushButton("Add Another Expense", self)
        self.reset_button = QPushButton("Reset", self)

        self.actions_button = QPushButton("Actions", self)

        self.expense_table = QTableWidget(self)
        self.expense_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.expense_table.hide()

        self.expenses = []

        self.editing_row = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Expense Tracker Program")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.select_category.addItems([
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Other"
        ])
        self.select_category.setEditable(True)
        self.select_category.lineEdit().setPlaceholderText("Select Category: ")
        self.select_category.lineEdit().setReadOnly(True)
        self.select_category.setCurrentIndex(-1)


        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.select_category)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.input_amount)
        self.input_amount.setPlaceholderText("Enter the amount: ")
        hbox1.addWidget(self.save_button)
        vbox.addLayout(hbox1)

        vbox.addWidget(self.expense_table)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.add_another_button)
        hbox2.addWidget(self.reset_button)

        hbox2.addWidget(self.actions_button)
        self.action_options = QMenu(self)
        self.edit_action = self.action_options.addAction("Edit")
        self.delete_action = self.action_options.addAction("Delete")
        self.actions_button.setMenu(self.action_options)

        vbox.addLayout(hbox2)

        central_widget.setLayout(vbox)

        self.input_amount.setFixedWidth(750)
        self.save_button.setFixedWidth(150)
        self.select_category.setFixedWidth(900)

        vbox.setAlignment(self.select_category, Qt.AlignCenter)
        self.title_label.setAlignment(Qt.AlignCenter)
        hbox1.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QLabel{
                font-size: 40px;
            }
            QComboBox{
                font-size: 20px;
                font-style: italic;
                border: 3px solid black;
                border-radius: 5px;
            }
            QLineEdit{
                font-size: 20px;
                border: 3px solid black;
                border-radius: 5px;
            }
            QPushButton{
                font-size: 20px;
                font-weight: bold;
                border: 3px solid black;
                border-radius: 5px;
            }
        """)

        self.save_button.clicked.connect(self.store_values)
        self.add_another_button.clicked.connect(self.new_expense)
        self.reset_button.clicked.connect(self.reset_table)

        self.delete_action.triggered.connect(self.delete_expense)
        self.edit_action.triggered.connect(self.edit_expense)

    def store_values(self):
        if self.select_category.currentIndex() == -1:
            QMessageBox.warning(self, "Error", "Please select a category!")
            return

        category = self.select_category.currentText()
        amount = self.input_amount.text().strip()

        try:
            amount = float(amount)

        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a number!")
            return

        if amount <= 0:
            QMessageBox.warning(self, "Error", "Please enter a positive number!")
            return

        expense = {
            "category": category,
            "amount": amount
        }

        if self.editing_row is None:
            self.expenses.append(expense)

        else:
            self.expenses[self.editing_row] = expense
            self.editing_row = None

        self.update_table()

        self.input_amount.clear()
        self.select_category.setCurrentIndex(-1)

    def update_table(self):
        if not self.expenses:
            self.expense_table.clear()
            self.expense_table.setRowCount(0)
            self.expense_table.setColumnCount(0)
            self.expense_table.hide()

            QMessageBox.information(self, "No expenses", "There are no expenses left!")
            return

        self.expense_table.show()
        self.expense_table.setColumnCount(2)
        self.expense_table.setHorizontalHeaderLabels(["Category", "Amount"])
        self.expense_table.setRowCount(len(self.expenses) + 1)

        total_expense = 0

        for row, expense in enumerate(self.expenses):
            category = expense["category"]
            amount = expense["amount"]
            total_expense += float(amount)

            self.expense_table.setItem(row, 0, QTableWidgetItem(category))
            self.expense_table.setItem(row, 1, QTableWidgetItem(f"${amount:.2f}"))

        total_row = len(self.expenses)
        self.expense_table.setItem(total_row, 0, QTableWidgetItem("TOTAL"))
        self.expense_table.setItem(total_row, 1, QTableWidgetItem(f"${total_expense:.2f}"))

    def new_expense(self):
        self.editing_row = None

        self.select_category.setCurrentIndex(-1)
        self.input_amount.clear()
        self.input_amount.setFocus()

    def reset_table(self):
        self.expenses.clear()
        self.editing_row = None

        self.input_amount.clear()
        self.select_category.setCurrentIndex(-1)

        self.expense_table.clear()
        self.expense_table.setRowCount(0)
        self.expense_table.setColumnCount(0)
        self.expense_table.hide()

        self.input_amount.setFocus()
        self.select_category.setEnabled(True)
        self.input_amount.setEnabled(True)
        self.save_button.setEnabled(True)

        QMessageBox.information(self, "Reset table", "Table reset!")

    def delete_expense(self):
        row = self.expense_table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Unselected", "No row selected!")
            return

        if row == len(self.expenses):
            QMessageBox.warning(self, "Error", "Total row can't be deleted!")
            return

        del self.expenses[row]
        self.update_table()

    def edit_expense(self):
        row = self.expense_table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Unselected", "No row selected!")
            return

        if row == len(self.expenses):
            QMessageBox.warning(self, "Error", "Total row can't be edited!")
            return

        expense = self.expenses[row]

        self.editing_row = row

        category = expense["category"]
        index = self.select_category.findText(category)

        self.select_category.setCurrentIndex(index)
        self.input_amount.setText(str(expense["amount"]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Expense_Tracker()
    window.show()
    sys.exit(app.exec_())
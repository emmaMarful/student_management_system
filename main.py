from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
import sys
import sqlite3
from Dialogs import AddDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        # self.setGeometry(150, 300, 360, 80)
        # self.setGeometry(200, 300, 500, 320)
        self.setFixedWidth(600)
        self.setFixedHeight(450)

        # file and help menu
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu("&Edit")

        # add student action to file menu
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        # refresh action
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.load_data)
        file_menu.addAction(refresh_action)

        # adds about action to help menu
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        # adds search action to Edit menu
        search_action = QAction("Search", self)
        search_action.triggered.connect(self.searchStudent)
        edit_menu.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_index, row_data in enumerate(cursor):
            self.table.insertRow(row_index)
            for col_index, item_in_rowdata in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(item_in_rowdata)))

        connection.close()
        # self.table.cursor(cursor)

    # insert a record
    def insert(self):
        dialog = AddDialog()
        dialog.exec()

    def searchStudent(self):
        dialog = SearchDialog()
        dialog.exec()


class SearchDialog(QDialog):
    # search dialog UI
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(310)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # enter student's name
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Enter a name")
        layout.addWidget(self.search_name)

        # search student button
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search)
        layout.addWidget(search_btn)

        self.setLayout(layout)

    def search(self):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        # name = self.search_name.text()
        # results = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        # results = cursor.execute("SELECT * FROM students WHERE UPPER(name) = UPPER(?)", (name, ))
        # row = list(results)

        # highlighting searched name on table
        name = self.search_name.text()
        items = mainWindow.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        name_check = cursor.execute("SELECT name FROM students").fetchall()

        str_name_check = []
        for i in name_check:
            str_name_check.append(i[0])

        if name in str_name_check:
            for item in items:
                print(item)
                mainWindow.table.item(item.row(), 1).setSelected(True)

            self.accept()
        else:
            error_message = QMessageBox()
            error_message.setWindowTitle("No Records")
            error_message.setText("No matching records found")
            error_message.setIcon(QMessageBox.Icon.Warning)
            error_message.exec()

        cursor.close()
        con.close()


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
mainWindow.load_data()
sys.exit(app.exec())

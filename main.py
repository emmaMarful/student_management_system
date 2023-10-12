from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        # self.setGeometry(150, 300, 360, 80)
        self.setGeometry(100, 200, 500, 280)

        file_menu = self.menuBar().addMenu("file")
        help_menu = self.menuBar().addMenu("help")

        add_student_action = QAction("add Student", self)
        file_menu.addAction(add_student_action)

        about_action = QAction("about", self)
        help_menu.addAction(about_action)

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


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
mainWindow.load_data()
sys.exit(app.exec())

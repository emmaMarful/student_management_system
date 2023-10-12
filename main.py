from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction
import sys


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

        self.setCentralWidget(self.table)


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec())

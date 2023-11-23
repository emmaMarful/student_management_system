from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QToolBar, QStatusBar, \
    QComboBox, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
from Dialogs import AddDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        # self.setGeometry(150, 300, 360, 80)
        # self.setGeometry(200, 300, 500, 320)
        self.setMinimumSize(600, 500)

        # file and help menu
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu("&Edit")

        # add student action to file menu
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
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
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.searchStudent)
        edit_menu.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)

        # add a toolbar which serves as a shortcut to
        # add and search for students
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # creating a status ba and adding a status bar element

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # detect a click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        editRecords = QPushButton("Edit Record")
        editRecords.clicked.connect(self.edit)

        delRecord = QPushButton("Delete Record")
        delRecord.clicked.connect(self.delete)

        children = self.statusBar.findChildren(QPushButton)
        print(children)

        if children:
            for child in children:
                self.statusBar.removeWidget(child)

        self.statusBar.addWidget(editRecords)
        self.statusBar.addWidget(delRecord)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_index, row_data in enumerate(cursor):
            self.table.insertRow(row_index)
            for col_index, item_in_rowdata in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(item_in_rowdata)))

        # remove status-bar's children after refreshed
        children = self.statusBar.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusBar.removeWidget(child)

        connection.close()
        # self.table.cursor(cursor)

    # insert a record
    def insert(self):
        dialog = AddDialog()
        dialog.exec()

    def searchStudent(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteRecord()
        dialog.exec()


class DeleteRecord(QDialog):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setWindowTitle("Delete Records")
        self.setMinimumSize(150, 90)

        label = QLabel("Do you want to delete this record")
        grid.addWidget(label, 0, 0, 1, 2)

        btnNo = QPushButton("No")
        btnYes = QPushButton("Yes")

        grid.addWidget(btnYes, 1, 0)
        grid.addWidget(btnNo, 1, 1)

        btnNo.clicked.connect(self.DoNot)
        btnYes.clicked.connect(self.delMe)

        self.setLayout(grid)

    def DoNot(self):
        self.accept()

    def delMe(self):
        # get student index from the table
        index_of_currentRow = mainWindow.table.currentRow()
        students_index = mainWindow.table.item(index_of_currentRow, 0).text()

        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (students_index, ))

        con.commit()
        cursor.close()
        con.close()
        mainWindow.load_data()

        # short message to confirm update
        QMessageBox.information(self, "status", "The record has been deleted successfully!")
        self.accept()



class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Records")
        self.setMinimumSize(310, 300)

        layout = QVBoxLayout()

        # get selected student name
        self.index = mainWindow.table.currentRow()
        studentin = mainWindow.table.item(self.index, 1).text()

        # add QLineEdit for name
        self.name = QLineEdit(studentin)
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # Add a combo box for courses
        self.courses = QComboBox()
        courses_list = ['Astronomy', 'Biology', 'Math', 'Physics']
        self.courses.addItems(courses_list)

        # set current course in combo box
        current_course = mainWindow.table.item(self.index, 2).text()
        self.courses.setCurrentText(current_course)
        layout.addWidget(self.courses)

        # add QLineEdit for phoneNumber
        current_ph = mainWindow.table.item(self.index, 3).text()
        self.phone = QLineEdit(current_ph)
        self.phone.setPlaceholderText("Enter the new phone Number")
        layout.addWidget(self.phone)

        # update button
        self.pushButton = QPushButton("Update")
        self.pushButton.clicked.connect(self.update_student)
        layout.addWidget(self.pushButton)

        self.setLayout(layout)

    def update_student(self):
        con = sqlite3.connect("database.db")
        student_index = mainWindow.table.item(self.index, 0).text()

        curser = con.cursor()
        curser.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.name.text(), self.courses.currentText(), self.phone.text(), student_index))

        con.commit()
        curser.close()
        con.close()

        # refresh table
        mainWindow.load_data()

        # short message to confirm update
        QMessageBox.information(self, "status", "The record has been updated!")
        self.accept()


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
        """starts a database connection with sqlite3. converts the user entered name with title.
        store the matching entered name in a name checker and also use a findItems method to
        store the object of the name from the QTableWidgets. append the values of the nameChecker
        in a list. Validate if the name exist from the appended list and select it from the
        QTableWidgets else print an error message with a QMessageBox
        """

        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        # name = self.search_name.text()
        # results = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        # results = cursor.execute("SELECT * FROM students WHERE UPPER(name) = UPPER(?)", (name, ))
        # row = list(results)

        # highlighting searched name on table
        name = self.search_name.text()
        name_title = name.title()

        name_check = cursor.execute("SELECT * FROM students WHERE name = ?", (name_title,))
        items = mainWindow.table.findItems(name_title, Qt.MatchFlag.MatchFixedString)

        # name_check = cursor.execute("SELECT name FROM students").fetchall()

        str_name_check = []
        for i in name_check:
            str_name_check.append(i)

        print(str_name_check)
        if name_title in str_name_check[0][1]:
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

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton
import sqlite3


class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        print("add dialog class has been initiated")
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Enter student's name")
        layout.addWidget(self.student_name)

        print("About to start the combo Box")
        # Add a combo box for courses
        self.course = QComboBox()
        course_name = ['Astronomy', 'Biology', 'Math', 'Physics']
        self.course.addItems(course_name)
        layout.addWidget(self.course)

        # Add a phone number
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Enter phone number")
        layout.addWidget(self.phone)

        # register push button
        submit_btn = QPushButton("Register")
        submit_btn.clicked.connect(self.addStudent)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    # add an addStudent method to add students to the "database.db"
    def addStudent(self):
        # print("Add Student initiated")
        name = self.student_name.text()
        st_course = self.course.itemText(self.course.currentIndex())
        st_phone = self.phone.text()

        con = sqlite3.connect("database.db")
        # print("Database has been connected")

        cursor = con.cursor()
        # print("Cursor has been set")

        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, st_course, st_phone))
        # print("Student has been added")

        con.commit()
        cursor.close()
        con.close()
        self.accept()




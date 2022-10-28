import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QLabel,
    QTableWidget, QGridLayout, QTableWidgetItem, QDialog, QDialogButtonBox,
    QVBoxLayout
)


class GraphicsMW(QWidget):  # Graphics for Main Window
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Project')

        self.chem_input = QLineEdit(self)
        self.chem_input.move(150, 150)
        self.chem_input.resize(75, 30)

        self.chem_input_label = QLabel(self)
        self.chem_input_label.move(100, 100)
        self.chem_input_label.setText('Input a chemical')

        self.enter_btn = QPushButton('Enter', self)
        self.enter_btn.move(200, 100)


class Window(GraphicsMW):  # Main window with an input line to get the formula
    def __init__(self):
        super().__init__()

        self.info = InfoWindow(self.chem_input.text())

        self.initUI()

    def initUI(self):
        self.chem_input.returnPressed.connect(self.enter_btn.click)

        self.enter_btn.clicked.connect(self.input_enter)

    def input_enter(self):  # func that opens the Info window
        self.info = InfoWindow(self.chem_input.text())


class GraphicsIW(QWidget):  # Graphics for Info Window
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 400, 360)
        self.setWindowTitle('Info Window')

        self.ready_btn = QPushButton('Data is ready', self)

        self.table = QTableWidget(self)
        self.table.setRowCount(9)
        self.table.setColumnCount(1)
        self.table.move(10, 10)
        self.table.resize(300, 315)  # width height

        self.table.setVerticalHeaderLabels([
            'Formula', 'Name', 'Group', 'Period', 'Atomic number',
            'Atomic mass', 'Density', 'Melting point', 'Boiling point'
        ])

        self.grid_layout = QGridLayout(self)
        self.grid_layout.addWidget(self.table, 0, 0)
        self.grid_layout.addWidget(self.ready_btn, 0, 1)


class QuestionDialog(QDialog):  # Dialog to ask about adding new element to database
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Create new?')

        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.ok_btn = QDialogButtonBox(q_btn)
        self.ok_btn.accepted.connect(self.accept)
        self.ok_btn.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Do you want to add your chemical to table?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.ok_btn)
        self.setLayout(self.layout)


class InfoWindow(GraphicsIW):  # Window with info about chemical shown as table
    def __init__(self, chem_formula):
        super().__init__()

        self.all_info = []

        self.formula = chem_formula

        self.open = True

        self.initUI()

        self.input_mode = False

        self.ready_btn.clicked.connect(self.get_data)

    def initUI(self):  # The window opens only when formula is ready or when user wants to add an element
        if self.formula:
            self.chem_input_event()
            if self.open:
                self.show()

    def put_data_to_table(self):  # func that puts info from list to table
        if self.all_info:
            row_pos = 0
            col_pos = 0

            for info in self.all_info[0]:
                if info:
                    self.table.setItem(row_pos, col_pos, QTableWidgetItem(str(info)))
                row_pos += 1

    def chem_input_event(self):  # func that sends a query to database and gets info as a list
        with sqlite3.connect('chemicals.db') as db:
            cursor = db.cursor()
            query = f'''
            SELECT *
            FROM Chem_elements
            WHERE Formula = ?
            '''
            cursor.execute(query, [self.formula])
            self.all_info = cursor.fetchall()

        if not self.all_info:
            dlg = QuestionDialog()

            if dlg.exec():
                self.open = True
                self.input_mode = True
            else:
                self.open = False
        else:
            self.put_data_to_table()
            self.ready_btn.hide()

    def get_data(self):  # func that puts the info from table to database
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = []
        for row in range(rows):
            dfr = []  # data from row
            for col in range(cols):
                try:
                    dfr.append(self.table.item(row, col).text())
                except:
                    dfr.append(None)
            data.append(*dfr)
        data.append(None)

        if any(data):
            with sqlite3.connect('chemicals.db') as db:
                cursor = db.cursor()
                query = f'''
                INSERT INTO Chem_elements
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                cursor.execute(query, data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())

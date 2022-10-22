import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QLabel, QTableWidget, QGridLayout, QTableWidgetItem
)
from pyqt5_plugins.examplebutton import QtWidgets


class GraphicsMW(QWidget):
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


class GraphicsIW(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 400, 360)
        self.setWindowTitle('Info Window')

        self.grid_layout = QGridLayout(self)

        self.table = QTableWidget(self)
        self.table.setRowCount(9)
        self.table.setColumnCount(1)
        self.table.move(10, 10)
        self.table.resize(300, 315)  # width height

        self.table.setVerticalHeaderLabels([
            'Formula', 'Name', 'Group', 'Period', 'Atomic number',
            'Atomic mass', 'Density', 'Melting point', 'Boiling point'
        ])

        self.grid_layout.addWidget(self.table, 0, 0)


class InfoWindow(GraphicsIW):
    def __init__(self, chem_formula):
        super().__init__()

        self.all_info = []

        self.formula = chem_formula

        self.chem_input_event()

    def put_data_to_table(self):
        if self.all_info:
            row_pos = 0
            col_pos = 0

            for info in self.all_info[0]:
                self.table.setItem(row_pos, col_pos, QTableWidgetItem(str(info)))
                row_pos += 1

    def chem_input_event(self):
        with sqlite3.connect('chemicals.db') as db:
            cursor = db.cursor()
            query = f'''
            SELECT *
            FROM Chem_elements
            WHERE Formula = ?
            '''
            cursor.execute(query, [self.formula])
            self.all_info = cursor.fetchall()

            self.put_data_to_table()


class Window(GraphicsMW):
    def __init__(self):
        super().__init__()

        self.info = InfoWindow(self.chem_input.text())

        self.initUI()

    def initUI(self):
        self.chem_input.returnPressed.connect(self.enter_btn.click)

        self.enter_btn.clicked.connect(self.input_enter)

    def input_enter(self):
        self.info = InfoWindow(self.chem_input.text())
        self.info.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())

import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QLineEdit, QPushButton, QLabel,
    QDialog, QDialogButtonBox,
    QTableWidget, QTableWidgetItem,
    QVBoxLayout, QGridLayout, QHeaderView, QSizePolicy,
    QScrollArea, QMainWindow, QFrame, QHBoxLayout, QInputDialog,
)
from math import ceil
from re import sub
import os.path

default = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F',
           'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl',
           'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn',
           'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As',
           'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb',
           'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In',
           'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La',
           'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb',
           'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
           'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl',
           'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
           'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk',
           'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db',
           'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh',
           'Fl', 'Mc', 'Lv', 'Ts', 'Og']

if not os.path.exists('default.txt'):
    with open('default.txt', 'w+') as file:
        for element in default:
            file.write(element + '\n')

if not os.path.exists('all_elements.txt'):
    with open('all_elements.txt', 'w+') as file:
        for element in default:
            file.write(element + '\n')

if not os.path.exists('chemicals.db'):
    with sqlite3.connect('chemicals.db') as db:
        cursor = db.cursor()
        query = '''CREATE TABLE IF NOT EXISTS Chem_elements
                (Formula STRING, Name STRING, Section INTEGER,
                Period INTEGER, "Atomic number" INTEGER, "Atomic mass" FLOAT,
                Density FLOAT, "Melting point" FLOAT, "Boiling point" FLOAT)'''
        cursor.execute(query)
        query = '''CREATE TABLE IF NOT EXISTS Chemicals
                (Formula STRING, "Molecular mass" FLOAT, Name STRING,
                Density FLOAT, "Melting point" FLOAT, "Boiling point" FLOAT,
                "Thermal conductivity" FLOAT, "Electrical conductivity" FLOAT)'''
        cursor.execute(query)

with open('all_elements.txt', 'r') as file:
    all_elements = [i.strip('\n') for i in file.readlines()]


class AddingDialog(QDialog):
    def __init__(self, unknown_formula):
        super().__init__()

        self.setWindowTitle('Create new?')

        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.ok_btn = QDialogButtonBox(q_btn)
        self.ok_btn.accepted.connect(self.accept)
        self.ok_btn.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(
            f'Unknown formula found: "{unknown_formula}".' +
            'Do you want to add it to the table?'
        )
        self.layout.addWidget(message)
        self.layout.addWidget(self.ok_btn)
        self.setLayout(self.layout)


'''
This dialog asks user about adding new
element or chemical to the corresponding table.
'''


class AgreementDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Reset?')

        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.ok_btn = QDialogButtonBox(q_btn)
        self.ok_btn.accepted.connect(self.accept)
        self.ok_btn.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.ok_btn)
        self.setLayout(self.layout)


class DeletingDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Delete?')

        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.ok_btn = QDialogButtonBox(q_btn)
        self.ok_btn.accepted.connect(self.accept)
        self.ok_btn.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.ok_btn)
        self.setLayout(self.layout)


'''
This dialog asks user about deleting the
element or chemical from the database.
'''


class ErrorDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Warning')

        q_btn = QDialogButtonBox.Ok

        self.ok_btn = QDialogButtonBox(q_btn)
        self.ok_btn.accepted.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel('Incorrect input!')
        self.layout.addWidget(message)
        self.layout.addWidget(self.ok_btn)
        self.setLayout(self.layout)


'''
This dialog will appear if input is incorrect.
'''


class AskDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Delete?')

        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.ok_btn = QDialogButtonBox(q_btn)
        self.ok_btn.accepted.connect(self.accept)
        self.ok_btn.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel('Do you want to delete this element?')
        self.layout.addWidget(message)
        self.layout.addWidget(self.ok_btn)
        self.setLayout(self.layout)


'''
Dialog to ask user about adding new available element.
'''


class GraphicsMW(QWidget):  # Graphics for Main Window
    def __init__(self):
        super().__init__()

        self.setGeometry(800, 400, 400, 300)  # Window
        self.setWindowTitle('Chemical dictionary')

        self.chem_input = QLineEdit(self)  # Input QLineEdit

        self.chem_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.chem_input.setAlignment(Qt.AlignCenter)
        self.chem_input.setFont(QFont('Libel Suit', 18))

        self.chem_input_label = QLabel(self)  # Label
        self.chem_input_label.setText('Input a chemical. Example: "Al(OH)3"')
        self.chem_input_label.setFont(QFont('Libel Suit', 20))
        self.chem_input_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.chem_input_label.setAlignment(Qt.AlignCenter)

        self.enter_btn = QPushButton('Enter', self)  # Enter button
        self.enter_btn.setFont(QFont('Libel Suit Regular', 20))
        self.enter_btn.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        self.all_elements_list_btn = QPushButton('All elements list', self)
        self.all_elements_list_btn.setFont(QFont('Libel Suit', 12))
        self.chem_input.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()  # Creating layout
        self.layout.addWidget(self.all_elements_list_btn, 0, 1, 1, 1)
        self.layout.addWidget(self.chem_input_label, 1, 1, 1, 1)
        self.layout.addWidget(self.chem_input, 2, 0, 1, 3)
        self.layout.addWidget(self.enter_btn, 3, 0, 1, 3)
        self.setLayout(self.layout)


'''
Class with graphics for Main Window.
'''


class MainWindow(GraphicsMW):
    def __init__(self):
        super().__init__()

        self.elem_info = InfoWindowForElements(self.chem_input.text())
        self.elements_window = None

        self.chem_input.returnPressed.connect(self.enter_btn.click)
        self.enter_btn.clicked.connect(self.input_enter)
        self.all_elements_list_btn.clicked.connect(self.all_elements_list)

    def all_elements_list(self):
        self.elements_window = ElementsWindow()
    '''
        User can change the list of available elements.
    Press 'All elements list' button to see all elements.
    At the end of the list user can press '+' button to add new one
    or click some element to delete it from the list.
    '''

    def input_enter(self):
        open_info = True
        result = Parser().parsing(self.chem_input.text())
        elements = result[0]
        list_of_syntax = result[1]
        if elements == 'Incorrect input':
            dlg = ErrorDialog()
            dlg.exec()
            open_info = False
        if open_info:
            if len(list_of_syntax) == 1:
                self.elem_info = InfoWindowForElements(
                    self.chem_input.text()
                )
            else:
                self.elem_info = InfoWindowForChemicals(
                    self.chem_input.text(), elements
                )
    '''
        When formula is ready user can press 'Enter'
    button on their keyboard or click 'Enter' button on the screen.
    Then formula is parsed (see Parser class) and user gets info
    from database ('Chem_elements' or 'Chemicals' - based on amount of
    elements in the formula and its length).
        If formula was incorrect the dialog (see Error dialog) will appear.
    '''


'''
    User inputs their chemical formula into QLineEdit.
Then it is checked for correctness and parsed.
User gets info from database as a table.
    User can change the list of available elements
in the 'All elements list' window.
'''


class ElementsWindow(QMainWindow):
    def create_buttons(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        btns_in_row = 6
        positions = [(i, j)
                     for i in range(ceil(len(all_elements) / btns_in_row))
                     for j in range(btns_in_row)]
        last_pos = (0, 0)
        for pos, name in zip(positions, all_elements):
            button = QPushButton(name)
            frame = QFrame()
            button.clicked.connect(
                lambda ch, btn=button, w=frame: self.interaction(w, btn)
            )

            hbox = QHBoxLayout(frame)
            hbox.addWidget(button)
            self.layout.addWidget(frame, *pos)
            if name == all_elements[-1]:
                last_pos = (pos[0] + int(not ((pos[1] + 1) % btns_in_row)),
                            (pos[1] + 1) % btns_in_row)

        adding_btn = QPushButton('+')
        frame = QFrame()
        adding_btn.clicked.connect(self.add)

        reset_btn = QPushButton('Reset to default')
        reset_btn.clicked.connect(self.reset)

        hbox = QHBoxLayout(frame)
        hbox.addWidget(adding_btn)

        self.layout.addWidget(frame, *last_pos)
        self.layout.addWidget(reset_btn)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        with open('all_elements.txt', 'w+') as file_to_write:
            if file_to_write:
                known = [i.strip('\n') for i in file_to_write.readlines()]
            else:
                known = []
            for element in all_elements:
                if element not in known:
                    file_to_write.write(element + '\n')
            file_to_write.close()

    def __init__(self):
        super().__init__()

        self.setGeometry(1000, 300, 620, 210)
        self.setWindowTitle('All elements list')

        self.scroll = QScrollArea()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.widget = QWidget()

        self.create_buttons()

        self.initUI()

    def reset(self):
        dlg = AgreementDialog()

        if dlg.exec():
            global all_elements
            with open('default.txt') as d_file:
                all_elements = [i.strip('\n') for i in d_file.readlines()]
            self.create_buttons()

    def add(self):
        name, ok_pressed = QInputDialog.getText(self, 'New element',
                                                'Input new element')
        if ok_pressed:
            if name in all_elements or \
                    not name.isalpha() or \
                    name != name.capitalize():
                dlg = ErrorDialog()
                dlg.exec()
            else:
                all_elements.append(name)
                self.create_buttons()

    def interaction(self, frame, btn):
        dlg = AskDialog()
        if dlg.exec():
            all_elements.remove(btn.text())
            frame.deleteLater()
            self.create_buttons()

    def initUI(self):
        self.show()


'''
    Window with all available elements shown as a list
of buttons with a sqrollbar. User can click on element
to delete it or click '+' to add new element.
Only capitalized strings of letters are accepted.
'''


class GraphicsIWFE(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 500, 360)
        self.setWindowTitle('Element')

        self.ready_btn = QPushButton('Update data', self)

        self.delete_btn = QPushButton('Delete element', self)

        self.table = QTableWidget(self)
        self.table.setRowCount(9)
        self.table.setColumnCount(1)
        self.table.setVerticalHeaderLabels([
            'Formula', 'Name', 'Group', 'Period', 'Atomic number',
            'Atomic mass', 'Density', 'Melting point', 'Boiling point'
        ])
        self.table.setHorizontalHeaderLabels(['Info'])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Columns and rows will take up all the free space

        self.grid_layout = QGridLayout(self)  # Creating layout
        self.grid_layout.addWidget(self.table, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.ready_btn, 0, 0)
        self.grid_layout.addWidget(self.delete_btn, 0, 1)


'''
Class with graphics for InfoWindowForElements class.
'''


class InfoWindowForElements(GraphicsIWFE):
    def __init__(self, chem_formula, dialog_flag=True):
        super().__init__()
        self.all_info = []
        self.formula = chem_formula
        self.open = True
        self.dialog_flag = dialog_flag
        self.ready_btn.clicked.connect(self.update_data)
        self.delete_btn.clicked.connect(self.delete_data)
        self.initUI()
    '''
        The class is called with entered formula.
    It also has an optional parameter to not ask the user
    about adding a new element twice (see in InfoWindowForChemicals class).
    '''

    def initUI(self):
        if self.formula:
            self.elem_input_event()
            if self.open:
                self.show()
    '''
        This func creates window only if self.open flag
    is True and formula is not empty.
    '''

    def elem_input_event(self):
        with sqlite3.connect('chemicals.db') as db:
            cursor = db.cursor()
            query = f'''
                SELECT Formula
                FROM Chem_elements
            '''
            cursor.execute(query)
            known_elements = [i[0] for i in cursor.fetchall()]
        '''
            This query is sent to get a list
        of elements that are already in database.
        '''

        self.table.setItem(0, 0, QTableWidgetItem(str(self.formula)))
        self.table.item(0, 0).setFlags(
            self.table.item(0, 0).flags() & ~Qt.ItemIsEditable
        )

        if self.formula in known_elements:
            with sqlite3.connect('chemicals.db') as db:
                cursor = db.cursor()
                query = f'''
                SELECT *
                FROM Chem_elements
                WHERE Formula = ?
                '''
                cursor.execute(query, [self.formula])
                self.all_info = cursor.fetchall()

            row_pos = 1
            col_pos = 0

            for info in self.all_info[0][1:]:
                if info or info == 0 or info == '0':
                    self.table.setItem(
                        row_pos, col_pos, QTableWidgetItem(str(info))
                    )
                row_pos += 1

        else:  # Asking about adding new element
            if self.dialog_flag:
                dlg = AddingDialog(self.formula)
                if dlg.exec():
                    self.open = True
                else:
                    self.open = False
    '''
        This func fills in the table with the info from db, if element
    is already there and asks user about adding it to db otherwise.
    '''

    def update_data(self):
        with sqlite3.connect('chemicals.db') as db:
            cursor = db.cursor()
            query = f'''
            SELECT Formula
            FROM Chem_elements
            '''
            cursor.execute(query)
            known_elements = [i[0] for i in cursor.fetchall()]

        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = []
        for row in range(rows):  # Collecting data from table
            dfr = []  # data from row
            for col in range(cols):
                try:
                    dfr.append(self.table.item(row, col).text())
                except (Exception,):
                    dfr.append(None)
            data.append(*dfr)

        if data[0] in known_elements:
            with sqlite3.connect('chemicals.db') as db:
                cursor = db.cursor()
                query = f'''
                UPDATE Chem_elements
                SET Formula = ?, Name = ?, Section = ?,
                    Period = ?, [Atomic number] = ?, [Atomic mass] = ?,
                Density = ?, [Melting point] = ?, [Boiling point] = ?
                WHERE Formula = ?
                '''
                cursor.execute(query, data + [self.formula])
        else:
            with sqlite3.connect('chemicals.db') as db:
                cursor = db.cursor()
                query = f'''
                INSERT INTO Chem_elements
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                cursor.execute(query, data)
    '''
        This func updates the db. It fills in the corresponding
    columns with values from the table, if the element is
    already there and creates new row with values from the table otherwise.
    Linked to a button.
    '''

    def delete_data(self):
        dlg = DeletingDialog()

        if dlg.exec():
            with sqlite3.connect('chemicals.db') as db:
                cursor = db.cursor()
                query = f'''
                DELETE FROM Chem_elements
                WHERE Formula = ?
                '''
                cursor.execute(query, [self.formula])
    '''
    This func deletes a row with entered formula from the db.
    Linked to a button.
    '''


'''
    Class creates window with info about element in input.
Sends a query to the database, takes all columns from the row
with the element and fills in the table with it.
If element is not in the database, it will ask user to fill in the
table with info and add it to database.
'''


class GraphicsIWFC(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 500, 360)
        self.setWindowTitle('Chemical')

        self.ready_btn = QPushButton('Update data', self)

        self.delete_btn = QPushButton('Delete chemical', self)

        self.table = QTableWidget(self)
        self.table.setRowCount(8)
        self.table.setColumnCount(1)

        self.table.setVerticalHeaderLabels([
            'Formula', 'Molecular mass', 'Name', 'Density',
            'Melting point', 'Boiling point', 'Thermal conductivity',
            'Electrical conductivity'
        ])
        self.table.setHorizontalHeaderLabels(['Info'])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.table.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        # Columns and rows will take up all the free space

        self.grid_layout = QGridLayout(self)  # Creating layout
        self.grid_layout.addWidget(self.table, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.ready_btn, 0, 0)
        self.grid_layout.addWidget(self.delete_btn, 0, 1)


'''
Class with graphics for InfoWindowForChemicals class.
'''


class InfoWindowForChemicals(GraphicsIWFC):
    def __init__(self, chem_formula, elements):
        super().__init__()

        self.amount_of_elements = elements
        self.unknown_element = InfoWindowForElements('')
        self.all_info = []
        self.formula = chem_formula
        self.open_chemical_window = True
        self.ready_btn.clicked.connect(self.update_data)
        self.delete_btn.clicked.connect(self.delete_data)
        self.initUI()
    '''
        The class is called with entered formula and the
    dictionary {element: amount} (see Parser class).
    '''

    def initUI(self):
        if self.formula:
            self.chem_input_event()
            if self.open_chemical_window:
                self.show()
    '''
        This func creates window only if self.open flag
    is True and formula is not empty.
    '''

    def chem_input_event(self):
        with sqlite3.connect('chemicals.db') as db:
            cursor = db.cursor()
            query = f'''
            SELECT Formula
            FROM Chemicals
            '''
            cursor.execute(query)
            known_chemicals = [i[0] for i in cursor.fetchall()]
        '''
            This query is sent to get a list of chemicals
        that are already in database.
        '''

        with sqlite3.connect('chemicals.db') as db:
            cursor = db.cursor()
            query = f'''
            SELECT Formula
            FROM Chem_elements
            '''
            cursor.execute(query)
            known_elements = [i[0] for i in cursor.fetchall()]
        '''
            This query is sent to get a list of elements that
        are already in database.
        '''

        everything_is_ready = True
        for element in self.amount_of_elements.keys():
            if element not in known_elements:
                everything_is_ready = False
                self.open_chemical_window = False
                dlg = AddingDialog(element)

                if dlg.exec():
                    self.unknown_element = InfoWindowForElements(
                        str(element), False
                    )
                else:
                    self.open_chemical_window = False
                break
        '''
            Checking that all elements in the entered formula
        are already in db. If new element is found,
        'AddingDialog' class will appear and 'InfoWindowForElements'
        class with new element as a parameter will be called.
        Also optional parameter is set to False to not ask user twice.
        '''

        if everything_is_ready:  # No new elements are found
            masses = {}
            for element in self.amount_of_elements.keys():
                with sqlite3.connect('chemicals.db') as db:
                    cursor = db.cursor()
                    query = f'''
                    SELECT [Atomic mass]
                    FROM Chem_elements
                    WHERE Formula = ?
                    '''
                    cursor.execute(query, [element])
                    masses[element] = str(cursor.fetchall()[0][0])
            molecular_mass = 0
            for element in self.amount_of_elements.keys():
                try:
                    molecular_mass += self.amount_of_elements[element] * \
                                      float(masses[element].replace(',', '.'))
                except (Exception,):
                    molecular_mass = 'Incorrect atomic mass'
                    break
            '''
                Here the molecular mass is calculated by accessing
            the database with the elements. If all elements' in
            formula mass is known and it is ok (can be called as float),
            the molecular mass will be calculated, it will be shown as
            'Incorrect atomic mass' otherwise.
            '''

            self.table.setItem(0, 0, QTableWidgetItem(str(self.formula)))
            self.table.item(0, 0).setFlags(
                self.table.item(0, 0).flags() & ~Qt.ItemIsEditable
            )

            self.table.setItem(1, 0, QTableWidgetItem(str(molecular_mass)))
            self.table.item(1, 0).setFlags(
                self.table.item(1, 0).flags() & ~Qt.ItemIsEditable
            )
            '''
                Formula and Molecular mass are set to readonly,
            because they are already known and calculated.
            '''

            if self.formula in known_chemicals:
                with sqlite3.connect('chemicals.db') as db:
                    cursor = db.cursor()
                    query = f'''
                    SELECT *
                    FROM Chemicals
                    WHERE Formula = ?
                    '''
                    cursor.execute(query, [self.formula])
                    self.all_info = cursor.fetchall()

                if self.all_info:
                    row_pos = 2
                    col_pos = 0

                    for info in self.all_info[0][2:]:
                        if info or info == 0 or info == '0':
                            self.table.setItem(
                                row_pos, col_pos, QTableWidgetItem(str(info))
                            )
                        row_pos += 1

            else:
                dlg = AddingDialog(self.formula)

                if dlg.exec():
                    self.open_chemical_window = True
                else:
                    self.open_chemical_window = False
            '''
                The table will be filled in with the info,
            if a chemical is already in db, and user will be asked to add
            the chemical to db otherwise.
            '''
    '''
        This func fills in the table with the info
    from db, if chemical is already there
    and asks user about adding it to db otherwise.
    '''

    def update_data(self):
        with sqlite3.connect('chemicals.db') as db:
            cursor = db.cursor()
            query = f'''
            SELECT Formula
            FROM Chemicals
            '''
            cursor.execute(query)
            known_chemicals = [i[0] for i in cursor.fetchall()]

        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = []
        for row in range(rows):  # Collecting data from table
            dfr = []  # data from row
            for col in range(cols):
                try:
                    dfr.append(self.table.item(row, col).text())
                except (Exception,):
                    dfr.append(None)
            data.append(*dfr)

        if any(data):
            if data[0] in known_chemicals:
                with sqlite3.connect('chemicals.db') as db:
                    cursor = db.cursor()
                    query = f'''
                    UPDATE Chemicals
                    SET Formula = ?, Name = ?, [Molecular mass] = ?,
                    Density = ?, [Melting point] = ?, [Boiling point] = ?,
                    [Thermal conductivity] = ?, [Electrical conductivity] = ?
                    WHERE Formula = ?
                    '''
                    cursor.execute(query, data + [self.formula])
            else:
                with sqlite3.connect('chemicals.db') as db:
                    cursor = db.cursor()
                    query = f'''
                    INSERT INTO Chemicals
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    cursor.execute(query, data)
    '''
        This func updates the db. It fills in
    the corresponding columns with values from the table, if the element is
    already there and creates new row with values from the table otherwise.
    Linked to a button.
    '''

    def delete_data(self):
        dlg = DeletingDialog()

        if dlg.exec():
            with sqlite3.connect('chemicals.db') as db:
                cursor = db.cursor()
                query = f'''
                DELETE FROM Chemicals
                WHERE Formula = ?
                '''
                cursor.execute(query, [self.formula])
    '''
        This func deletes a row with entered formula from the db.
    Linked to a button.
    '''


'''
    Class creates window with info about chemical in input.
Sends a query to the database, takes all columns from the row
with the chemical and fills in the table with it.
If chemical is not in the database, it will ask user to fill in the
table with info and add it to database.
'''


class Parser:
    def grammar_check(self, formula):
        only_elements = formula.replace('(', '').replace(')', '')
        no_nums = ''

        for j in only_elements:
            if not j.isdigit():
                no_nums += j
        only_elements = no_nums

        if not only_elements.isalpha:
            return False

        only_elements = sorted(
            sub(r'([A-Z])', r' \1', only_elements).split(), key=len
        )[::-1]

        if (set(only_elements) - set(all_elements)) or not len(only_elements):
            return False
        return True
    '''
        This func checks the syntax in formula.
    It returns False if wrong elements or symbols are in formula.
    '''

    def parsing(self, formula):
        list_of_syntax = []
        if formula == '':  # Checking the correctness of brackets in formula
            bracket_check = False
        elif formula[0] == ')' or formula[-1] == '(':
            bracket_check = False
        else:
            x = []
            for j in formula:
                if j == '(':
                    x.append(j)
                elif j == ')' and len(x) >= 1:
                    del x[-1]
            if len(x) == 0:
                bracket_check = True
            else:
                bracket_check = False

        if not (bracket_check and self.grammar_check(formula)):
            return ['Incorrect input', list_of_syntax]

        stack = []  # separate different elements, brackets and indexes
        length = len(formula)
        ind = 0
        while ind < length:
            if formula[ind].isalpha():  # separate elements
                if formula[ind].islower():
                    c = stack.pop()
                    c += formula[ind]
                    stack.append(c)
                else:
                    stack.append(formula[ind])
                ind += 1
            elif formula[ind] == '(':  # separate brackets
                stack.append(formula[ind])
                ind += 1
            elif formula[ind] == ')':
                stack.append(formula[ind])
                ind += 1
            else:
                num_str = formula[ind]  # separate indexes
                ind += 1
                while ind < length and formula[ind].isdigit():
                    num_str += formula[ind]
                    ind += 1
                stack.append(num_str)
        list_of_syntax = stack[:]

        length = len(stack) - 1
        # add index '1' after elements and brackets with no index
        tmp_stack = []
        for ind in range(length):
            tmp_stack.append(stack[ind])
            if stack[ind].isalpha():
                if not stack[ind + 1].isdigit():
                    tmp_stack.append("1")
            elif stack[ind] == ')':
                if not stack[ind + 1].isdigit():
                    tmp_stack.append("1")
        tmp_stack.append(stack[-1])
        if stack[length].isalpha():
            tmp_stack.append("1")
        stack = tmp_stack
        if stack[-1] == ')':
            stack.append('1')

        tmp_stack = []
        # show elements as lists [name, amount]
        # the list now is [[name, amount], [name, amount]]
        ind = 0
        length = len(stack)
        if stack[0].isdigit():
            main_factor = int(stack[0])
            ind += 1
        else:
            main_factor = 1
        while ind < length:
            if stack[ind].isalpha():
                tmp_stack.append([stack[ind], stack[ind + 1]])
                ind += 2
            elif stack[ind] == '(':
                tmp_stack.append(stack[ind])
                ind += 1
            elif stack[ind] == ')':
                num = int(stack[ind + 1])
                tmp = []
                c = tmp_stack.pop()
                while ind > 0 and c != '(':
                    c1 = [c[0], str(int(c[1]) * num)]
                    tmp.append(c1)
                    c = tmp_stack.pop()
                tmp_stack.extend(tmp)
                ind += 2
        stack = tmp_stack

        result_dict = {}  # show elements as dicts {name: total}
        for element in stack:
            if element[0] in result_dict:
                count = result_dict[element[0]] + int(element[1]) * main_factor
                result_dict[element[0]] = count
            else:
                result_dict[element[0]] = int(element[1]) * main_factor

        return [result_dict, list_of_syntax]


'''
    Class to parse the inputted formula.
Firstly checks that formula is correct with
grammar_check func and bracket_check flag.
Then it parses the entered formula and returns
the dict {element: amount} for every element in it.
'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()

    sys.exit(app.exec())

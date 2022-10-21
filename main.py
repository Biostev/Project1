import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QLabel, QDialog
)


class InfoWindow(QWidget):
    def __init__(self, chem_formula):
        super().__init__()
        self.setGeometry(200, 200, 200, 200)
        self.setWindowTitle('Info Window')

        self.formula = QLabel(self)
        self.formula.setText(chem_formula)
        self.formula.move(50, 50)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Project')

        self.chem_input = QLineEdit(self)
        self.chem_input_label = QLabel(self)

        self.enter_btn = QPushButton('Enter', self)

        self.chem_info = []

        self.initUI()

    def initUI(self):
        self.chem_input.move(150, 150)
        self.chem_input.resize(75, 30)
        self.chem_input.returnPressed.connect(self.enter_btn.click)

        self.chem_input_label.move(100, 100)
        self.chem_input_label.setText('Input a chemical')

        self.enter_btn.move(200, 100)
        self.enter_btn.clicked.connect(self.input_enter)

    def chem_input_event(self):
        pass

    def input_enter(self):
        global info
        info = InfoWindow(self.chem_input.text())
        info.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())

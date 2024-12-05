import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog
)

class Coffi_Window(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setupUI()

    def setupUI(self):
        labels = ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"]
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(labels)

        self.btn_update.clicked.connect(self.update_data_in_table)

    def update_data_in_table(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute('''
                            select *
                            from coffee
                            ''').fetchall()
        self.tableWidget.setRowCount(len(result))
        for index, item in enumerate(result):
            c_id, grade, degree_of_roasting, \
            ground_or_in_grains, teaste_description, \
            price, packing_volme = item
            self.tableWidget.setItem(0, 0, QTableWidgetItem(str(c_id)))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(grade))
            self.tableWidget.setItem(0, 2, QTableWidgetItem(degree_of_roasting))
            self.tableWidget.setItem(0, 3, QTableWidgetItem(ground_or_in_grains))
            self.tableWidget.setItem(0, 4, QTableWidgetItem(teaste_description))
            self.tableWidget.setItem(0, 5, QTableWidgetItem(price))
            self.tableWidget.setItem(0, 6, QTableWidgetItem(packing_volme))



if __name__ == "__main__":
    app =QApplication(sys.argv)
    ui = Coffi_Window()
    ui.show()
    sys.exit(app.exec())

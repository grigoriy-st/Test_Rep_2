import sqlite3
import sys
import random

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog
)
from pprint import pprint

from django.db.models.expressions import result

DB_NAME = 'coffee.sqlite'

class Coffi_Window(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setupUI()

    def setupUI(self):
        labels = ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"]
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.cellClicked.connect(self.on_cell_clicked)

        self.btn_update.clicked.connect(self.update_data_in_table)
        self.btn_add_entry.clicked.connect(self.add_entry)
        self.btn_edit_entry.clicked.connect(self.edit_entry)


    def update_data_in_table(self):
        con = sqlite3.connect(DB_NAME)
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

            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(c_id)))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(grade))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(degree_of_roasting))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(ground_or_in_grains))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(teaste_description))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(str(packing_volme)))

    def add_entry(self):
        window = Save_Entry_Window()
        window.exec()
        self.update_data_in_table()

    def edit_entry(self):
        entry_id = self.cell_is_clicked()
        if entry_id == None:
            return
        window = Save_Entry_Window()

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        q = f'''
            select *
            from {DB_NAME}
            where id = {entry_id}
            '''
        entry = cur.execute(q).fetchall()

        entry_id, name_of_variety, degree_of_roasting, \
        ground_or_in_grains, taste_description,\
        price, volume = entry[0]
        # Заполнение старыми данными
        self.LE_name_of_the_variety.setText(name_of_variety)
        self.CB_degree_of_roasting.setCurrentText(degree_of_roasting)
        self.CB_ground_or_in_grains.setCurrentText(ground_or_in_grains)
        self.PTE_taste_description.setPlainText(taste_description)
        self.LE_price.setText(price)
        self.CB_volume.setCurrentText(volume)

        window.exec()
        self.update_data_in_table()

    def cell_is_clicked(self):
        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                item = self.item(row, column)
                if item is not None:
                    return self.tableWidget.item(row, 0).text()
        return None




class Save_Entry_Window(QDialog):
    def __init__(self):
        super(Save_Entry_Window, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setupUI()

    def setupUI(self):
        self.btn_save_entry.clicked.connect(self.save_entry)
        # self.second_window.exec_()

    def save_entry(self, is_edit_func=False, entry_id=None):
        if is_edit_func: # проверка на то, является ли вызывающая функция функцией для редактирования
            entry_id = entry_id
        else:
            entry_id = self.generate_entry_id()

        name_of_variety = self.LE_name_of_the_variety.text()
        degree_of_roasting = self.CB_degree_of_roasting.currentText()
        ground_or_in_grains = self.CB_ground_or_in_grains.currentText()
        taste_description = self.PTE_taste_description.toPlainText()
        price = self.LE_price.text()
        volume = self.CB_volume.currentText()

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()

        if is_edit_func:
            # обновление данных в бд
            # _ = cur.execute(f'''
            #                         insert into coffee
            #                         (ID, Grade, Degree_of_roasting, Ground_or_in_grains,
            #                         Teaste_description, Price, Packing_volume)
            #                         values (?, ?, ?, ?, ?, ?, ?)''',
            #                 (entry_id, name_of_variety,
            #                  degree_of_roasting, ground_or_in_grains,
            #                  taste_description, price, volume)
            #                 )
        else:
            _ = cur.execute(f'''
                            insert into coffee
                            (ID, Grade, Degree_of_roasting, Ground_or_in_grains,
                            Teaste_description, Price, Packing_volume) 
                            values (?, ?, ?, ?, ?, ?, ?)''',
                            (entry_id, name_of_variety,
                             degree_of_roasting, ground_or_in_grains,
                             taste_description, price, volume)
                            )
        con.commit()
        con.close()
        self.close()

    def generate_entry_id(self) -> int:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        q = '''
                select id
                from coffee
            '''
        all_ids = cur.execute(q).fetchall()
        all_ids = [int(item[0]) for item in all_ids]
        con.close()

        while True:
            gen_id = random.randint(1, 200)
            if gen_id not in all_ids:
                break
        return gen_id

if __name__ == "__main__":
    app =QApplication(sys.argv)
    ui = Coffi_Window()
    ui.show()
    sys.exit(app.exec())

import sqlite3
import sys
import random

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog
)
from addEditCoffeeForm_ui import CoffeeForm
from main_ui import Main_Window

DB_NAME = "../data/coffee.sqlite"

class Coffi_Window(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Main_Window()
        self.ui.setupUi(self)
        self.setupUI()

    def setupUI(self):
        labels = ["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"]
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget.cellClicked.connect(self.edit_entry)

        self.ui.btn_update.clicked.connect(self.update_data_in_table)
        self.ui.btn_add_entry.clicked.connect(self.create_entry)

    def update_data_in_table(self):
        """ Обновление данны в таблице. """

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        result = cur.execute('''
                            select *
                            from coffee
                            ''').fetchall()
        self.ui.tableWidget.setRowCount(len(result))

        for index, item in enumerate(result):
            c_id, grade, degree_of_roasting, \
            ground_or_in_grains, teaste_description, \
            price, packing_volme = item

            self.ui.tableWidget.setItem(index, 0, QTableWidgetItem(str(c_id)))
            self.ui.tableWidget.setItem(index, 1, QTableWidgetItem(grade))
            self.ui.tableWidget.setItem(index, 2, QTableWidgetItem(degree_of_roasting))
            self.ui.tableWidget.setItem(index, 3, QTableWidgetItem(ground_or_in_grains))
            self.ui.tableWidget.setItem(index, 4, QTableWidgetItem(teaste_description))
            self.ui.tableWidget.setItem(index, 5, QTableWidgetItem(str(price)))
            self.ui.tableWidget.setItem(index, 6, QTableWidgetItem(str(packing_volme)))

    def create_entry(self):
        """ Создание новой записи."""
        self.window = Save_Entry_Window()

        self.window.exec()
        self.update_data_in_table()

    def edit_entry(self, row, column):
        """ Редактирование записи. """
        entry_id = self.ui.tableWidget.item(row, 0).text()
        if entry_id == None:
            return
        self.window1 = Save_Entry_Window()
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        q = f'''
            select *
            from coffee
            where id = {entry_id}
            '''
        entry = cur.execute(q).fetchall()

        entry_id, name_of_variety, degree_of_roasting, \
        ground_or_in_grains, taste_description,\
        price, volume = entry[0]
        # Заполнение старыми данными для дальнейшего редактирования
        self.window1.saving_window.LE_name_of_the_variety.setText(name_of_variety)
        self.window1.saving_window.CB_degree_of_roasting.setCurrentText(degree_of_roasting)
        self.window1.saving_window.CB_ground_or_in_grains.setCurrentText(ground_or_in_grains)
        self.window1.saving_window.PTE_taste_description.setPlainText(taste_description)
        self.window1.saving_window.LE_price.setText(str(price))
        self.window1.saving_window.CB_volume.setCurrentText(str(volume))

        self.window1.saving_window.btn_save_entry.clicked.connect(
                lambda:self.window1.save_entry(True, entry_id))

        self.window1.exec()
        self.update_data_in_table()


class Save_Entry_Window(QDialog):
    def __init__(self):
        super().__init__()
        self.saving_window = CoffeeForm()
        self.saving_window.setupUi(self)
        self.setupUI()

    def setupUI(self):
        self.saving_window.btn_save_entry.clicked.connect(self.save_entry)

    def save_entry(self, is_edit_func=False, entry_id=None):
        """ Сохранение записи. """
        if is_edit_func: # проверка на то, является ли вызывающая функция функцией для редактирования
            entry_id = entry_id
        else:
            entry_id = self.generate_entry_id()

        name_of_variety = self.saving_window.LE_name_of_the_variety.text()
        degree_of_roasting = self.saving_window.CB_degree_of_roasting.currentText()
        ground_or_in_grains = self.saving_window.CB_ground_or_in_grains.currentText()
        taste_description = self.saving_window.PTE_taste_description.toPlainText()
        price = self.saving_window.LE_price.text()
        volume = self.saving_window.CB_volume.currentText()

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()

        if is_edit_func:
            _ = cur.execute(f'''
                                update coffee
                                set grade = ?, degree_of_roasting = ?, ground_or_in_grains = ?,
                                teaste_description = ?, price = ?, packing_volume = ?
                                where id = ?
                                ''', (name_of_variety, degree_of_roasting, ground_or_in_grains,
                                      taste_description, price, volume, entry_id))
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
        """ Генерация уникального id записи. """
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

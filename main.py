import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('venv/minecraft.ui', self)
        self.req_list = {}
        self.def_icon = self.button_item_1.icon()

        self.con = sqlite3.connect("mine_calc.sql")
        self.cur = self.con.cursor()

        self.close_1.hide()
        self.close_2.hide()
        self.close_3.hide()
        self.close_4.hide()
        self.close_5.hide()
        self.close_6.hide()
        self.button_item_2.hide()
        self.button_item_3.hide()
        self.button_item_4.hide()
        self.button_item_5.hide()
        self.button_item_6.hide()
        self.button_item_7.hide()

        self.add_item.clicked.connect(self.to_page_2)
        self.back_btn.clicked.connect(self.to_page_1)
        self.add_item_wo_craft.clicked.connect(self.add_item_wo_craft_f)
        self.reset_req_btn.clicked.connect(self.clear_req)
        self.add_req_item_craft.clicked.connect(self.add_req)
        self.add_craft.clicked.connect(self.add_craft_f)

        self.button_item_1.clicked.connect(self.choose_item_1)
        self.button_item_2.clicked.connect(self.choose_item_2)
        self.button_item_3.clicked.connect(self.choose_item_3)
        self.button_item_4.clicked.connect(self.choose_item_4)
        self.button_item_5.clicked.connect(self.choose_item_5)
        self.button_item_6.clicked.connect(self.choose_item_6)
        self.button_item_7.clicked.connect(self.choose_item_7)

        self.close_1.clicked.connect(self.close_f_1)
        self.close_2.clicked.connect(self.close_f_2)
        self.close_3.clicked.connect(self.close_f_3)
        self.close_4.clicked.connect(self.close_f_4)
        self.close_5.clicked.connect(self.close_f_5)
        self.close_6.clicked.connect(self.close_f_6)

    def get_items(self):
        items = self.cur.execute('''SELECT name FROM resourses''').fetchall()
        list_items = []
        for elem in items:
            list_items.append(elem[0])
        return list_items

    def get_items_with_craft(self):
        items = self.cur.execute('''SELECT name FROM resourses 
        WHERE id IN (SELECT result_item_id FROM crafts)''').fetchall()
        list_items = []
        for elem in items:
            list_items.append(elem[0])
        return list_items

    def to_page_1(self):
        self.pages.setCurrentIndex(0)
        self.append_req_item.clear()

    def to_page_2(self):
        self.pages.setCurrentIndex(1)

        list_items = self.get_items()
        self.append_req_item.addItems(list_items)

    def add_item_wo_craft_f(self):
        item = self.item_wo_craft_name.text().lower()
        list_items = self.get_items()
        image = self.image_name.text()

        if item not in list_items:
            if item != '':
                self.cur.execute(f"""INSERT INTO resourses(name) VALUES('{item.lower()}')""")
                self.con.commit()
                self.statusBar().showMessage(f'Предмет {item.lower()} успешно добавлен')
        else:
            self.cur.execute(f'''UPDATE resourses SET image = "{image}" WHERE name = "{item}"''')
            self.con.commit()
            self.statusBar().showMessage(f'Путь к картинке для предмета {item} обновлен')

    def clear_req(self):
        self.req_items.clear()
        self.req_list.clear()

    def add_req(self):
        if self.append_req_item.currentText() not in self.req_list.keys():
            self.req_list[self.append_req_item.currentText()] = str(self.spinBox_2.value())
        else:
            self.req_list[self.append_req_item.currentText()] = \
                str(int(self.req_list.get(self.append_req_item.currentText())) + self.spinBox_2.value())
        text = ''
        for key, value in self.req_list.items():
            text += f'{str(key)} - {str(value)}\n'
        self.req_items.setPlainText(text)

    def add_craft_f(self):
        crafts = self.cur.execute('''SELECT name FROM resourses WHERE id IN (
        SELECT result_item_id from crafts)''').fetchall()
        craft_list = []
        for elem in crafts:
            craft_list.append(elem[0].lower())

        list_items = self.get_items()
        item = self.result_item.text().lower()

        res_count = self.result_count.value()
        lst1 = []
        for elem in self.req_list.keys():
            id_item = self.cur.execute(f'''SELECT id FROM resourses WHERE name = "{elem}"''').fetchall()[0][0]
            lst1.append(str(id_item))
        req_id = ' ,'.join(lst1)
        req_count = ' ,'.join(self.req_list.values())
        if item in craft_list:
            self.cur.execute(f'''UPDATE crafts SET
            result_item_count = {res_count},
            requirement_items_id = "{req_id}",
            requirement_items_count = "{req_count}"
            WHERE result_item_id = (SELECT id FROM resourses WHERE name = "{item}")''')
            self.con.commit()
            self.statusBar().showMessage(f'Успешно обновлен крафт для предмета: {item}')
        else:
            if item not in list_items:
                self.cur.execute(f'''INSERT INTO resourses(name) VALUES("{item}")''')
                self.con.commit()
            name = self.cur.execute(f'''SELECT id from resourses WHERE name = "{item}"''').fetchall()[0][0]
            self.cur.execute(f'''INSERT INTO 
            crafts(result_item_id, result_item_count, requirement_items_id, requirement_items_count) 
            VALUES({name}, {res_count},
             "{req_id}", "{req_count}")''')
            self.con.commit()
            self.statusBar().showMessage(f'Успешно добавлен крафт для предмета: {item}')

    def choose_item_1(self):
        items = self.get_items_with_craft()

        item, ok = QInputDialog().getItem(self, "Выберети предмет",
                                          "Предметы:", items, 0, False)
        if ok and item != '':
            path = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.button_item_1.setIcon(QIcon(f'images/{path[0][0]}'))
            self.sender().setIconSize(QSize(90, 90))
            self.button_item_2.show()

    def choose_item_2(self):
        items = self.get_items_with_craft()

        item, ok = QInputDialog().getItem(self, "Выберети предмет",
                                          "Предметы:", items, 0, False)
        if ok and item != '':
            path = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.button_item_2.setIcon(QIcon(f'images/{path[0][0]}'))
            self.sender().setIconSize(QSize(90, 90))
            self.button_item_3.show()
            if self.button_item_4.isHidden():
                self.close_1.show()

    def choose_item_3(self):
        items = self.get_items_with_craft()

        item, ok = QInputDialog().getItem(self, "Выберети предмет",
                                          "Предметы:", items, 0, False)
        if ok and item != '':
            path = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.button_item_3.setIcon(QIcon(f'images/{path[0][0]}'))
            self.sender().setIconSize(QSize(90, 90))
            self.button_item_4.show()
            self.close_1.hide()
            if self.button_item_5.isHidden():
                self.close_2.show()

    def choose_item_4(self):
        items = self.get_items_with_craft()

        item, ok = QInputDialog().getItem(self, "Выберети предмет",
                                          "Предметы:", items, 0, False)
        if ok and item != '':
            path = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.button_item_4.setIcon(QIcon(f'images/{path[0][0]}'))
            self.sender().setIconSize(QSize(90, 90))
            self.button_item_5.show()
            self.close_2.hide()
            if self.button_item_6.isHidden():
                self.close_3.show()

    def choose_item_5(self):
        items = self.get_items_with_craft()

        item, ok = QInputDialog().getItem(self, "Выберети предмет",
                                          "Предметы:", items, 0, False)
        if ok and item != '':
            path = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.button_item_5.setIcon(QIcon(f'images/{path[0][0]}'))
            self.sender().setIconSize(QSize(90, 90))
            self.button_item_6.show()
            self.close_3.hide()
            if self.button_item_7.isHidden():
                self.close_4.show()

    def choose_item_6(self):
        items = self.get_items_with_craft()

        item, ok = QInputDialog().getItem(self, "Выберети предмет",
                                          "Предметы:", items, 0, False)
        if ok and item != '':
            path = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.button_item_6.setIcon(QIcon(f'images/{path[0][0]}'))
            self.sender().setIconSize(QSize(90, 90))
            self.button_item_7.show()
            self.close_4.hide()
            self.close_5.show()

    def choose_item_7(self):
        items = self.get_items_with_craft()

        item, ok = QInputDialog().getItem(self, "Выберети предмет",
                                          "Предметы:", items, 0, False)
        if ok and item != '':
            path = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.button_item_7.setIcon(QIcon(f'images/{path[0][0]}'))
            self.sender().setIconSize(QSize(90, 90))
            self.close_5.hide()
            self.close_6.show()

    def close_f_1(self):
        self.button_item_2.setIcon(self.def_icon)
        self.button_item_3.hide()
        self.close_1.hide()

    def close_f_2(self):
        self.button_item_3.setIcon(self.def_icon)
        self.button_item_4.hide()
        self.close_2.hide()
        self.close_1.show()

    def close_f_3(self):
        self.button_item_4.setIcon(self.def_icon)
        self.button_item_5.hide()
        self.close_3.hide()
        self.close_2.show()

    def close_f_4(self):
        self.button_item_5.setIcon(self.def_icon)
        self.button_item_6.hide()
        self.close_4.hide()
        self.close_3.show()

    def close_f_5(self):
        self.button_item_6.setIcon(self.def_icon)
        self.button_item_7.hide()
        self.close_5.hide()
        self.close_4.show()

    def close_f_6(self):
        self.button_item_7.setIcon(self.def_icon)
        self.close_6.hide()
        self.close_5.show()

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    sys.exit(app.exec_())

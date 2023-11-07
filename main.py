import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QButtonGroup, QMessageBox


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('minecraft.ui', self)
        self.req_list = {}
        self.def_icon = self.button_item_1.icon()
        self.images_list = [''] * 7
        self.res_items = []
        self.craft = dict()
        self.spin_boxes = [self.item_count_1, self.item_count_2, self.item_count_3, self.item_count_4,
                           self.item_count_5, self.item_count_6, self.item_count_7]
        self.result_btns = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5, self.item_6, self.item_7,
                            self.item_8, self.item_9, self.item_10, self.item_11, self.item_12, self.item_13,
                            self.item_14, self.item_15, self.item_16, self.item_17, self.item_18, self.item_19,
                            self.item_20, self.item_21, self.item_22]
        self.count_labels = [self.count_1, self.count_2, self.count_3, self.count_4, self.count_5, self.count_6,
                             self.count_7, self.count_8, self.count_9, self.count_10, self.count_11, self.count_12,
                             self.count_13, self.count_14, self.count_15, self.count_16, self.count_17,
                             self.count_18, self.count_19, self.count_20, self.count_21, self.count_22]

        self.con = sqlite3.connect("mine_calc.sql")
        self.cur = self.con.cursor()

        self.button_item_2.hide()
        self.button_item_3.hide()
        self.button_item_4.hide()
        self.button_item_5.hide()
        self.button_item_6.hide()
        self.button_item_7.hide()
        for spinbox in self.spin_boxes:
            spinbox.hide()
        self.crafts.hide()

        self.add_item.clicked.connect(self.to_page_2)
        self.back_btn.clicked.connect(self.to_page_1)
        self.add_item_wo_craft.clicked.connect(self.add_item_wo_craft_f)
        self.reset_req_btn.clicked.connect(self.clear_req)
        self.add_req_item_craft.clicked.connect(self.add_req)
        self.add_craft.clicked.connect(self.add_craft_f)
        self.calculate.clicked.connect(self.count)

        self.button_item_1.clicked.connect(self.choose_item)
        self.button_item_2.clicked.connect(self.choose_item)
        self.button_item_3.clicked.connect(self.choose_item)
        self.button_item_4.clicked.connect(self.choose_item)
        self.button_item_5.clicked.connect(self.choose_item)
        self.button_item_6.clicked.connect(self.choose_item)
        self.button_item_7.clicked.connect(self.choose_item)

        self.close_1.clicked.connect(self.close_f)
        self.close_2.clicked.connect(self.close_f)
        self.close_3.clicked.connect(self.close_f)
        self.close_4.clicked.connect(self.close_f)
        self.close_5.clicked.connect(self.close_f)
        self.close_6.clicked.connect(self.close_f)

        self.item_group_btn = QButtonGroup()
        self.item_group_btn.addButton(self.button_item_1, id=1)
        self.item_group_btn.addButton(self.button_item_2, id=2)
        self.item_group_btn.addButton(self.button_item_3, id=3)
        self.item_group_btn.addButton(self.button_item_4, id=4)
        self.item_group_btn.addButton(self.button_item_5, id=5)
        self.item_group_btn.addButton(self.button_item_6, id=6)
        self.item_group_btn.addButton(self.button_item_7, id=7)

        self.close_group_btn = QButtonGroup()
        self.close_group_btn.addButton(self.close_1, id=1)
        self.close_group_btn.addButton(self.close_2, id=2)
        self.close_group_btn.addButton(self.close_3, id=3)
        self.close_group_btn.addButton(self.close_4, id=4)
        self.close_group_btn.addButton(self.close_5, id=5)
        self.close_group_btn.addButton(self.close_6, id=6)
        for button in self.close_group_btn.buttons():
            button.hide()

        self.result_group_btn = QButtonGroup()
        for index, res in enumerate(self.result_btns):
            self.result_group_btn.addButton(res, id=index + 1)
            res.clicked.connect(self.info)
            res.hide()
            self.count_labels[index].hide()

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
            if item != '' or image != '':
                self.cur.execute(f"""INSERT INTO resourses(name, image) VALUES('{item.lower()}', '{image}')""")
                self.con.commit()
                self.statusBar().showMessage(f'Предмет {item.lower()} успешно добавлен')
            else:
                self.statusBar().showMessage('Ошибка')
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
        req_id = ', '.join(lst1)
        req_count = ', '.join(self.req_list.values())
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

    def count(self):
        res_dict = dict()
        self.res_items.clear()
        count_items = [self.item_count_1.value(), self.item_count_2.value(), self.item_count_3.value(),
                       self.item_count_4.value(), self.item_count_5.value(), self.item_count_6.value(),
                       self.item_count_7.value()]
        items = self.images_list.copy()
        for i, elem in enumerate(items):
            if elem:
                keys = self.cur.execute(f'''SELECT requirement_items_id FROM crafts
                WHERE result_item_id =
                (SELECT id FROM resourses WHERE image = "{elem}")''').fetchall()[0][0].split(', ')
                values = self.cur.execute(f'''SELECT requirement_items_count FROM crafts
                WHERE result_item_id =
                (SELECT id FROM resourses WHERE image = "{elem}")''').fetchall()[0][0].split(', ')
                req = []
                for index, k in enumerate(keys):
                    key = self.cur.execute(f'''SELECT name FROM resourses WHERE id = "{k}"''').fetchall()[0][0]
                    req.append(key)
                    if key not in self.get_items_with_craft():
                        if key not in res_dict.keys():
                            res_dict[key] = int(values[index]) * count_items[i]
                        else:
                            res_dict[key] = res_dict.get(key) + int(values[index]) * count_items[i]
                    else:
                        count_items.append(int(values[index]) * count_items[i])
                        img = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{key}"''').fetchall()[0][0]
                        items.append(img)
                        print(f'{key}, {elem}')
                name = self.cur.execute(f'''SELECT name FROM resourses WHERE image = "{elem}"''').fetchall()[0][0]
                self.craft[name] = req
        self.craft.clear()

        result = 0
        for j, r in enumerate(self.result_btns):
            r.hide()
            self.count_labels[j].hide()
        for item, count in res_dict.items():
            image = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.result_group_btn.button(result + 1).show()
            self.result_group_btn.button(result + 1).setIcon(QIcon(f'images/{image[0][0]}'))
            self.result_group_btn.button(result + 1).setIconSize(QSize(55, 55))
            self.count_labels[result].show()
            self.count_labels[result].setText(f'x {int(count)}')
            self.res_items.append(item)
            result += 1
        self.crafts.show()

    def info(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        i = self.result_group_btn.id(self.sender()) - 1
        msg.setText(f'Этот предмет: {self.res_items[i]}')
        msg.setWindowTitle('Информация о предмете')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def choose_item(self):
        items = self.get_items_with_craft()

        item, ok = QInputDialog().getItem(self, "Выберети предмет",
                                          "Предметы:", items, 0, False)
        if ok and item != '':
            i = self.item_group_btn.id(self.sender())
            path = self.cur.execute(f'''SELECT image FROM resourses WHERE name = "{item}"''').fetchall()
            self.sender().setIcon(QIcon(f'images/{path[0][0]}'))
            self.sender().setIconSize(QSize(90, 90))
            if i != 7:
                self.item_group_btn.button(i + 1).show()
            if i > 1:
                for button in self.close_group_btn.buttons():
                    button.hide()
                self.close_group_btn.button(i - 1).show()
            self.spin_boxes[i - 1].show()
            self.images_list[i - 1] = f'{path[0][0]}'

    def close_f(self):
        i = self.close_group_btn.id(self.sender())
        self.item_group_btn.button(i + 1).setIcon(self.def_icon)
        if i != 6:
            self.item_group_btn.button(i + 2).hide()
        self.sender().hide()
        if i != 1:
            self.close_group_btn.button(i - 1).show()
        self.spin_boxes[i].setValue(1)
        self.spin_boxes[i].hide()
        self.images_list[i] = ''

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    sys.exit(app.exec_())

import csv
from config import menu_path
class Menu:

    def csv_reader(file_obj, type):
        reader = csv.reader(file_obj)
        rows = []
        for row in reader:
            if row[0] == type:
                rows.append(row)
        return rows

    def load_menu(type_m):
        with open(menu_path, "r", encoding="UTF8") as f_obj:
            return Menu.csv_reader(f_obj, type_m)

    def load_menu_m(zak):
        keys = zak.keys()
        message = ""
        for member in keys:
            items = list(zak[member])
            rows = Menu.load_menu(member)
            for row in rows:
                for i in items:
                    if row[1] == i:
                        message += row[2] + " " + row[3] + " р. \n"
        return message
import random
import time
import vk_api.vk_api
from menu import Menu

class Dialog:

    def __init__(self, name):
        self.last_msg = None
        self.curr_win = "main"
        self.order = {}
        self.name = name
        self.menu_num = ["горячее", "холодное", "десерт", "напиток", "комбо"]
        self.address = ""
        self.code = str(random.randint(1000, 9999))
        
    def process_msg(self, msg):

        if self.last_msg == None:
            self.last_msg = msg
            self.curr_win = "main"
            self.last_menu = ""
            return """
                    &#128270; Список команд​:
                    1. Открыть меню​
                    2. О нас
                    3. Команды для бота """
        
        self.last_msg = msg 
        
        if msg == "н":
            self.last_msg = None
            self.order.clear()
            return self.process_msg("сброс")
            
        if msg.startswith("з "): 
            if self.last_menu in self.menu_num: 
                print(msg.lstrip('з '))
                if self.last_menu in self.order.keys():
                    nz = self.order[self.last_menu]
                    self.order[self.last_menu] = nz + " " + msg.lstrip('з ')
                else:
                    self.order[self.last_menu] = msg.lstrip('з ')
            print(self.order)
            return "Заказ дополнен"
            
        if msg.startswith("а "): 
            self.address = msg.lstrip('а ')
            return "Адрес установлен"
            
        if msg.startswith("м"): 
            self.curr_win = "main"
            self.last_menu = ""
            return self.process_msg("1")
            
        if self.curr_win == "main":

            if msg == "1":
                self.curr_win = "menu"
                return """&#127869; Меню​
                    1. Горячие блюда
                    2. Холодные блюда
                    3. Десерт​
                    4. Напитки​
                    5. Комбо сезона
                    6. Заказать​
                    7. Отменить заказ
                    8. Назад
                    9. Команды для бота
                    """
                    
        
            if msg == "2":
                return """&#10067;
                          Информация о нас"""
        
            if msg == "3":
                return """&#10071;
                          H - #Отменить заказ и вернуться в начало#
                          З 'номер блюда или блюд через пробел' - #Сделать заказ в выбранном меню#
                          А 'ваш адрес через пробел' - #Задать адрес доставки#
                          М - #Вернуться  меню#"""
            else:
                return "?"
        
        if self.curr_win == "menu":
            
            if msg == "1":  
                self.last_menu = "горячее"
                return "горячее"
            
            if msg == "2":
                self.last_menu = "холодное"
                return "холодное"
                
            if msg == "3":
                self.last_menu = "десерт"
                return "десерт"
                
            if msg == "4":
                self.last_menu = "напиток"
                return "напиток"
            
            if msg == "5":
                self.last_menu = "комбо"
                return "комбо"
                
            if msg == "6":
                self.curr_win = "order"
                return """&#10068; Заказ
                          1. На месте 
                          2. Доставка
                          3. Назад"""
                
            if msg == "7":
                self.last_msg = None
                self.order.clear()
                return self.process_msg("назад")
                
            if msg == "8":
                self.last_msg = None
                return self.process_msg("назад")
                
            if msg == "9":
                return """&#10071;
                          H - #Отменить заказ и вернуться в начало#
                          З 'номер блюда или блюд через пробел' - #Сделать заказ в выбранном меню#
                          А 'ваш адрес через пробел' - #Задать адрес доставки#
                          М - #Вернуться  меню#"""
                          
            else:
                return "?"
        if self.curr_win == "order":
            
            if msg == "1":
                self.curr_win = "order_m"
                return """&#10068; Заказ:
                          """ + Menu.load_menu_m(self.order) + self.address + """
                          #Невозможно изменение заказа после выбора адреса#
                            1. Адрес 1
                            2. Адрес 2
                            3. Назад"""
            
            if msg == "2":
                self.curr_win = "order_d"
                return """&#10068; Заказ:
                          """ + Menu.load_menu_m(self.order) + self.address + """
                          1. Подтвердить
                          2. Отмена 
                          3. Назад"""
                          
            if msg == "3":
                self.curr_win = "main"
                self.last_menu = ""
                return self.process_msg("1")
                
            else:
                return "?"
        if self.curr_win == "order_m":
            
            if msg == "1":
                return """/\\&#9989; Заказ будет готов в течении часа.
                          С этим кодом """ + self.code + """ обратитесь в нашу кассу для получения и оплаты заказа
                          Приятного аппетита!
                          Заказ:
                          """ + Menu.load_menu_m(self.order)

                            
                
            
            if msg == "2":
                return """/\\&#9989; Заказ будет готов в течении часа.
                          С этим кодом """ + self.code + """ обратитесь в нашу кассу для получения и оплаты заказа
                          Приятного аппетита!
                          Заказ:
                          """ + Menu.load_menu_m(self.order)
                
            if msg == "3":
                self.curr_win == "menu"
                return self.process_msg("6")
                
            else:
                return "?"
        if self.curr_win == "order_d":
            
            if msg == "1":
                if self.address == "":
                    return """Введите адрес:
                    А 'ваш адрес через пробел' - #Задать адрес доставки#
                    """
                else:
                    return """/\\&#9989; Доставка по адресу """ + self.address + """ подтверждена.
                    Заказ:
                    """ + Menu.load_menu_m(self.order)
            
            if msg == "2":
                self.last_msg = None
                self.order.clear()
                return """&#10060; Заказ отменён"""
                
            if msg == "3":
                self.curr_win == "menu"
                return self.process_msg("6")
                
            else:
                return "?"



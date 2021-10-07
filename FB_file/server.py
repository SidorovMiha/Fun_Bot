import random
import time
import string
import vk_api.vk_api
import requests

from config import logoURL
from vk_api.upload import VkUpload
from menu import Menu
from io import BytesIO
from dialog import Dialog

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

class Server:

    
    def __init__(self, api_token, group_id, response_id, server_name: str="Empty"):
        
        self.server_name = server_name
        self.group_id = group_id
        self.response_id = response_id
        print(server_name + " group_id:" + group_id)
        self.users = {}
        self.vk = vk_api.VkApi(token=api_token)
        self.vk_api = self.vk.get_api()
        self.upload = VkUpload(self.vk_api)
        self.menu_num = ["горячее", "холодное", "десерт", "напиток", "комбо"]
        print("load longpoll")
        self.long_poll = VkBotLongPoll(self.vk, group_id, wait=30)
        print("longpoll loaded")
        
        
    def upload_photo(self, upload, url):
    
        img = requests.get(url).content 
        f = BytesIO(img)
        response = upload.photo_messages(f)[0]
        owner_id = response['owner_id']
        photo_id = response['id']
        access_key = response['access_key']
        return owner_id, photo_id, access_key


    def send_photo(self, peer_id, message, owner_id, photo_id, access_key):
    
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self.vk_api.messages.send(random_id = time.time(), message=message, peer_id=peer_id, attachment=attachment)
        return 'фото отправленно'

    def menu_send(self, PEER_ID, type):
        rows = Menu.load_menu(type)
        for member in rows:
            message = member[1] + ". " + member[2] + " " + member[3] + " р."
            url = member[4]   
            self.send_photo(PEER_ID, message, *self.upload_photo(self.upload, url))


    def send_msg(self, send_id, message):
        
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id = time.time())
        return 'сообщение отправленно'
        
    def start(self):
        for event in self.long_poll.listen():  
            if event.type == VkBotEventType.MESSAGE_NEW:
            
                msg = str.lower(event.message.text)
                
                if event.message.peer_id in self.users:
                    r_msg = self.users[event.message.peer_id].process_msg(msg)
                    if r_msg in self.menu_num:
                        self.menu_send(event.message.peer_id, r_msg)
                        m_msg = """&#127869; Меню​
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
                        self.menu_send(event.message.peer_id, m_msg)
                    elif r_msg.startswith("/\\"): 
                        r_msg = r_msg.lstrip('/\\')
                        self.send_msg(event.message.peer_id, r_msg)  
                        self.send_msg(self.response_id, r_msg)
                    else:
                        self.send_msg(event.message.peer_id, r_msg)    
                        print("id:"+ str(event.message.peer_id) + " Cообщение:" + msg)
               
                
                if event.message.peer_id not in self.users:
                    user_get = self.vk_api.users.get(user_ids=(event.message.peer_id))
                    info = user_get[0]
                    self.users[event.message.peer_id] = Dialog(info['first_name'])
                    message = """Добро пожаловать! К вашим услугам, """ + info['first_name'] + "."
                    self.send_photo(event.message.peer_id, message, *self.upload_photo(self.upload, logoURL))
                    self.send_msg(event.message.peer_id, self.users[event.message.peer_id].process_msg(""))
                    print("Новый юзер:" + str(event.message.peer_id) + " " + info['first_name'])

                
                
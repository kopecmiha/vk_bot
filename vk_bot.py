import vk_api
import json
import random
import requests
import transliterate
from vk_api.longpoll import VkLongPoll, VkEventType
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id' : random.randint(0, 999999999999999999999999999999999)})

def getjson(url, data = None):
    response = requests.get(url, params = data)
    response = response.text
    return response

def org():
	write_msg(event.user_id, "Какой тип квеста")
	write_msg(event.user_id, "Корпоратив, Детский день рождения, Взрослый день рождения")

def org_hard():
    write_msg(event.user_id, "Выберите сложность")
    write_msg(event.user_id, "Легкий, Средний, Сложный")

def org_time():
    write_msg(event.user_id, "Выберите время прохождения")
    write_msg(event.user_id, "30 минут, 60 минут, 90 минут, Свой вариант")

def org_time_svoi():
    write_msg(event.user_id, "Введите время в минутах")
    
def org_place():
    write_msg(event.user_id, "Передайте геолокацию примерного места проведения")

def org_rad():
    write_msg(event.user_id, "Введите радиус вокруг места проведения")

def uchastnic():
    write_msg(event.user_id, "Введите ID")

def get_cord(ID):
    msg = getjson("https://api.vk.com/method/messages.getById", {
         'message_ids' : ID,
         'access_token' : token,
         'v' : '5.101'
         })
    msg = json.loads(msg)
    #msg = msg[msg.find("[") + 1 :msg.rfind("]")]
    msg = msg["response"]
    msg = msg["items"]
    msg = msg[0]["geo"]
    msg = msg["coordinates"]
    lat = msg["latitude"]
    long = msg['longitude']
    org_rad()

def org_team():
    write_msg(event.user_id, "Введите название команды")

def org_end(team):
    write_msg(event.user_id, "ID Команды")
    if ord(team[0])>=65 and ord(team[0])<= 122:
        teamID = "ID" + str(random.randint(0, 2000)) + team
    else:
        teamID = "ID" + str(random.randint(0, 2000)) + transliterate.translit(team, reversed=True)
    write_msg(event.user_id, teamID)

token = "1b1e3a491bf270d2711ee7ee81407a68e6a561f8bac6dc6509d337ac646ba00101f59b7b028abc20c97ff"
vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk, wait=25, mode=234, preload_messages=True, group_id='186273393')

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
        
            request = event.text
            ID = event.message_id
            if request == "Привет":
                write_msg(event.user_id, "Привет")
            elif request == "Хочу квест":
                org()
            elif request == "Участвую в квесте":
               uchastnic()
            elif request == "Корпоратив" or request == "Детский день рождения" or request == "Взрослый день рождения":
               org_hard()
            elif request == "Легкий" or request == "Средний" or request == "Сложный":
               org_time()
            elif request == "Место":
               get_cord(ID)
            elif request == "Свой вариант":
               org_time_svoi()
            elif request.find("минут")> -1:
                org_place()
            elif request.find("Радиус") > -1:
                org_team()
            elif request.find("Команда:") > -1:
                org_end(request[request.find(":") + 2:len(request)])


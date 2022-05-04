from datetime import date
from random import randrange
import time
import requests

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = '0958750174482253c31483e132a96c88aa890529dfe797f60e04beb97f8522441c78629e31f280bcd644c'

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


def calc_user_age(bdate):
    list_date = bdate.split('.')
    today = date.today()
    year = today.year - int(list_date[2])
    if today.month > int(list_date[1]):
        if today.day > int(list_date[0]):
            year += 1
    return year


def get_user_data(user_id):
    res = vk.method('users.get', {'user_ids': user_id, 'fields': 'bdate, city, sex'})
    temp_gender = 1 if res[0]['sex'] == 2 else 2
    temp_city = res[0]['city']
    temp_age = calc_user_age(res[0]['bdate'])
    info = [temp_gender, temp_city, temp_age]
    return info


def generation_age(info):
    age = info[2]
    if info[0] == 1:
        age_from = age
        age_to = age + 3
    else:
        age_from = age - 3
        age_to = age
    return [age_from, age_to]


def search_bitches(info):
    result = generation_age(info)
    return vk.method('users.search', {'hometown': info[1], 'sex': info[0], 'age_from': result[0], 'age_to': result[1]})


while True:
    time.sleep(5)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            # получить данніе юзера
            user_data = get_user_data(event.user_id)
            if event.to_me:
                request = event.text

                if request == "привет":
                    write_msg(event.user_id, f"Хай, {event.user_id}")
                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                elif request == "покажи шлюх":
                    result = search_bitches(user_data)
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")

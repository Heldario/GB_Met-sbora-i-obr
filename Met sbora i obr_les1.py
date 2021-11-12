# Задача 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

print('======================')
print('Задача 1')
print('======================')

import requests
import json
from pprint import pprint

user = 'Heldario'
url = f'https://api.github.com/users/{user}/repos'

# Здесь не понял как содержимое репозитория получить
# url2 = f'https://api.github.com/repos/{user}/Repository-2'

response = requests.get(url)
j_data = response.json()

# print(response.status_code)
# print(response.text)
# pprint(j_data)
n = len(j_data)
print('For user', user, f'there are {n} repository/-ies:')
for i in range(n):
    print(j_data[i]['name'])

with open('les1_to_json.json', 'w') as f:
    json.dump(j_data, f)

# Задача 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
# Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.

print('======================')
print('Задача 2')
print('======================')

token_vk = 'xxx'
method_vk = 'groups.get'
url_vk = f'https://api.vk.com/method/{method_vk}?v=5.52&access_token={token_vk}&v=5.131'

response_vk = requests.get(url_vk)
j_data_vk = response_vk.json()

print(f'There are some groups:')

print(j_data_vk['response']['items'])
# С выводом названий сообществ не стал заморачиваться.
# Делается вызовом метода groups.getById с передачей параметру group_ids полученных items
# Задача 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

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

# with open('les1_to_json.json', 'w') as f:
#     json.dump(j_data, f)
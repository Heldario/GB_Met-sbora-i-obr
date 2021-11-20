# Задача 1. Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('192.168.16.165', 27017)

db = client['vacancies_supejob_1611']
vacancies = db.vacancies

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36'}
url = 'https://russia.superjob.ru'

page = 1
tag_next = 'Дальше'
while tag_next == 'Дальше':
    params = {'keywords': 'python',
              'page': page}
    response = requests.get(url + '/vacancy/search/', params = params, headers = headers)
    dom = BeautifulSoup(response.text, 'html.parser')

    # Проверяем на наличие кнопки "Дальше" для пагинации
    tag_next = dom.find('a', {'class': 'icMQ_ bs_sM _3ze9n _1M2AW f-test-button-dalshe f-test-link-Dalshe'})
    try:
        tag_next = tag_next.getText()
    except:
        tag_next = None
    page = page + 1

    tag_divs = dom.find_all('div', {'class': 'f-test-search-result-item'})
    # href = tag_div.findChildren('a', {'href': re.compile('^/vakansii')}) #/vakansii/qa-avtomatizator-39705235.html
    # for kk in href:
    #     pprint(kk['href'])

    for tag_div in tag_divs:
        for tag in tag_div:
            vacancy_data ={}
            try:
                tag_a = tag.find('a')
                name = tag_a.getText()
                tag_salary = tag.find('span', {'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'})
                # pprint(tag_salary)
                salary_text = tag_salary.getText()
                # print(salary_text)
                salary_min = None
                salary_max = None
                salary_avg = None
                if salary_text == 'По договорённости':
                    pass
                elif salary_text.find('—') != -1: # от - до
                    b = salary_text.find('—')
                    salary_min = re.findall('\d+', salary_text[:b])
                    salary_max = re.findall('\d+', salary_text[b:])
                    salary_min = int(''.join(salary_min))
                    salary_max = int(''.join(salary_max))
                elif salary_text.find('от') != -1:
                    salary = re.findall('\d+', salary_text)
                    salary_min = int(''.join(salary))
                elif salary_text.find('до') != -1:
                    salary = re.findall('\d+', salary_text)
                    salary_max = int(''.join(salary))
                else:
                    salary = re.findall('\d+', salary_text)
                    salary_avg = int(''.join(salary))

                link = url + tag_a['href']

                # Заводим id для документа в БД
                k = link.rfind('-')
                # link_id = re.findall('\d+', link[k+1:]) - так не работает
                link_id = int(link[k + 1:].replace(".html", ""))

                vacancy = {"_id": link_id,
                           "name": name,
                           "salary_min": salary_min,
                           "salary_avg": salary_avg,
                           "salary_max": salary_max,
                           "salary_text": salary_text,
                           "link": link}

                # Заполняем БД вакансиями
                try:
                    vacancies.insert_one(vacancy)
                    print("Вакансия с данными параметрами добавлена в базу:")
                    pprint(vacancy)
                except dke:
                    # print("Вакансия с данными параметрами уже есть в базе:")
                    # pprint(vacancy)
                    pass

            except:
                pass

print(f'Общее число вакансий в базе: {vacancies.find().count()}')

salary_in = input("Введите зарплату ")
salary_in = int(salary_in)

# Выводим вакансии с заработной платой больше введённой суммы
for vac in vacancies.find({'$or': [
                                    {'salary_min': {'$gte': salary_in}},
                                    {'salary_max': {'$gte': salary_in}}
                                    ]}):
    pprint(vac)
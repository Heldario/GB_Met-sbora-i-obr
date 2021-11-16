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

with open('supejob_vakansies_to_csv.csv', 'w') as f:
    f.write('{0} )^{1}^{2}^{3}^{4}^{5}^{6}\n'.format('0', 'Наименование вакансии', 'Зарплата', 'Мин', 'Сред', 'Макс',
                                                     'Ссылка'))
i = 1
serials_list = []


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
            serial_data ={}
            try:
                tag_a = tag.find('a')
                name = tag_a.getText()
                # print(name)

                tag_salary = tag.find('span', {'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'})
                # pprint(tag_salary)
                salary_text = tag_salary.getText()
                # print(salary_text)
                salary_min = None
                salary_max = None
                salary_avg = None
                if salary_text == 'По договорённости':
                    # salary_avg = None
                    pass
                elif salary_text.find('—') != -1: # от - до
                    b = salary_text.find('—')
                    salary_min = re.findall('\d+', salary_text[:b])
                    salary_max = re.findall('\d+', salary_text[b:])
                    salary_min = ''.join(salary_min)
                    salary_max = ''.join(salary_max)
                elif salary_text.find('от') != -1:
                    salary = re.findall('\d+', salary_text)
                    salary_min = ''.join(salary)
                elif salary_text.find('до') != -1:
                    salary = re.findall('\d+', salary_text)
                    salary_max = ''.join(salary)
                else:
                    salary = re.findall('\d+', salary_text)
                    salary_avg = ''.join(salary)
                # print(f'salary_text: {salary_text}\n'
                #       f'salary_min: {salary_min}\n'
                #       f'salary_avg: {salary_avg}\n'
                #       f'salary_max: {salary_max}')

                link = url + tag_a['href']
                # print(link)
                with open('supejob_vakansies_to_csv.csv', 'a') as f:
                    f.write('{0} )^{1}^{2}^{3}^{4}^{5}^{6}\n'.format(i, name, salary_text, salary_min, salary_avg, salary_max, link))
                    i = i + 1

                serial_data['name'] = name
                serial_data['salary_text'] = salary_text
                serial_data['salary_min'] = salary_min
                serial_data['salary_avg'] = salary_avg
                serial_data['salary_max'] = salary_max
                serial_data['link'] = link
                serials_list.append(serial_data)
            except:
                pass

# pprint(serials_list)
with open('supejob_vakansies_to_json.json', 'w') as f:
    json.dump(serials_list, f)
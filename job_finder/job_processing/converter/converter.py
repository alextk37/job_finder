import requests
import json
import os
from datetime import datetime as dt

currency_url = 'https://v6.exchangerate-api.com/v6/4b1b0621cacc12680baad742/latest/USD'
currency_path = os.path.abspath('job_processing/converter/currency_data')


def make_file_name():
    """
    Функция для создания имени файла с текущей датой.
    Формат имени файла: 'день-месяц-год currency.json'.
    """
    f = '%d-%m-%Y'
    now = dt.now()
    name = dt.strftime(now, f) + ' ' + 'currency' + ' ' + '.json'
    return name


def load_currency():
    """
    Функция для загрузки данных о валюте из API и сохранения их в файл.
    Имя файла определяется с помощью функции make_file_name.
    """
    file_path = os.path.join(currency_path, make_file_name())
    response = requests.get(currency_url)
    data = response.json()

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def check_fresh():
    """
    Проверка актуальности данных о валюте.
    Если данные не актуальны или их нет,
    функция удаляет старые файлы и загружает новые данные.
    """
    if os.listdir(currency_path):
        files = os.listdir(currency_path)
        if files[0] != make_file_name():
            for file_name in files:
                file_path = os.path.join(currency_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            load_currency()
    else:
        load_currency()


def converter(currency, sallary):
    """
    Функция для конвертации зарплаты из одной валюты в рубли.
    Проверяем актуальность данных о валюте,
    Открываем файл с данными, извлекаем курсы валют.
    """
    check_fresh()
    file_name = os.listdir(currency_path)[0]
    file_path = os.path.join(currency_path, file_name)

    with open(file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        currency_data = json_data.get('conversion_rates')
    if currency in currency_data or currency == 'BYR':
        if currency == 'BYR':
            currency = 'BYN'
        currency_course = currency_data.get(currency)
        rub_course = currency_data.get('RUB')
        rub = (sallary / currency_course) * rub_course
        return int(rub)
    return None

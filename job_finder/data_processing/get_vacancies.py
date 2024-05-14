from datetime import datetime as dt
from rich.progress import Progress
from data_processing.etc.carcass import Parser
import os
import requests
import json
import time


class HeadHunterParser(Parser):
    '''
        Класс, используемый для парсинга вакансий с HeadHunter.



        Атрибуты:
        ________
        url : str
            URL API HeadHunter
        headers : dict
            заголовки для использования в запросе API
        params : dict
            параметры для использования в запросе API
        keyword : str
            ключевое слово для поиска в вакансиях
        amount : int
            количество страниц вакансий для получения
        vacancies : list
            список полученных вакансий
        now : datetime
            текущая дата и время

        Методы:
        ______
        connection():
            Получает вакансии с API HeadHunter.
        save_data():
            Сохраняет полученные вакансии в файл JSON.
    '''

    def __init__(self, keyword, amount) -> None:
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '',
                       'page': 0,
                       'per_page': 10
                       }
        self.keyword = keyword
        self.amount = amount
        self.vacancies = []
        self.now = dt.now()

    def connection(self):
        self.params['text'] = self.keyword
        with Progress() as progress:
            task = progress.add_task("[red]Загружаем данные...",
                                     total=self.amount)
            while not progress.finished:
                while self.params.get('page') != self.amount:
                    response = requests.get(self.url,
                                            headers=self.headers,
                                            params=self.params)
                    vacancies = response.json()['items']
                    self.vacancies.extend(vacancies)
                    self.params['page'] += 1
                    progress.update(task, advance=1)
                    time.sleep(0.02)

    def save_data(self):
        f = '%d-%m-%Y %H:%M:%S'
        name = dt.strftime(self.now, f) + ' ' + self.keyword + ' ' + '.json'
        abs_path = os.path.abspath('data_processing/save_data')
        file_path = os.path.join(abs_path, name)
        with open(file_path, 'w') as json_file:
            json.dump(self.vacancies, json_file, ensure_ascii=False)

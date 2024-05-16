import json
from job_processing.vacancy import Vacancy
from data_processing.get_local import LocalData


class Vacanccies:
    '''
    Конструктор класса Vacanccies.

    '''

    def __init__(self, num_file) -> None:
        self.num_file = num_file
        self.vacanccies_list = []

    def vac_counter(self):
        '''
        Метод возвращает количество вакансий в списке.

        '''

        return len(self.vacanccies_list)

    def vac_append(self):
        '''
        Метод добавляет вакансии в список из указанного файла.

        '''

        files = LocalData()
        vac_file = files.get_path(self.num_file)
        with open(vac_file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            for data in json_data:
                chunk = {'name': data.get('name'),
                         'salary': data.get('salary'),
                         'url': data.get('alternate_url'),
                         'employer': data.get('employer'),
                         'snippet': data.get('snippet')
                         }
                self.vacanccies_list.append(Vacancy(**chunk))

    def vac_all(self):
        '''
        Метод возвращает все вакансии из списка.

        '''

        return self.vacanccies_list

    def vac_top(self, amount):
        '''
        Метод возвращает топ "n" вакансий по зарплате.

        '''

        sort_vac = sorted(self.vacanccies_list,
                          reverse=True)
        return sort_vac[:amount]

    def vac_sorted(self):
        '''
        Метод сортирует вакансии по зарплате.

        '''

        sort_vac = sorted(self.vacanccies_list,
                          reverse=True)
        self.vacanccies_list = sort_vac

    def vac_filter(self, down, up):
        '''
        Метод фильтрует вакансии по указанному диапазону зарплат.

        Параметры:
        - down: нижняя граница диапазона зарплат
        - up: верхняя граница диапазона зарплат

        '''
        filter_list = []
        for vac in self.vacanccies_list:
            if down <= vac.get_money()[1] <= up:
                filter_list.append(vac)
        return filter_list

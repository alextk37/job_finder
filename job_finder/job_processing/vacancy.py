from job_processing.converter.converter import converter as con


class Vacancy:

    def __init__(self,
                 name,
                 salary,
                 url,
                 employer,
                 snippet
                 ) -> None:
        '''
        Конструктор класса Vacancy.

        Параметры:
        - name (str): Название вакансии.
        - salary (dict): Словарь с информацией о зарплате.
        - url (str): URL вакансии.
        - employer (str): Работодатель.
        - snippet (str): Краткое описание вакансии.
        '''

        self.name = name
        self.salary = salary
        self.url = url
        self.employer = employer
        self.snippet = snippet

    def __repr__(self) -> str:
        '''
        Функция возвращает строковое представление объекта.
        '''

        return f'Вакансия {self.name}'

    def get_money(self):
        '''
        Функция возвращает диапазон зарплаты для вакансии.
        '''

        if self.salary:
            currency = self.salary.get('currency')
            if currency == 'RUR':
                if self.salary.get('from') and self.salary.get('to'):
                    from_ = self.salary.get('from')
                    to_ = self.salary.get('to')
                    return from_, to_
                elif self.salary.get('from') and self.salary.get('to') == None:
                    from_ = self.salary.get('from')
                    return from_, from_
                else:
                    to_ = self.salary.get('to')
                    return 0, to_
            else:
                if self.salary.get('from') and self.salary.get('to'):
                    from_ = self.salary.get('from')
                    to_ = self.salary.get('to')
                    return con(currency, from_), con(currency, to_)
                elif self.salary.get('from') and self.salary.get('to') == None:
                    from_ = self.salary.get('from')
                    return con(currency, from_), con(currency, from_)
                else:
                    to_ = self.salary.get('to')
                    return 0, con(currency, to_)
        else:
            return 0, 0

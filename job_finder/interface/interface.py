from rich.console import Console
from rich.table import Table


class VacTable():
    '''
    Конструктор класса VacTable.

    Параметры:
    - vacanccies: список вакансий
    '''

    def __init__(self, vacanccies) -> None:
        self.vacanccies = vacanccies

    def vac_table(self):
        '''
        Метод строит таблицу с информацией о вакансиях.
        '''

        console = Console()
        if self.vacanccies:

            table = Table(show_header=True,
                          header_style='bold red',
                          show_lines=True)
            table.add_column('Вакансия', style='cyan', width=10)
            table.add_column('Компания', width=10)
            table.add_column('Зарплата', justify='right',
                             style='green', width=10)
            table.add_column('Ссылка на вакансию', justify='right',
                             style='green')

            for vac in self.vacanccies:
                name = vac.name
                employer = vac.employer.get('name')
                money_from = vac.get_money()[0]
                money_to = vac.get_money()[1]
                money_phrase = f'от {money_from} до {money_to}'
                if money_from == 0 and money_to == 0:
                    money_phrase = 'Нет данных'
                url = vac.url

                table.add_row(name,
                              employer,
                              money_phrase,
                              url)
            console.print(table)
        else:
            console.print('! Отсутствую данные для отображения !',
                          style="bold red")

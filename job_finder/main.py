from data_processing.get_vacancies import HeadHunterParser
from data_processing.get_local import LocalData
from job_processing.vacanccies import Vacanccies
from interface.interface import VacTable
from rich.console import Console

files = LocalData()
console = Console()


def menu_vac():
    '''
    Функция выводит меню с вариантами работы с программой.

    '''

    console.print('1 - Вывести все данные из файла (осторожно TL;DR)',
                  style='green')
    console.print('2 - Вывести топ - "n" вакансий по зарплате',
                  style='green')
    console.print('3 - Сортировать вакансии по зарплате',
                  style='green')
    console.print('4 - Вывести вакансии в указанном диапазоне зарплат',
                  style='green')
    console.print('5 - Закончить работу с программой',
                  style='red')


def page_vac(num_file):
    '''
    Функция обрабатывает взаимодействие пользователя с меню программы.
    '''

    vac = Vacanccies(num_file)
    vac.vac_append()
    len_ = vac.vac_counter()
    console.print(f'[cyan]Количество вакансий в файле - {len_}[/]')
    console.print('[cyan]Конвертация в RUB по курсу /exchangerate-api.com/[/]')
    console.print(f'[cyan]{'- ' * 20}[/]')
    menu_vac()
    while True:
        answer = console.input('[cyan]-->  [/]')
        match answer:
            case '1':
                table = VacTable(vac.vac_all())
                table.vac_table()
                menu_vac()
            case '2':
                console.print('Введите количество вакансий. Нажмите Enter',
                              style='green')
                try:
                    amount = int(console.input('[cyan]-->  [/]'))
                    table = VacTable(vac.vac_top(amount))
                    table.vac_table()
                    menu_vac()
                except ValueError:
                    console.print('Количество должно быть числом',
                                  style='red')
                    menu_vac()
            case '3':
                vac.vac_sorted()
                table = VacTable(vac.vac_all())
                table.vac_table()
                menu_vac()
            case '4':
                console.print('Введите 2 числа через пробел. Нажмите Enter',
                              style='green')
                span = console.input('[cyan]-->  [/]')
                down, up = span.split(' ')
                try:
                    table = VacTable(vac.vac_filter(int(down), int(up)))
                    table.vac_table()
                    menu_vac()
                except Exception:
                    console.print('Количество должно быть числом',
                                  style='red')
                    menu_vac()
            case '5':
                console.print('Bye!:waving_hand:')
                break


def menu_files():
    '''
    Функция выводит меню с вариантами работы с программой.

    '''

    if len(files) > 0:
        console.print('1 - Загрузить новые данные',
                      style='green')
        console.print('2 - Закончить работу с программой',
                      style='red')
        console.print('3 - Удалить локальные данные',
                      style='red')
        console.print('4 - Удалить файл',
                      style='red')
        console.print('5 - Работать с файлом',
                      style='cyan')
    else:
        console.print('1 - Загрузить новые данные', style='green')
        console.print('2 - Закончить работу с программой', style='red')


def page_files():
    '''
    Функция обрабатывает взаимодействие пользователя с меню программы.
    '''

    console.print(':construction_worker: JOB_FINDER v.0.01',
                  style='bold cyan')
    console.print(f'[cyan]{'- ' * 20}[/]')
    files.get_table()
    menu_files()
    while True:
        answer = console.input('[cyan]-->  [/]')
        match answer:
            case '1':
                console.print('Введите поисковый запрос и нажмите Enter',
                              style='green')
                keywords = console.input('[cyan]-->  [/]')
                console.print('Введите количество страниц. Нажмите Enter',
                              style='green')
                try:
                    amount = int(console.input('[cyan]-->  [/]'))
                    load = HeadHunterParser(keywords, amount)
                    load.connection()
                    load.save_data()
                    files.update_ls()
                    files.get_table()
                    menu_files()
                except ValueError:
                    console.print('Количество должно быть числом',
                                  style='red')
                    menu_files()

            case '2':
                console.print('Bye!:waving_hand:')
                break

            case '3':
                files.clear_folder()
                files.update_ls()
                files.get_table()
                menu_files()
            case '4':
                console.print('Введите номер файла для удаления',
                              style='red')
                try:
                    num_file = int(console.input('[cyan]-->  [/]'))
                    files.remove_file(num_file)
                    files.update_ls()
                    files.get_table()
                    menu_files()
                except ValueError:
                    console.print('Номер файла должен быть числом',
                                  style='red')
                    files.get_table()
                    menu_files()
            case '5':
                console.print('Введите номер файла',
                              style='cyan')
                try:
                    num_file = int(console.input('[cyan]-->  [/]'))
                    if num_file > len(files):
                        console.print('Файл не найден',
                                      style='red')
                        menu_files()
                    else:
                        name = files.ls[num_file]
                        console.print(f'[cyan]{'- ' * 20}[/]')
                        console.print(f'[cyan]Работаем с файлом {name}[/]')
                        page_vac(num_file)
                        break
                except ValueError:
                    console.print('Номер файла должен быть числом',
                                  style='red')
                    files.get_table()
                    menu_files()


if __name__ == '__main__':
    page_files()

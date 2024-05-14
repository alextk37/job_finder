import os
from rich.console import Console
from rich.table import Table


class LocalData:
    '''
    Конструктор класса LocalData.
    '''

    def __init__(self) -> None:
        self.path = os.path.abspath('data_processing/save_data')
        self.ls = os.listdir(self.path)

    def __len__(self):
        '''
        Метод возвращает количество файлов в списке.
        '''

        return len(self.ls)

    def update_ls(self):
        '''
        Метод обновляет список файлов.
        '''

        self.ls = os.listdir(self.path)

    def get_table(self):
        '''
        Метод отображает таблицу с информацией о локальных данных.
        '''

        console = Console()
        if self.ls:
            table = Table(show_header=True,
                          header_style='bold red',
                          show_lines=True,
                          title="Локальные данные")
            table.add_column('№', style='cyan')
            table.add_column('Дата')
            table.add_column('Время')
            table.add_column('Поисковый запрос', justify='right',
                             style='green')

            index = 0

            for file_name in self.ls:
                file_name_list = file_name.split(' ')
                date = file_name_list[0]
                time = file_name_list[1]
                keyword = ' '.join(file_name_list[2:]).rstrip('.json')

                table.add_row(str(index),
                              date,
                              time,
                              keyword)
                index += 1
            console.print(table)
        else:
            console.print('! Отсутствую данные для отображения !',
                          style="bold red")

    def clear_folder(self):
        '''
        Метод очищает папку с данными.
        '''

        console = Console()
        console.print('Внимание это удалит все данные', style="bold red")
        warning = '[bold red]"YES" для продолжения."NO" для отмены->[/]  '
        warning_word = console.input(warning).upper()
        match warning_word:
            case 'YES':
                for file_name in self.ls:
                    file_path = os.path.join(self.path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    self.ls = os.listdir(self.path)
                console.print('* Данные удалены *', style="bold green")
            case 'NO':
                console.print('* Операция отменена *', style="bold green")

    def remove_file(self, num_file):
        '''
        Метод удаляет файл по указанному номеру.
        '''

        console = Console()
        if num_file < len(self.ls):
            file_name = self.ls[num_file]
            file_path = os.path.join(self.path, file_name)
            console.print(f'Будет удален файл [green]{file_name}[/]',
                          style="bold red")
            warning = '[bold red]"YES" для продолжения."NO" для отмены->[/]  '
            warning_word = console.input(warning).upper()
            match warning_word:
                case 'YES':
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    self.ls = os.listdir(self.path)
                    console.print('* Файл удален *', style="bold green")
                case 'NO':
                    console.print('* Операция отменена *', style="bold green")
        else:
            console.print('Нет такого файла', style="bold red")

    def get_path(self, num_file):
        '''
        Метод возвращает путь к файлу по указанному номеру.
        '''

        console = Console()
        if num_file < len(self.ls):
            file_name = self.ls[num_file]
            file_path = os.path.join(self.path, file_name)
            return file_path
        else:
            console.print('Файл не найден', style="bold red")

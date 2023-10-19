import os

from classes.DBCreator import DBCreator
from classes.DBManager import DBManager
from classes.file_manager import EmployersJSON, VacanciesJSON
from src.utils import user_interaction
from config import config


def main():

    # Получение от пользователя названия компаний для поиска и записи в файлы JSON
    user_interaction()

    # Параметры для работы с базами данных Postgres
    params = config()

    # Создание базы данных
    head_hunter_db = DBCreator('headhunter_db', params)
    head_hunter_db.create_db()

    # Получение информации из файлов JSON
    employers_in_database = EmployersJSON()
    vacancies_in_database = VacanciesJSON()
    employers = employers_in_database.read_file()
    vacancies = vacancies_in_database.read_file()

    # Запись данных из файлов JSON в таблицы БД
    head_hunter_db.save_employers_to_database(employers)
    head_hunter_db.save_vacancies_to_database(vacancies)

    # Словарь с вариантами запроса
    query_menu = {
        0: "0 - Выхода из программы",
        1: "1 - Список всех компаний и количество вакансий у каждой компании",
        2: "2 - Список всех вакансий с указанием имени компании, названия вакансии, зарплаты и ссылки на вакансию",
        3: "3 - Cредняя зарплата по вакансиям",
        4: "4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям",
        5: "5 - Список всех вакансий, по наличию введенного слова"
    }

    # Функции для ответа на запросы пользователя
    db_response = DBManager("headhunter_db", params)
    func_1 = db_response.get_companies_and_vacancies_count()
    func_2 = db_response.get_all_vacancies()
    func_3 = db_response.get_avg_salary()
    func_4 = db_response.get_vacancies_with_higher_salary()
    func_5 = db_response

    # Словарь с функциями
    func_dict = {
        1: func_1, 2: func_2, 3: func_3, 4: func_4, 5: func_5
    }

    # Счетчик неверных запросов
    count_error = 3

    while True:

        print('\nВыберите вариант запроса\n')
        for query in range(0, len(query_menu)):
            print(f'{query_menu.get(query)}')

        user_number = int(input("Ваш выбор: "))

        if user_number in range(1, 5):
            print(f'\nВы ввели {query_menu.get(user_number)}')
            print(f'\n{func_dict.get(user_number)}')
        elif user_number == 5:
            user_words = input(f'\nВы ввели {query_menu.get(user_number)}\nВведите ключевые слова: ')
            print(f'\n{func_dict.get(user_number).get_vacancies_with_keyword(user_words)}')
        elif user_number == 0:
            print(f'\nВы ввели {query_menu.get(user_number)}\nДо встречи!!!')
            break
        elif count_error != 0:
            count_error -= 1
            print(f'Неверный запрос, при 3х неверных запросах программа завершится\n'
                  f'Осталось неверных запросов: {count_error}\n')
        else:
            print('Вы израсходовали максимум неверных запросов(((')
            break

    os.remove('employers.json')
    os.remove('vacancies.json')


if __name__ == '__main__':
    main()

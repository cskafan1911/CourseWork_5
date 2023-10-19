import os

from classes.DBManager import DBManager
from classes.file_manager import EmployersJSON, VacanciesJSON
from classes.head_hunter_API import HeadHunterAPI


def user_interaction_one():
    """
    Функция запрашивает у пользователя название компаний и сохраняет их в файлы JSON
    """
    print('Привет! Это программа выдает информацию о 10-ти интересующих работодателях и их открытых вакансиях')

    for num in range(1, 11):
        user_input = input(f"Введите название компании № {num}:\n")

        # Экземпляр класса HeadHunterAPI
        employer = HeadHunterAPI(user_input)
        # Информация о работодателе полученная по API
        employer_data = employer.get_employer_data()

        # Информация о вакансиях работодателя полученная по API при помощи id работодателя
        vacancies_data = employer.get_vacancies_data(employer_data.get('id'))

        # Экземпляр класса EmployersJSON
        employers_file = EmployersJSON()
        employers_file.save_file(employer_data)

        # Экземпляр класса VacanciesJSON
        vacancies_file = VacanciesJSON()
        vacancies_file.save_file(vacancies_data)


def user_interaction_two(params):
    """
    Функция показывает какую информацию из базы данных можно получить и ждет запроса пользователя
    """
    # Словарь с вариантами запроса
    query_menu = {
        '0': "0 - Выход из программы",
        '1': "1 - Список всех компаний и количество вакансий у каждой компании",
        '2': "2 - Список всех вакансий с указанием имени компании, названия вакансии, зарплаты и ссылки на вакансию",
        '3': "3 - Cредняя зарплата по вакансиям",
        '4': "4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям",
        '5': "5 - Список всех вакансий, по наличию введенного слова"
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
    count_error = 2

    while True:

        print('\nВыберите вариант запроса\n')
        for query in range(0, len(query_menu)):
            print(f'{query_menu.get(str(query))}')

        user_number = input("Ваш выбор: ")

        try:
            if int(user_number) in range(1, 5):
                print(f'\nВы ввели {query_menu.get(user_number)}')
                print(f'\n{func_dict.get(int(user_number))}')
            elif int(user_number) == 5:
                user_words = input(f'\nВы ввели {query_menu.get(user_number)}\nВведите ключевое слово: ')
                print(f'\n{func_dict.get(int(user_number)).get_vacancies_with_keyword(user_words)}')
            elif int(user_number) == 0:
                print(f'\nВы ввели {query_menu.get(user_number)}\nДо встречи!!!')
                break
            elif count_error != 0:
                print(f'\nНеверный запрос, при 3х неверных запросах программа завершится\n'
                      f'Осталось неверных запросов: {count_error}')
                count_error -= 1
            elif count_error == 0:
                print('\nВы израсходовали максимум неверных запросов(((\n'
                      'Программа прекращает работу\n'
                      'До встречи!!!')
                break
        except ValueError:
            print(f'\nНеверный запрос, при 3х неверных запросах программа завершится\n'
                  f'Осталось неверных запросов: {count_error}')
            if count_error == 0:
                print('\nВы израсходовали максимум неверных запросов(((\n'
                      'Программа прекращает работу\n'
                      'До встречи!!!')
                break
            count_error -= 1

    os.remove('employers.json')
    os.remove('vacancies.json')

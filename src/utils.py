from classes.file_manager import EmployersJSON, VacanciesJSON
from classes.head_hunter_API import HeadHunterAPI


def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    print('Привет! Это программа выдает информацию о 10-ти интересующих работодателях и их открытых вакансиях')

    for num in range(1, 4):
        user_input = input(f"Введите название компании № {num}:\n")
        employer = HeadHunterAPI(user_input)
        employer_data = employer.get_employer_data()
        vacancies_data = employer.get_vacancies_data(employer_data['id'])
        employers_file = EmployersJSON()
        employers_file.save_file(employer_data)
        vacancies_file = VacanciesJSON()
        vacancies_file.save_file(vacancies_data)


user_interaction()

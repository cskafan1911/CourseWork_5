from classes.file_manager import EmployersJSON, VacanciesJSON
from classes.head_hunter_API import HeadHunterAPI


def user_interaction():
    """
    Функция запрашивает у пользователя название компаний и сохраняет их в файлы JSON
    """
    print('Привет! Это программа выдает информацию о 10-ти интересующих работодателях и их открытых вакансиях')

    for num in range(1, 3):
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

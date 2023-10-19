from classes.DBCreator import DBCreator
from classes.file_manager import EmployersJSON, VacanciesJSON
from src.utils import user_interaction_one, user_interaction_two
from config import config


def main():

    # Получение от пользователя названия компаний для поиска и записи в файлы JSON
    user_interaction_one()

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

    user_interaction_two(params)


if __name__ == '__main__':
    main()

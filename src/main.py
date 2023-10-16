from classes.DBCreator import DBCreator
from classes.file_manager import EmployersJSON, VacanciesJSON
from src.utils import user_interaction
from config import config


def main():

    user_interaction()
    params = config()
    head_hunter_db = DBCreator('headhunter_db', params)
    head_hunter_db.create_db()
    employers_in_database = EmployersJSON()
    vacancies_in_database = VacanciesJSON()
    employers_in_database.read_file()
    vacancies_in_database.read_file()


if __name__ == '__main__':
    main()

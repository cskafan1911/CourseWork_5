from typing import Any

import psycopg2

from classes.DBCreator import DBCreator


class DBManager(DBCreator):
    """
    Класс для работы с базами данных Postgres
    """

    def get_companies_and_vacancies_count(self) -> list[tuple[Any]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """

        return self.__get_data_from_database('SELECT employer_name, open_vacancies FROM employers ORDER BY open_vacancies DESC')

    def get_all_vacancies(self) -> list[tuple[Any]]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты (от и до)
        и ссылки на вакансию
        """

        return self.__get_data_from_database('SELECT employer_name, vacancy_name, salary_from, salary_to, url_vacancy FROM vacancies')

    def get_avg_salary(self) -> list[tuple[Any]]:
        """
        Получает среднюю зарплату по вакансиям
        """

        return self.__get_data_from_database('SELECT ROUND ((AVG (salary_from) + AVG(salary_to)) / 2) AS AVG_salary FROM vacancies')

    def get_vacancies_with_higher_salary(self) -> list[Any]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        result = self.__get_data_from_database('SELECT * FROM vacancies WHERE (salary_to + salary_from) / 2 > '
                                '(SELECT ROUND ((AVG (salary_from) + AVG(salary_to)) / 2) FROM vacancies)')

        return result

    def get_vacancies_with_keyword(self, word) -> list[tuple[Any]] | str:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :param word: слово для поиска вакансий
        :return: данные из базы postgres
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM vacancies"
                f" WHERE vacancy_name LIKE '%{word}%'"
            )
            rows = cur.fetchall()

        if len(rows) == 0:
            return f'В названии вакансий из базы данных нет слова {word}'

        return rows

    def __get_data_from_database(self, queries) -> list[Any]:
        """
        Метод делает запрос и получает данные из базы
        :param queries: SQL запрос
        :return: данные из базы postgres
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(queries)
            rows = cur.fetchall()

        return rows

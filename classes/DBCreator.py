from typing import Any

import psycopg2


class DBCreator:
    """
    Класс для создания базы данных
    """

    def __init__(self, database_name: str, params: dict[str: Any]) -> None:
        """
        Инициализация класса DBCreator
        :param database_name: название базы данных
        :param params: параметры для создания базы данных
        """
        self.database_name = database_name
        self.params = params

    def create_db(self) -> None:
        """
        Метод создает базу данных
        """
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {self.database_name}')
        cur.execute(f'CREATE DATABASE {self.database_name}')

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY NOT NULL,
                    employer_name VARCHAR(255) NOT NULL,
                    open_vacancies INTEGER,
                    url_employer VARCHAR(255)
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancies_id INTEGER PRIMARY KEY,
                    vacancy_name VARCHAR NOT NULL,
                    employer_id INT REFERENCES employers(employer_id),
                    employer_name VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    experience VARCHAR(50),
                    requirement TEXT,
                    url_vacancy TEXT
                )
            """)

        conn.commit()
        conn.close()

    def save_employers_to_database(self, data_employers: list[dict[str, Any]]) -> None:
        """
        Сохраняет данные о работодателях и их вакансиях в базу данных
        :param data_employers: данные о работодателях
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            for employer in data_employers:
                if employer.get('id') is None:
                    continue
                else:
                    cur.execute("""
                    INSERT INTO employers (employer_id, employer_name, open_vacancies, url_employer)
                    VALUES (%s, %s, %s, %s)
                    RETURNING employer_id
                    """,
                                (employer.get('id'), employer.get('name'), employer.get('open_vacancies'), employer.get('url'))
                                )

        conn.commit()
        conn.close()

    def save_vacancies_to_database(self, data_vacancies: list[dict[str, Any]]) -> None:
        """
        Сохраняет данные о работодателях и их вакансиях в базу данных
        :param data_vacancies: данные о вакансиях работодателей
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            for vacancy in data_vacancies:
                if vacancy.get('salary') is None:
                    vacancy['salary'] = {'from': None, 'to': None}
                cur.execute("""
                INSERT INTO vacancies (vacancies_id, vacancy_name, employer_id, employer_name, salary_from, 
                salary_to, experience, requirement, url_vacancy)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                            (vacancy.get('id'), vacancy.get('name'), vacancy.get('employer').get('id'),
                             vacancy.get('employer').get('name'),
                             vacancy.get('salary').get('from'), vacancy.get('salary', {}).get('to'),
                             vacancy.get('experience').get('name'),
                             vacancy.get('snippet').get('requirement'), vacancy.get('url'))
                            )

        conn.commit()
        conn.close()

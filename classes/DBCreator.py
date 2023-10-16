import psycopg2


class DBCreator:
    """
    Класс для создания базы данных
    """

    def __init__(self, database_name: str, params: dict) -> None:
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
                    salary_avg INTEGER,
                    experience VARCHAR(50),
                    requirement TEXT,
                    url_vacancy TEXT
                )
            """)

        conn.commit()
        conn.close()

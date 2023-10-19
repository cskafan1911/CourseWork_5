from typing import Any

import requests
from settings import URL_HH_API_EMPLOYERS, URL_HH_API_VACANCIES


class HeadHunterAPI:
    """
    Класс для поиска информации о работодателе и его открытых вакансиях
    """

    def __init__(self, employer_name: str):
        """
        Инициализация класса HeadHunterAPI
        :param employer_name: название компании
        """
        self.employer_name = employer_name

    def get_employer_data(self) -> dict[str: Any]:
        """
        Метод для получения информации о работодателе
        :return: Словарь с информацией о работодателе в городе Москва
        """
        try:
            params = {
                'text': f"{self.employer_name}",
                'area': 1,
                'only_with_vacancies': True,
                'pages': 1,
                'per_page': 100
            }
            req = requests.get(URL_HH_API_EMPLOYERS, params)
            req.content.decode()
            req.close()

            employer_data = req.json()['items'][0]

            return employer_data

        except IndexError:

            return {}

    def get_vacancies_data(self, employer_id: int) -> list[dict[str: Any]]:
        """
        Метод для получения вакансий работодателя
        :param employer_id: id работодателя
        :return: Список вакансий работодателя
        """
        try:

            params = {
                'employer_id': f"{employer_id}",
                'per_page': 100
            }
            req = requests.get(URL_HH_API_VACANCIES, params)
            req.content.decode()
            req.close()

            vacancy_data = req.json()['items']

            return vacancy_data

        except KeyError:

            return []

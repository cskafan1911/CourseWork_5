from typing import Any

import requests
from config import URL_HH_API_EMPLOYERS, URL_HH_API_VACANCIES


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

    def get_employer_data(self) -> dict:
        """
        Метод для получения информации о работодателе
        :return: Словарь с информацией о работодателе в городе Москва
        """
        params = {
            'text': f"{self.employer_name}",
            'area': 1,
            'only_with_vacancies': True,
            'pages': 1,
            'per_page': 10
        }
        req = requests.get(URL_HH_API_EMPLOYERS, params)
        req.content.decode()
        req.close()

        employer_data = req.json()['items'][0]

        return employer_data

    def get_vacancies_data(self, employer_id: int) -> list[dict]:
        """
        Метод для получения вакансий работодателя
        :param employer_id: id работодателя
        :return: Список вакансий работодателя
        """
        params = {
            'employer_id': f"{employer_id}",
            'per_page': 10
        }
        req = requests.get(URL_HH_API_VACANCIES, params)
        req.content.decode()
        req.close()

        vacancy_data = req.json()['items']

        return vacancy_data

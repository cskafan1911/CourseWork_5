import ast
import json
import os
from abc import ABC, abstractmethod
from typing import Any

from settings import FILENAME_EMPLOYER, FILENAME_VACANCIES


class JSONManager(ABC):
    """
    Абстрактный класс для работы с файлами JSON
    """

    @abstractmethod
    def save_file(self, data):
        """
        Метод сохраняет данные в файл формата JSON
        :param data: Данные для сохранения
        """
        pass

    @abstractmethod
    def read_file(self):
        """
        Метод для чтения файла
        """
        pass


class EmployersJSON(JSONManager):
    """
    Класс для работы с файлами работодателя формата json
    """

    def __init__(self):
        """
        Инициализатор для класса EmployersJSON
        """
        self.__filename = FILENAME_EMPLOYER + ".json"

    def save_file(self, data: dict[str: Any]) -> None:
        """
        Метод сохраняет информацию о работодателе в файл формата JSON
        """

        if os.path.exists(self.__filename):
            with open(self.__filename, 'r', encoding='utf-8') as file:
                employer_data = json.load(file)
            if not any(employer.get('id') == data.get('id') for employer in employer_data):
                employer_data.append(data)
                with open(self.__filename, 'w', encoding='utf-8') as file:
                    json.dump(employer_data, file, ensure_ascii=False, indent=2)

        else:
            employer_data = [data]

            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(employer_data, file, ensure_ascii=False, indent=2)

    def read_file(self) -> list[dict[str: Any]]:
        """
        Метод для чтения файла
        """
        with open(self.__filename, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        return json_data


class VacanciesJSON(JSONManager):
    """
    Класс для работы с файлами вакансий работодателя формата json
    """

    def __init__(self):
        """
        Инициализатор для класса VacanciesJSON
        """
        self.__filename = FILENAME_VACANCIES + ".json"

    def save_file(self, data: list[dict[str: Any]]) -> None:
        """
        Метод сохраняет список вакансий в файл формата JSON
        """

        if os.path.exists(self.__filename):
            with open(self.__filename, 'r', encoding='utf-8') as file:
                vacancy_data = json.load(file)
            for new_vacancy in data:
                if not any(vacancy.get('id') == new_vacancy.get('id') for vacancy in vacancy_data):
                    vacancy_data.append(new_vacancy)
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(vacancy_data, file, ensure_ascii=False, indent=2)
        else:
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

    def read_file(self) -> list[dict[str: Any]]:
        """
        Метод для чтения файла
        """
        with open(self.__filename, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        return json_data

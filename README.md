# CourseWork_5
Описание программы
-------------------------
Программа для парсинга данных о работодателях и их вакансиях с API HeadHunter и последующей работе через базу 
данных PostgreSQL. Пользователь вводит 10 интересующих 
его компаний, программа парсит Api HeadHunter и сохраняет данные в файлы(employers - для компаний, vacancies - для вакансий)
формата json. Далее создается база данных headhunter_db в PostgreSQL и переносятся данные из файлов json в таблицы employers и vacancies.
После программа выводит на экран возможные варианты запроса. Пользователь может выводить интересующие его запросы до того момента пока 
не завершит программу самостоятельно или пока не сделает 3 неверных запроса. После этого программа удаляет файлы json и завершает свою работу.

Для запуска программы
---------------------------
Программа работает с PostgreSQL. Для подключения к базе данных PostgreSQL необходимо создать файл database.ini в директории src и прописать в нем 
(в строке password='ваш пароль от PostgresSQL'):

[postgresql]
host=localhost
user=postgres
password=
port=5432


Для работы с виртуальным окружением нужно использовать poetry (для установки пропишите pip install poetry в терминале pycharm). 
Для установки зависимостей нужно прописать в терминале pycharm -> poetry install.

Для запуска программы можно прописать в терминале python main.py или открыть файл main.py и 
запустить функцию main()

import requests
import json
import csv
import psycopg2


def hh_get_vacancies(vacancy_name):
    """Запрос к API HH"""

    params = {
        'text': vacancy_name,
        'area': 1,
        'page': 0,
        'per_page': 50
    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    js_obj = json.loads(data)
    vacancy_data = vacancies_pars(js_obj)
    return vacancy_data


def vacancies_pars(js_obj):
    """Парсинг полученных вакансий"""

    all_vacancy = []
    for obj in js_obj['items']:
        salary = obj.get('salary') or {}
        salary_from = salary.get('from')
        salary_to = salary.get('to')
        if salary_from is not None:
            salary_from = int(salary_from)
        if salary_to is not None:
            salary_to = int(salary_to)
        all_vacancy.append({
            'id': obj['id'],
            'vacancy_name': obj['name'],
            'salary_from': salary_from or 0,
            'salary_to': salary_to or 0,
            'company_name': obj['employer']['name'],
            'url': obj['url'],
            'requirements': obj['snippet']['requirement']
        })

    return all_vacancy


def csv_writer(user_input):
    """Сохранение данных в формате csv"""

    cols = ['id', 'vacancy_name', 'salary_from', 'salary_to', 'company_name', 'url', 'requirements']

    with open('vacancies.csv', 'w', newline='', encoding='utf-8') as file:
        wr = csv.DictWriter(file, fieldnames=cols)
        wr.writeheader()
        wr.writerows(hh_get_vacancies(user_input))


# Соединение с базой данных

connection = psycopg2.connect(host="localhost",
                              database="Course_5_database",
                              user="postgres",
                              password="324214Kross!"
                              )


def create_table():
    """Создание таблицы в БД"""

    with connection as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies(
                        id INT PRIMARY KEY,
                        vacancy_name TEXT,
                        salary_from INT,
                        salary_to INT,
                        company_name TEXT,
                        url TEXT,
                        requirements TEXT

                    );
                """)


def table_add_data():
    """Добавление данных в таблицу"""

    with connection as conn:
        with conn.cursor() as cursor:
            with open('vacancies.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    cursor.execute(
                        "INSERT INTO vacancies (id,"
                        "vacancy_name, "
                        "salary_from, "
                        "salary_to, "
                        "company_name, "
                        "url, "
                        "requirements)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        row
                    )


def clear_table():
    """Очистка таблицы"""

    with connection as conn:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE vacancies")


if __name__ == '__main__':
    # user_input = input('Введите название вакансии: \n')
    # csv_writer(user_input)
    # create_table()
    # clear_table()
    # table_add_data()
    # connection.close()
    pass

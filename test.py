import requests
import json
import csv
import psycopg2
from sqlalchemy import create_engine


# def hh_get_employers():
#     """Запрос к API HH"""
#
#     params = {
#         'text': 'IT',
#         'area': 1,
#         'page': 0,
#         'per_page': 50
#     }
#     req = requests.get('https://api.hh.ru/employers', params)
#     data = req.content.decode()
#     req.close()
#     js_obj = json.loads(data)
#     vacancy_data = employers_pars(js_obj)
#     return vacancy_data
#     # return js_obj
#
#
# def employers_pars(js_obj):
#     """Парсинг полученных вакансий"""
#
#     all_emp = []
#     for obj in js_obj['items']:
#         all_emp.append({
#             'id': obj['id'],
#             'Работодатель': obj['name'],
#             'Ссылка': obj['url'],
#             'Количество открытых вакансий': obj['open_vacancies'],
#             'Ссылка на вакансии': obj['vacancies_url'],
#         })
#
#     return all_emp


def get_vacancies():
    """Запрос к API HH"""

    params = {
        'text': 'QA',
        'area': 1,
        'page': 0,
        'per_page': 50
    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    js_obj = json.loads(data)
    return vacancies_pars(js_obj)


def vacancies_pars(js_obj):
    """Парсинг полученных вакансий"""

    all_vacancy = []
    for obj in js_obj['items']:
        salary = obj.get('salary')
        if obj['salary']['from'] != 0:
            all_vacancy.append({
                'id': obj['id'],
                'vacancy_name': obj['name'],
                'salary_from': obj['salary']['from'],
                'salary_to': obj['salary']['to'],
                'company_name': obj['employer']['name'],
                'url': obj['url'],
                'requirements': obj['snippet']['requirement']
            })

    return all_vacancy


if __name__ == '__main__':
    print(get_vacancies())

from utils import table_add_data, create_table, csv_writer, clear_table, connection
from DB_Manager import DBManager


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    print('Добрый день!\n')
    create_db = input('\nВведите название вакансии для формирования Базы Данных:  \n')
    csv_writer(create_db)
    create_table()
    clear_table()
    table_add_data()

    # print('Введите "1", чтобы получить список всех вакансий по запросу,\n'
    #       'Введите "2", чтобы получить среднюю зарплату по данным вакансиям,\n'
    #       'Введите "3", чтобы получить список всех вакансий,у которых зарплата выше средней,\n'
    #       'Введите "4", чтобы получить количество открытых вакансий компании\n')

    client = DBManager('Course_5_database')

    enter_1 = input('Нажмите "Enter", чтобы получить список всех вакансий по запросу\n')
    get_vacancies = client.get_all_vacancies()
    print(get_vacancies)

    enter_2 = input('Нажмите "Enter", чтобы получить среднюю зарплату по данным вакансиям\n')
    avg_salary = client.get_avg_salary()
    print(avg_salary)

    enter_3 = input('Нажмите "Enter", чтобы получить список всех вакансий,у которых зарплата выше средней\n')
    higher_salary = client.get_vacancies_with_higher_salary()
    print(higher_salary)

    enter_4 = input('Нажмите "Enter", чтобы получить количество открытых вакансий компании\n')
    get_info = client.get_companies_and_vacancies_count()
    print(get_info)

    keyword = input('\nВведите ключевое слово для получения информации по конкретной вакансии: \n')
    vac_with_keyword = client.get_vacancies_with_keyword(keyword)
    print(vac_with_keyword)

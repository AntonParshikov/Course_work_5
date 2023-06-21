import psycopg2


class DBManager:
    def __init__(self, dbname):
        self.dbname = dbname
        self.user = 'postgres'
        self.password = '324214Kross!'
        self.host = 'localhost'

    def connect(self):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )
        return conn

    def get_companies_and_vacancies_count(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT company_name, COUNT(*) as vacancies_count
            FROM vacancies
            GROUP BY company_name
            ORDER BY vacancies_count DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_all_vacancies(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            ORDER BY salary_from DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_avg_salary(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT AVG(salary_from)
            FROM vacancies
        """)
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            WHERE salary_from > {avg_salary}
            ORDER BY salary_from DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            WHERE vacancy_name LIKE '%{keyword}%'
            ORDER BY salary_from DESC
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result


if __name__ == '__main__':
    client = DBManager('Course_5_database')
    # vac = client.get_vacancies_with_keyword('QA')
    # avg_salary = client.get_avg_salary()
    # all_vacancies = client.get_all_vacancies()
    # higher_salary = client.get_vacancies_with_higher_salary()
    pass


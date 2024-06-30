import psycopg2
from db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class DBManager:
    def __init__(self):
        """
        Initialize the database connection.
        """
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Get the count of vacancies for each company.

        :return: List of companies and their vacancies count
        """
        self.cur.execute("""
            SELECT e.name, COUNT(v.vacancy_id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """
        Get all vacancies.

        :return: List of all vacancies
        """
        self.cur.execute("""
            SELECT e.name, v.name, v.salary, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """
        Get the average salary of all vacancies.

        :return: Average salary
        """
        self.cur.execute("""
            SELECT AVG(v.salary)
            FROM vacancies v
            WHERE v.salary IS NOT NULL
        """)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Get vacancies with a salary higher than the average salary.

        :return: List of vacancies with higher salary
        """
        avg_salary = self.get_avg_salary()
        self.cur.execute("""
            SELECT e.name, v.name, v.salary, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.salary > %s
        """, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Get vacancies that contain the keyword in their name.

        :param keyword: Keyword to search for
        :return: List of vacancies with the keyword
        """
        self.cur.execute("""
            SELECT e.name, v.name, v.salary, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.name ILIKE %s
        """, (f'%{keyword}%',))
        return self.cur.fetchall()

    def close(self):
        """
        Close the database connection.
        """
        self.cur.close()
        self.conn.close()
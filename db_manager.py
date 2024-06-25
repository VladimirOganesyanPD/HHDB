import psycopg2


class DBManager:
    def __init__(self, dbname, user, password):
        self.conn = psycopg2.connect(database=dbname, user=user, password=password)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("""
            SELECT e.name, COUNT(v.vacancy_id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute("""
            SELECT e.name, v.name, v.salary, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("""
            SELECT AVG(v.salary)
            FROM vacancies v
            WHERE v.salary IS NOT NULL
        """)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("""
            SELECT e.name, v.name, v.salary, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.salary > %s
        """, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute("""
            SELECT e.name, v.name, v.salary, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.name ILIKE %s
        """, (f'%{keyword}%',))
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    db_manager = DBManager("hhdb", "postgres", "290102gg228")
    print("Companies and vacancies count:", db_manager.get_companies_and_vacancies_count())
    print("All vacancies:", db_manager.get_all_vacancies())
    print("Average salary:", db_manager.get_avg_salary())
    print("Vacancies with higher salary:", db_manager.get_vacancies_with_higher_salary())
    print("Vacancies with keyword 'python':", db_manager.get_vacancies_with_keyword("python"))
    db_manager.close()
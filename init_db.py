import psycopg2
from fetch_data import get_employer_data, get_vacancies


def create_tables():
    commands = (
        """
        CREATE TABLE employers (
            employer_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary INTEGER,
            url VARCHAR(255) NOT NULL,
            employer_id INTEGER NOT NULL,
            FOREIGN KEY (employer_id)
            REFERENCES employers (employer_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )

    conn = None
    try:
        conn = psycopg2.connect(database="hhdb", user="postgres", password="290102gg228")
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_data(employers, vacancies):
    conn = None
    try:
        conn = psycopg2.connect(database="hhdb", user="postgres", password="290102gg228")
        cur = conn.cursor()

        for employer in employers:
            cur.execute(
                "INSERT INTO employers (name, url) VALUES (%s, %s) RETURNING employer_id",
                (employer['name'], employer['alternate_url'])
            )
            employer_id = cur.fetchone()[0]
            for vacancy in vacancies:
                if vacancy['employer']['id'] == employer['id']:
                    cur.execute(
                        "INSERT INTO vacancies (name, salary, url, employer_id) VALUES (%s, %s, %s, %s)",
                        (vacancy['name'], vacancy['salary']['from'] if vacancy['salary'] else None, vacancy['alternate_url'], employer_id)
                    )

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_tables()
    employers = get_employer_data(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    vacancies = get_vacancies(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    insert_data(employers, vacancies)
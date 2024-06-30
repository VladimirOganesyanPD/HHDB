from db_manager import DBManager
from init_db import initialize_database


def main():
    """
    Main function to interact with the user and perform database operations.
    """
    initialize_database()

    db_manager = DBManager()

    while True:
        print("\nВыберите действие:")
        print("1. Получить количество вакансий у каждой компании")
        print("2. Получить все вакансии")
        print("3. Получить среднюю зарплату по вакансиям")
        print("4. Получить вакансии с зарплатой выше средней")
        print("5. Найти вакансии по ключевому слову")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
            for company in companies_and_vacancies:
                print(f"Компания: {company[0]}, Количество вакансий: {company[1]}")
        elif choice == '2':
            all_vacancies = db_manager.get_all_vacancies()
            for vacancy in all_vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, URL: {vacancy[3]}")
        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")
        elif choice == '4':
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            for vacancy in higher_salary_vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, URL: {vacancy[3]}")
        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in keyword_vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, URL: {vacancy[3]}")
        elif choice == '6':
            print("Выход из программы.")
            db_manager.close()
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 6.")


if __name__ == "__main__":
    main()
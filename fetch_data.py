import requests

HH_API_URL = "https://api.hh.ru"


def get_employer_data(employer_ids):
    employers = []
    for employer_id in employer_ids:
        response = requests.get(f"{HH_API_URL}/employers/{employer_id}")
        if response.status_code == 200:
            employers.append(response.json())
    return employers


def get_vacancies(employer_ids):
    vacancies = []
    for employer_id in employer_ids:
        response = requests.get(f"{HH_API_URL}/vacancies", params={"employer_id": employer_id})
        if response.status_code == 200:
            vacancies.extend(response.json().get('items', []))
    return vacancies


if __name__ == "__main__":
    employer_ids = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]  # IDs of companies
    employers = get_employer_data(employer_ids)
    vacancies = get_vacancies(employer_ids)
    print("Employers:", employers)
    print("Vacancies:", vacancies)
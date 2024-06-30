import requests

HH_API_URL = "https://api.hh.ru"

def get_employer_data(employer_ids):
    """
    Get employer data from the API.

    :param employer_ids: List of employer IDs
    :return: List of employers
    """
    employers = []
    for employer_id in employer_ids:
        response = requests.get(f"{HH_API_URL}/employers/{employer_id}")
        if response.status_code == 200:
            employers.append(response.json())
    return employers

def get_vacancies(employer_ids):
    """
    Get vacancies data from the API.

    :param employer_ids: List of employer IDs
    :return: List of vacancies
    """
    vacancies = []
    for employer_id in employer_ids:
        response = requests.get(f"{HH_API_URL}/vacancies", params={"employer_id": employer_id})
        if response.status_code == 200:
            vacancies.extend(response.json().get('items', []))
    return vacancies
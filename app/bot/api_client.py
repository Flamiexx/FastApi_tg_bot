# api_client.py
import requests

BASE_URL = "http://127.0.0.1:8000"


def create_expense(data):
    return requests.post(f"{BASE_URL}/expenses/", json=data)


def update_expense(expense_id, data):
    return requests.put(f"{BASE_URL}/expenses/{expense_id}", json=data)


def get_expenses(start_date=None, end_date=None):
    if start_date and end_date:
        return requests.get(f"{BASE_URL}/expenses/?start_date={start_date}&end_date={end_date}")
    return requests.get(f"{BASE_URL}/expenses/")


def delete_expense(expense_id):
    return requests.delete(f"{BASE_URL}/expenses/{expense_id}")

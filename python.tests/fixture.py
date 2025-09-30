import pytest
import requests

base_url = "http://127.0.0.1:5000/api/tasks" 

def fixture_api_task():
    payload = {"title": "API Test Task", "description": "Created via automation", "status": "pending"} 
    response = requests.post(f"{base_url}", json=payload)
    return response.json()["id"]

def test_create_task():
    payload = {"title": "API Test Task", "description": "Created via automation", "status": "pending"}
    response = requests.post(f"{base_url}", json=payload)

    assert response.status_code == 201
    assert response.json()["title"] == "API Test Task"

    if __name__ == "__main__":
        test_create_task()
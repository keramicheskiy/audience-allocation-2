import requests

from settings import BACKEND_URL, ADMIN_EMAIL, ADMIN_PASSWORD
import pytest
from wait_for_backend import wait_for_backend


@pytest.fixture(scope="session", autouse=True)
def wait_for_service():
    wait_for_backend()


def test_connection():
    response = requests.get(BACKEND_URL + "/health")
    assert response.status_code == 200


@pytest.fixture
def teacher_token():
    user_data = {
        "first_name": "Игнат",
        "patronymic": "Петрович",
        "last_name": "Шарков",
        "email": "i.p.sharkov@mail.ru",
        "password": "Ogurec228!",
        "role": "teacher"
    }
    register_resp = requests.post(f"{BACKEND_URL}/auth/register", json=user_data)

    if register_resp.status_code == 201:
        print("[INFO] Пользователь зарегистрирован")
    elif register_resp.status_code == 400 and "уже существует" in register_resp.text:
        print("[INFO] Пользователь уже существует, переход к логину")
    else:
        register_resp.raise_for_status()

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    login_resp = requests.post(f"{BACKEND_URL}/auth/login", json=login_data)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json().get("token")
    assert token, "Token was not provided"
    return token


@pytest.fixture
def admin_token():
    user_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
    }
    response = requests.post(f"{BACKEND_URL}/auth/login", json=user_data)
    assert response.status_code == 200
    token = response.json()["token"]
    assert token, "Token was not provided"
    return token


def test_create_equipment(admin_token):
    response = requests.post(
        f"{BACKEND_URL}/equipments/",
        json={"name": "Нет"},
        headers={"Content-Type": "application/json"},
        cookies={"Token": admin_token}
    )
    assert response.status_code == 201


def test_create_auditorium(admin_token):
    response = requests.get(f"{BACKEND_URL}/equipments", cookies={"Token": admin_token})
    assert response.status_code == 200
    assert len(response.json())
    equipment_id = response.json()[0]["id"]
    data = {
        "number": "221B",
        "size": 300,
        "equipment": equipment_id,
        "location": "ГУК В",
        "description": "..."
    }
    response = requests.post(
        f"{BACKEND_URL}/auditoriums/new",
        headers={"Content-Type": "application/json"},
        json=data,
        cookies={"Token": admin_token}
    )
    assert response.status_code == 201


def test_allow_teacher_auditorium(admin_token, teacher_token):
    response = requests.get(f"{BACKEND_URL}/auth/verify-token", cookies={"Token": teacher_token})
    assert response.status_code == 200
    teacher = response.json()
    response = requests.get(f"{BACKEND_URL}/auditoriums", cookies={"Token": admin_token})
    assert response.status_code == 200
    auditoriums = response.json()
    assert len(auditoriums)
    response = requests.post(
        f"{BACKEND_URL}/users/{teacher.id}/auditoriums",
        headers={"Content-Type": "application/json"},
        cookies={"Token": teacher_token},
        json={"auditorium_id": int(auditoriums[0]["id"])}
    )
    assert response.status_code == 201

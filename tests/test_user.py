from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]
def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'unknown@example.com'})
    assert response.status_code == 404


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Anna Sidorova',
        'email': 'a.sidorova@example.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    # Проверим, что возвращается ID (целое число)
    user_id = response.json()
    assert isinstance(user_id, int) and user_id > 0


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate_user = {
        'name': 'Another Ivan',
        'email': users[0]['email']  # уже существует
    }
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409


def test_delete_user():
    '''Удаление пользователя'''
    email_to_delete = users[1]['email']  # 'p.p.petrov@mail.com'

    # Убедимся, что пользователь существует до удаления
    get_before = client.get("/api/v1/user", params={'email': email_to_delete})
    assert get_before.status_code == 200

    # Удаляем
    delete_response = client.delete("/api/v1/user", params={'email': email_to_delete})
    assert delete_response.status_code == 204

    # Проверяем, что пользователь больше не существует
    get_after = client.get("/api/v1/user", params={'email': email_to_delete})
    assert get_after.status_code == 404

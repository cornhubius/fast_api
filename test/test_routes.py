from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['Hello world!']


def test_create_user(temp_db):
    request_data = {
        "username": "stringstring",
        "email": "stringstring@example.com",
        "password": "stringstring",
        "confirm_password": "stringstring"
    }
    request_data_1 = {
        "username": "stringstring1",
        "email": "stringstring1@example.com",
        "password": "stringstring1",
        "confirm_password": "stringstring1"
    }
    with TestClient(app) as client:
        response = client.post("/user/", json=request_data)
        response_1 = client.post("/user/", json=request_data_1)
    assert response.status_code == 200
    assert response.json()["id"] == "1"
    assert response.json()["email"] == "stringstring@example.com"
    assert response.json()["username"] == "stringstring"
    assert response.json()["register_date"] is not None


def test_bad_password(temp_db):
    request_data_bad_password = {
        "username": "stringstring1",
        "email": "stringstring1@example.com",
        "password": "strin",
        "confirm_password": "strin"
    }
    response = client.post("/user/", json=request_data_bad_password)
    assert response.json()[
        'detail'][0]['msg'] == 'ensure this value has at least 8 characters'


def test_ununique_email(temp_db):
    request_data = {
        "username": "stringstring",
        "email": "stringstring@example.com",
        "password": "stringstring",
        "confirm_password": "stringstring"
    }
    with TestClient(app) as client:
        response = client.post("/user/", json=request_data)
    assert response.status_code == 422
    assert response.json() == {'detail': 'Email must be unique'}


def test_pass_dont_match(temp_db):
    request_data_bad_password = {
        "username": "stringstring2",
        "email": "stringstring2@example.com",
        "password": "strinstrinstrin",
        "confirm_password": "strinstrin"
    }
    response = client.post("/user/", json=request_data_bad_password)
    assert response.status_code == 400
    assert response.json() == {'detail': "password don't match"}


def test_get_user_by_id(temp_db):
    with TestClient(app) as client:
        response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json()["id"] == "1"
    assert response.json()["email"] == "stringstring@example.com"
    assert response.json()["username"] == "stringstring"
    assert response.json()["register_date"] is not None


def test_get_not_exist_user_by_id(temp_db):
    with TestClient(app) as client:
        response = client.get("/user/5")
    assert response.json() == {'detail': 'User not found'}


def test_get_user_list(temp_db):
    with TestClient(app) as client:
        response = client.get("/user-list/")
    assert response.json()[0]['email'] == 'stringstring@example.com'
    assert response.json()[0]['id'] == '1'
    assert response.json()[0]['register_date'] is not None
    assert response.json()[0]['username'] == 'stringstring'

    assert response.json()[1]['email'] == 'stringstring1@example.com'
    assert response.json()[1]['id'] == '2'
    assert response.json()[1]['register_date'] is not None
    assert response.json()[1]['username'] == 'stringstring1'


def test_auth(temp_db):
    request_data = {
        "email": "stringstring@example.com",
        "password": "stringstring"
    }
    with TestClient(app) as client:
        response = client.post("/auth/", json=request_data)
    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['token_type'] == 'Bearer'


def test_failed_auth(temp_db):
    request_data = {
        "email": "stringstring1@example.com",
        "password": "stringstring"
    }
    with TestClient(app) as client:
        response = client.post("/auth/", json=request_data)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_patch(temp_db):
    request_data_auth = {
        "email": "stringstring@example.com",
        "password": "stringstring"
    }
    request_data_patch = {
        "username": "stringstringnew",
        "email": "stringstringnew@example.com",
        "password": "stringstringnew"
    }
    with TestClient(app) as client:
        response_auth = client.post("/auth/", json=request_data_auth)
        token = response_auth.json()['access_token']
        response = client.patch("/user/1", json=request_data_patch,
                                headers={'Content-Type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(token)})
    assert response.json()['username'] == 'stringstringnew'
    assert response.json()['email'] == 'stringstringnew@example.com'


def test_patch_unauthorized(temp_db):
    request_data_auth = {
        "email": "stringstringnew@example.com",
        "password": "stringstringnew"
    }
    request_data_patch = {
        "username": "stringstringnew",
        "email": "stringstringnew@example.com",
        "password": "stringstringnew"
    }
    with TestClient(app) as client:
        response_auth = client.post("/auth/", json=request_data_auth)
        token = response_auth.json()['access_token']
        response = client.patch("/user/2", json=request_data_patch,
                                headers={'Content-Type': 'application/json',
                                         'Authorization': 'Bearer {}'.format(token)})
    assert response.json() == {'detail': 'User not found'}


def test_put(temp_db):
    request_data_auth = {
        "email": "stringstringnew@example.com",
        "password": "stringstringnew"
    }
    request_data_patch = {
        "username": "testestest",
        "email": "testestest@example.com",
        "password": "testestest",
        "confirm_password": "testestest"
    }
    with TestClient(app) as client:
        response_auth = client.post("/auth/", json=request_data_auth)
        token = response_auth.json()['access_token']
        response = client.put("/user/1", json=request_data_patch,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(token)})
    assert response.json()['username'] == 'testestest'
    assert response.json()['email'] == 'testestest@example.com'


def test_put_unauthorized(temp_db):
    request_data_auth = {
        "email": "testestest@example.com",
        "password": "testestest"
    }
    request_data_patch = {
        "username": "testestest",
        "email": "testestest@example.com",
        "password": "testestest",
        "confirm_password": "testestest"
    }
    with TestClient(app) as client:
        response_auth = client.post("/auth/", json=request_data_auth)
        token = response_auth.json()['access_token']
        response = client.put("/user/2", json=request_data_patch,
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer {}'.format(token)})
    assert response.json() == {'detail': 'User not found'}


def test_delete_unauthorized(temp_db):
    request_data_auth = {
        "email": "testestest@example.com",
        "password": "testestest"
    }
    with TestClient(app) as client:
        response_auth = client.post("/auth/", json=request_data_auth)
        token = response_auth.json()['access_token']
        response = client.delete("/user/2", headers={'Content-Type': 'application/json',
                                                     'Authorization': 'Bearer {}'.format(token)})
    assert response.json() == {'detail': 'User not found'}


def test_delete(temp_db):
    request_data_auth = {
        "email": "testestest@example.com",
        "password": "testestest"
    }
    with TestClient(app) as client:
        response_before_delete = client.get("/user-list/")
        response_auth = client.post("/auth/", json=request_data_auth)
        token = response_auth.json()['access_token']
        response_delete = client.delete("/user/1", headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer {}'.format(token)})
        response_after_delete = client.get("/user-list/")
    assert len(response_before_delete.json()) == 2
    assert response_delete.json()['status_code'] == 200
    assert response_delete.json()['detail'] == 'Successful deleting'
    assert len(response_after_delete.json()) == 1

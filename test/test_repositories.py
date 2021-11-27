import asyncio
import pytest

from models.users import UserAuth, UserPatch
from repositories.users import UserRepository
from databases import Database


@pytest.fixture(scope="module")
def user_repository(temp_db):
    user_repository = UserRepository(Database(temp_db))
    yield user_repository


def test_create_user(user_repository):
    test_user_1 = UserAuth(username="stringstring1", email="stringstring1@example.com",
                           password="stringstring1", confirm_password="stringstring1")
    test_user_2 = UserAuth(username="stringstring2", email="stringstring2@example.com",
                           password="stringstring2", confirm_password="stringstring2")

    response_1 = asyncio.run(user_repository.create(test_user_1))
    response_2 = asyncio.run(user_repository.create(test_user_2))

    assert response_1.id == 1
    assert response_1.username == "stringstring1"
    assert response_1.email == "stringstring1@example.com"
    assert response_2.id == 2
    assert response_2.username == "stringstring2"
    assert response_2.email == "stringstring2@example.com"


def test_get_list_user(user_repository):
    response = asyncio.run(user_repository.get_list_user())
    assert len(response) == 2
    assert response[0][0] == 1
    assert response[0][1] == "stringstring1"


def test_get_by_id(user_repository):
    response = asyncio.run(user_repository.get_by_id(1))
    assert response.id == '1'
    assert response.username == "stringstring1"


def test_update(user_repository):
    update = UserAuth(username="stringstring2new", email="stringstring2new@example.com",
                      password="stringstring2new", confirm_password="stringstring2new")

    response = asyncio.run(user_repository.update(2, update))
    response_1 = asyncio.run(user_repository.get_by_id(2))
    assert response_1.username == "stringstring2new"
    assert response.username == "stringstring2new"
    assert response.email == "stringstring2new@example.com"


def test_patch(user_repository):
    patch = UserPatch(email="stringstring2@example.com")

    response = asyncio.run(user_repository.patch(2, patch))
    response_1 = asyncio.run(user_repository.get_by_id(2))
    assert response_1.email == "stringstring2@example.com"
    assert response.email == "stringstring2@example.com"


def test_get_by_email(user_repository):
    response = asyncio.run(
        user_repository.get_by_email('stringstring2@example.com'))
    assert response.username == 'stringstring2new'


def test_delete(user_repository):
    before = asyncio.run(user_repository.get_list_user())
    response = asyncio.run(user_repository.delete(2))
    after = asyncio.run(user_repository.get_list_user())
    assert len(before) == 2
    assert len(after) == 1
    assert response.status_code == 200

import bcrypt
import pytest
from httpx import AsyncClient
from pydantic import EmailStr
from pytest_mock import MockFixture

from src.auth.models import UserSchema

ENDPOINT = "/api/Users"


@pytest.mark.anyio
async def test_create_user(client: AsyncClient, mocker: MockFixture):
    user_data = {
        "fullname": "testuser",
        "password": "password123",
        "email": EmailStr("test@example.com"),
    }
    user = UserSchema(**user_data)
    mocker.patch("src.auth.service.create_user", return_value=user)
    mocker.patch("src.auth.handler.get_jwt_variables", return_value=("secret", "HS256"))

    response = await client.post(f"{ENDPOINT}/signup", json=user_data)

    assert response.status_code == 201
    assert "access_token" in response.json()


@pytest.mark.anyio
async def test_create_user_with_existing_email(
    client: AsyncClient, mocker: MockFixture
):
    user_data = {
        "fullname": "testuser",
        "password": "password123",
        "email": EmailStr("test@example.com"),
    }
    mocker.patch(
        "src.auth.service.fetch_user_by_email",
        return_value={"email": "test@example.com"},
    )
    response = await client.post(f"{ENDPOINT}/signup", json=user_data)
    assert response.status_code == 400


@pytest.mark.anyio
async def test_create_user_with_invalid_email(client: AsyncClient, mocker: MockFixture):
    user_data = {
        "fullname": "testuser",
        "password": "password123",
        "email": EmailStr("test.example.com"),
    }
    mocker.patch("src.auth.service.create_user", return_value=user_data)
    response = await client.post(f"{ENDPOINT}/signup", json=user_data)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_not_existing_user_login(client: AsyncClient, mocker: MockFixture):
    user_data = {
        "fullname": "testuser",
        "password": "password123",
        "email": EmailStr("test@example.com"),
    }
    hashed_password = bcrypt.hashpw(user_data["password"].encode(), bcrypt.gensalt())
    user_data["password"] = hashed_password.decode()
    response = await client.post(f"{ENDPOINT}/login", json=user_data)
    assert response.status_code == 401


@pytest.mark.anyio
async def test_existing_user_login(client: AsyncClient, mocker: MockFixture):
    user_data = {
        "fullname": "testuser",
        "password": "password123",
        "email": EmailStr("test@example.com"),
    }
    hashed_password = bcrypt.hashpw(user_data["password"].encode(), bcrypt.gensalt())
    user_data["password"] = hashed_password.decode()
    mocker.patch("src.auth.service.fetch_user_by_email", return_value=user_data)
    response = await client.post(
        f"{ENDPOINT}/login",
        json={"email": user_data["email"], "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

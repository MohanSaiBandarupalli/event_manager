import pytest
from pydantic import ValidationError
from datetime import datetime
from uuid import uuid4
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, LoginRequest

# Tests for UserBase
def test_user_base_valid():
    user_base_data = {
        "email": "john.doe@example.com",
        "nickname": "john_doe123",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
    }
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid():
    user_create_data = {
        "email": "john.doe@example.com",
        "password": "SecurePassword123!",
        "nickname": "john_doe123",
    }
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid():
    user_update_data = {
        "email": "john.doe.new@example.com",
        "nickname": "john_updated",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg",
    }
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.nickname == user_update_data["nickname"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid():
    user_response_data = {
        "id": uuid4(),
        "email": "test@example.com",
        "nickname": "response_user",
        "role": "AUTHENTICATED",
        "created_at": datetime.now(),
        "last_login_at": datetime.now(),
    }
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    assert user.nickname == user_response_data["nickname"]

# Tests for LoginRequest
def test_login_request_valid():
    login_request_data = {
        "email": "john.doe@example.com",
        "password": "SecurePassword123!",
    }
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

def test_login_request_missing_email():
    login_request_data = {
        "password": "SecurePassword123!",
    }
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(**login_request_data)
    assert "email" in str(exc_info.value)

def test_login_request_missing_password():
    login_request_data = {
        "email": "john.doe@example.com",
    }
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(**login_request_data)
    assert "password" in str(exc_info.value)

def test_login_request_invalid_password():
    login_request_data = {
        "email": "john.doe@example.com",
        "password": "short",
    }
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(**login_request_data)
    # Corrected the error message to match the actual Pydantic validation output
    assert "String should have at least 8 characters" in str(exc_info.value)

# Parametrized tests for nickname validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname):
    user_base_data = {
        "email": "john.doe@example.com",
        "nickname": nickname,
    }
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname):
    user_base_data = {
        "email": "john.doe@example.com",
        "nickname": nickname,
    }
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url):
    user_base_data = {
        "email": "john.doe@example.com",
        "nickname": "john_doe123",
        "profile_picture_url": url,
    }
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url):
    user_base_data = {
        "email": "john.doe@example.com",
        "nickname": "john_doe123",
        "profile_picture_url": url,
    }
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Tests for invalid email
def test_user_base_invalid_email():
    user_base_data_invalid = {
        "email": "john.doe.example.com",
        "nickname": "john_doe123",
    }
    with pytest.raises(ValidationError) as exc_info:
        UserBase(**user_base_data_invalid)

    assert "value is not a valid email address" in str(exc_info.value)

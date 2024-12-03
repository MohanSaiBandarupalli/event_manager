import pytest
from pydantic import ValidationError
from uuid import uuid4
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, LoginRequest

# Fixture for user base data
@pytest.fixture
def user_base_data():
    return {
        "email": "john.doe@example.com",
        "nickname": "john_doe123",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I am a software engineer.",
        "profile_picture_url": "https://example.com/profile.jpg",
    }

# Test valid UserBase schema
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]
    assert user.first_name == user_base_data["first_name"]

# Test missing nickname in UserCreate
def test_user_create_missing_nickname(user_base_data):
    user_create_data = {**user_base_data, "password": "SecurePassword123!"}
    user_create_data.pop("nickname")
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**user_create_data)
    assert "Field required" in str(exc_info.value), f"Unexpected error message: {str(exc_info.value)}"

# Test no values provided in UserUpdate
def test_user_update_no_values():
    with pytest.raises(ValueError) as exc_info:
        UserUpdate()
    assert "At least one field must be provided for the update" in str(exc_info.value)

# Test valid UserUpdate
def test_user_update_valid():
    update_data = {"email": "updated.email@example.com", "bio": "Updated bio"}
    user_update = UserUpdate(**update_data)
    assert user_update.email == "updated.email@example.com"
    assert user_update.bio == "Updated bio"

# Test invalid password in LoginRequest with parameterized cases
@pytest.mark.parametrize(
    "password, error_message",
    [
        ("short", "Password must have at least 8 characters"),
        ("NOLOWERCASE123!", "Password must include a lowercase letter."),
        ("nouppercase123!", "Password must include an uppercase letter."),
        ("NoSpecial123", "Password must include a special character."),
    ],
)
def test_login_request_invalid_password(password, error_message):
    login_request_data = {"email": "john.doe@example.com", "password": password}
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(**login_request_data)
    assert error_message in str(exc_info.value)

# Test valid LoginRequest
def test_login_request_valid():
    login_request_data = {
        "email": "john.doe@example.com",
        "password": "SecurePassword123!",
    }
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Test invalid email in UserBase
def test_user_base_invalid_email():
    invalid_data = {
        "email": "john.doe.example.com",  # Invalid email
        "nickname": "john_doe123",
    }
    with pytest.raises(ValidationError) as exc_info:
        UserBase(**invalid_data)
    assert "value is not a valid email address" in str(exc_info.value)

# Test valid UserResponse
def test_user_response_valid():
    user_response_data = {
        "id": uuid4(),
        "email": "test@example.com",
        "nickname": "response_user",
        "role": "AUTHENTICATED",
        "is_professional": True,
    }
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    assert user.nickname == user_response_data["nickname"]
    assert user.role == "AUTHENTICATED"
    assert user.is_professional is True

# Test valid nickname formats with parameterized cases
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname):
    data = {
        "email": "john.doe@example.com",
        "nickname": nickname,
    }
    user = UserBase(**data)
    assert user.nickname == nickname

# Test invalid nickname formats with parameterized cases
@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname):
    data = {
        "email": "john.doe@example.com",
        "nickname": nickname,
    }
    with pytest.raises(ValidationError):
        UserBase(**data)

# Test valid profile picture URL formats
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url):
    data = {
        "email": "john.doe@example.com",
        "nickname": "john_doe123",
        "profile_picture_url": url,
    }
    user = UserBase(**data)
    assert user.profile_picture_url == url

# Test invalid profile picture URL formats
@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url):
    data = {
        "email": "john.doe@example.com",
        "nickname": "john_doe123",
        "profile_picture_url": url,
    }
    with pytest.raises(ValidationError):
        UserBase(**data)
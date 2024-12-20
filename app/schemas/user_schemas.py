from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re
from app.utils.nickname_gen import generate_nickname

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: str = Field(default_factory=generate_nickname, min_length=3, pattern=r'^[\w-]+$', example="john_doe")
    first_name: str = Field(default="First", example="John")
    last_name: str = Field(default="Last", example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profile.jpg")
    linkedin_profile_url: Optional[str] = Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    nickname: str = Field(..., min_length=3, pattern=r'^[\w-]+$', example="john_doe")  # Required nickname
    password: str = Field(..., min_length=8, example="SecurePassword123!")  # Required password

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must have at least 8 characters.")
        if not any(c.islower() for c in password):
            raise ValueError("Password must include a lowercase letter.")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must include an uppercase letter.")
        if not any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in password):
            raise ValueError("Password must include a special character.")
        return password

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example="john_doe")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Updated bio")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profile.jpg")
    linkedin_profile_url: Optional[str] = Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for the update.")
        return values

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    is_professional: Optional[bool] = Field(default=False, example=True)

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="SecurePassword123!")

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must have at least 8 characters.")
        if not any(c.islower() for c in password):
            raise ValueError("Password must include a lowercase letter.")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must include an uppercase letter.")
        if not any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in password):
            raise ValueError("Password must include a special character.")
        return password

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="Resource not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(...)
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
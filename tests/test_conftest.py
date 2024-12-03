# test_users.py

from builtins import len
import pytest
from httpx import AsyncClient
from sqlalchemy.future import select
import uuid
from app.models.user_model import User, UserRole
from app.utils.security import verify_password
from app.database import Base

@pytest.mark.asyncio
async def test_user_creation(db_session, verified_user):
    """Test that a user is correctly created and stored in the database."""
    result = await db_session.execute(select(User).filter_by(email=verified_user.email))
    stored_user = result.scalars().first()
    assert stored_user is not None
    assert stored_user.email == verified_user.email
    assert verify_password("MySuperPassword$1234", stored_user.hashed_password)

# Apply similar corrections to other test functions
@pytest.mark.asyncio
async def test_locked_user(db_session, locked_user):
    result = await db_session.execute(select(User).filter_by(email=locked_user.email))
    stored_user = result.scalars().first()
    assert stored_user.is_locked

@pytest.mark.asyncio
async def test_verified_user(db_session, verified_user):
    result = await db_session.execute(select(User).filter_by(email=verified_user.email))
    stored_user = result.scalars().first()
    assert stored_user.email_verified

@pytest.mark.asyncio
async def test_user_role(db_session, admin_user):
    result = await db_session.execute(select(User).filter_by(email=admin_user.email))
    stored_user = result.scalars().first()
    assert stored_user.role == UserRole.ADMIN

@pytest.mark.asyncio
async def test_bulk_user_creation_performance(db_session, users_with_same_role_50_users):
    result = await db_session.execute(select(User).filter_by(role=UserRole.AUTHENTICATED))
    users = result.scalars().all()
    assert len(users) == 50

@pytest.mark.asyncio
async def test_password_hashing(user):
    assert verify_password("MySuperPassword$1234", user.hashed_password)

@pytest.mark.asyncio
async def test_user_unlock(db_session, locked_user):
    locked_user.unlock_account()
    await db_session.commit()
    result = await db_session.execute(select(User).filter_by(email=locked_user.email))
    updated_user = result.scalars().first()
    assert not updated_user.is_locked

@pytest.mark.asyncio
async def test_update_professional_status(db_session, verified_user):
    verified_user.update_professional_status(True)
    await db_session.commit()
    result = await db_session.execute(select(User).filter_by(email=verified_user.email))
    updated_user = result.scalars().first()
    assert updated_user.is_professional
    assert updated_user.professional_status_updated_at is not None

@pytest.fixture(scope="function", autouse=True)
async def clear_database(db_session):
    """Cleans up database tables after each test."""
    yield
    for table in reversed(Base.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()

@pytest.fixture
async def users_with_same_role_50_users(db_session):
    """Creates 50 users with unique nicknames."""
    users = []
    for i in range(50):
        user = User(
            email=f"user{i}@example.com",
            nickname=f"user_{uuid.uuid4().hex[:8]}",
            hashed_password="hashed_password",
            role=UserRole.AUTHENTICATED
        )
        db_session.add(user)
        users.append(user)
    await db_session.commit()
    return users

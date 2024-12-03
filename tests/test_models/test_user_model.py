from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User, UserRole

@pytest.mark.asyncio
async def test_user_role(db_session: AsyncSession, user: User, admin_user: User, manager_user: User):
    """
    Tests that the default role is assigned correctly and can be updated.
    """
    assert user.role == UserRole.AUTHENTICATED, "Default role should be AUTHENTICATED"
    assert admin_user.role == UserRole.ADMIN, "Admin role should be correctly assigned"
    assert manager_user.role == UserRole.MANAGER, "Manager role should be correctly assigned"

@pytest.mark.asyncio
async def test_has_role(user: User, admin_user: User, manager_user: User):
    """
    Tests the has_role method to ensure it accurately checks the user's role.
    """
    assert user.has_role(UserRole.AUTHENTICATED), "User should have AUTHENTICATED role"
    assert not user.has_role(UserRole.ADMIN), "User should not have ADMIN role"
    assert admin_user.has_role(UserRole.ADMIN), "Admin user should have ADMIN role"
    assert manager_user.has_role(UserRole.MANAGER), "Manager user should have MANAGER role"

@pytest.mark.asyncio
async def test_user_repr(user: User):
    """
    Tests the __repr__ method for accurate representation of the User object.
    """
    assert repr(user) == f"<User {user.nickname}, Role: {user.role.name}>", "__repr__ should include nickname and role"

@pytest.mark.asyncio
async def test_account_lock_and_unlock(db_session: AsyncSession, user: User):
    """
    Tests locking and unlocking the user account.
    """
    # Initially, the account should not be locked.
    assert not user.is_locked, "Account should initially be unlocked"

    # Lock the account and verify.
    user.lock_account()
    await db_session.commit()
    await db_session.refresh(user)
    assert user.is_locked, "Account should be locked after calling lock_account()"

    # Unlock the account and verify.
    user.unlock_account()
    await db_session.commit()
    await db_session.refresh(user)
    assert not user.is_locked, "Account should be unlocked after calling unlock_account()"

@pytest.mark.asyncio
async def test_email_verification(db_session: AsyncSession, user: User):
    """
    Tests the email verification functionality.
    """
    # Initially, the email should not be verified.
    assert not user.email_verified, "Email should initially be unverified"

    # Verify the email and check.
    user.verify_email()
    await db_session.commit()
    await db_session.refresh(user)
    assert user.email_verified, "Email should be verified after calling verify_email()"

@pytest.mark.asyncio
async def test_failed_login_attempts_increment(db_session: AsyncSession, user: User):
    """
    Tests that failed login attempts can be incremented and persisted correctly.
    """
    initial_attempts = user.failed_login_attempts
    user.failed_login_attempts += 1
    await db_session.commit()
    await db_session.refresh(user)
    assert user.failed_login_attempts == initial_attempts + 1, "Failed login attempts should increment"

@pytest.mark.asyncio
async def test_last_login_update(db_session: AsyncSession, user: User):
    """
    Tests updating the last login timestamp.
    """
    new_last_login = datetime.now(timezone.utc)
    user.last_login_at = new_last_login
    await db_session.commit()
    await db_session.refresh(user)
    assert user.last_login_at == new_last_login, "Last login timestamp should update correctly"

@pytest.mark.asyncio
async def test_user_profile_pic_update(db_session: AsyncSession, user: User):
    """
    Tests updating the user's profile picture URL.
    """
    new_profile_pic_url = "https://example.com/new_picture.png"
    user.profile_picture_url = new_profile_pic_url
    await db_session.commit()
    await db_session.refresh(user)
    assert user.profile_picture_url == new_profile_pic_url, "Profile picture URL should be updated correctly"

@pytest.mark.asyncio
async def test_user_linkedin_url_update(db_session: AsyncSession, user: User):
    """
    Tests updating the user's LinkedIn profile URL.
    """
    new_linkedin_url = "https://linkedin.com/in/new-profile"
    user.linkedin_profile_url = new_linkedin_url
    await db_session.commit()
    await db_session.refresh(user)
    assert user.linkedin_profile_url == new_linkedin_url, "LinkedIn profile URL should be updated correctly"

@pytest.mark.asyncio
async def test_user_github_url_update(db_session: AsyncSession, user: User):
    """
    Tests updating the user's GitHub profile URL.
    """
    new_github_url = "https://github.com/new-profile"
    user.github_profile_url = new_github_url
    await db_session.commit()
    await db_session.refresh(user)
    assert user.github_profile_url == new_github_url, "GitHub profile URL should be updated correctly"

@pytest.mark.asyncio
async def test_user_update_role(db_session: AsyncSession, user: User):
    """
    Tests updating the user's role and ensuring the change persists.
    """
    new_role = UserRole.ADMIN
    user.role = new_role
    await db_session.commit()
    await db_session.refresh(user)
    assert user.role == new_role, "User role should be updated to ADMIN"

@pytest.mark.asyncio
async def test_user_pro_status_update(db_session: AsyncSession, user: User):
    """
    Tests updating the user's professional status.
    """
    user.update_professional_status(True)
    await db_session.commit()
    await db_session.refresh(user)
    assert user.is_professional, "User should have professional status set to True"
    assert user.professional_status_updated_at is not None, "Professional status update timestamp should be set"

@pytest.mark.asyncio
async def test_default_role_assignment(db_session: AsyncSession):
    """
    Tests that a user without a specified role defaults to ANONYMOUS.
    """
    user = User(nickname="new_user", email="new@example.com", hashed_password="hashed_password")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    assert user.role == UserRole.ANONYMOUS, "Default role should be ANONYMOUS if not specified"

@pytest.mark.asyncio
async def test_email_verification_token_update(db_session: AsyncSession, user: User):
    """
    Tests generating and clearing the email verification token.
    """
    user.verification_token = "some_token"
    await db_session.commit()
    await db_session.refresh(user)
    assert user.verification_token == "some_token", "Verification token should be updated correctly"

    user.verification_token = None
    await db_session.commit()
    await db_session.refresh(user)
    assert user.verification_token is None, "Verification token should be cleared"

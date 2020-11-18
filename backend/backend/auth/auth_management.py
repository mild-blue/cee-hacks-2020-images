from typing import Optional

from backend.auth.crypto.password_crypto import encode_password
from backend.error_handling.exceptions.entity_exceptions import EntityUpdateException
from common.db.model.app_user import AppUser
from common.db.repository.app_user_repository import AppUserRepository
from common.enums.app_user_role import AppUserRole


def register_user(username: str,
                  password: str,
                  role: AppUserRole) -> AppUser:
    """
    Registers new user for given email, password and role.
    """
    normalized_username = username.lower()
    _assert_user_registration(normalized_username, password, role)

    user = AppUser(
        username=normalized_username,
        pass_hash=encode_password(password),
        role=role,
    )
    return AppUserRepository.create(user)


def _assert_user_registration(normalized_username: str, password: str, role: Optional[AppUserRole]):
    if not normalized_username:
        raise EntityUpdateException('Invalid username.')
    if not role:
        raise EntityUpdateException('Invalid user role.')
    if AppUserRepository.get_by_username(normalized_username):
        raise EntityUpdateException('The username is already in use.')

    _assert_user_password_validity(password)


def _assert_user_password_validity(password: str):
    # TODO define our password policies for the users
    if not password:
        raise EntityUpdateException('Invalid password.')

import logging
from datetime import timedelta

from backend.auth.crypto.jwt_crypto import encode_auth_token
from backend.auth.crypto.password_crypto import password_matches_hash
from backend.auth.request_context import get_request_token
from backend.configuration.application_configuration import get_application_configuration
from backend.error_handling.exceptions.auth_exceptions import CredentialsMismatchException
from common.db.repository.app_user_repository import AppUserRepository

logger = logging.getLogger(__name__)


def credentials_login(username: str, password: str) -> str:
    """
    Starts login flow for the given credentials. Returns valid JWT,
    if verification fails, some AuthenticationException is raised.
    """
    user = AppUserRepository.get_by_username(username)
    if not user or not password_matches_hash(user.pass_hash, password):
        logger.warning(f'User {username} credentials mismatch during login.')
        raise CredentialsMismatchException()

    conf = get_application_configuration()
    return encode_auth_token(user_id=user.id,
                             user_role=user.role,
                             expiration=timedelta(days=conf.jwt_expiration_days),
                             jwt_secret=conf.jwt_secret)


def refresh_token() -> str:
    """
    Refreshes JWT for users, does not work for SERVICE accounts and OTP tokens.
    """
    token = get_request_token()
    conf = get_application_configuration()
    return encode_auth_token(user_id=token.user_id,
                             user_role=token.role,
                             expiration=timedelta(days=conf.jwt_expiration_days),
                             jwt_secret=conf.jwt_secret)

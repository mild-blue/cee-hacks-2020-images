from flask import g, request

from backend.auth.crypto.jwt_crypto import parse_request_token
from backend.auth.model import DecodedBearerToken
from backend.configuration.application_configuration import get_application_configuration
from common.enums.app_user_role import AppUserRole


def get_request_token() -> DecodedBearerToken:
    """
    Returns token of the currently logged in user.
    Token is present in the header Authorization: Bearer <real_token>
    """
    return parse_request_token(
        auth_header=request.headers.get('Authorization'),
        jwt_secret=get_application_configuration().jwt_secret
    )


def store_user_in_context(user_id: int, user_role: AppUserRole):
    """
    Sets user id and role for the current request context.
    """
    g.user_id = user_id
    g.user_role = user_role


def get_user_role():
    """
    Retrieves role from the request context.
    """
    return g.user_role

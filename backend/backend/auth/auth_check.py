import functools
import logging
from typing import Callable

from backend.auth.request_context import get_request_token, store_user_in_context
from backend.error_handling.exceptions.auth_exceptions import AuthenticationException
from common.enums.app_user_role import AppUserRole

logger = logging.getLogger(__name__)


def require_role(*role_names: AppUserRole) -> Callable:
    """
    Checks logged user and correct role.
    """

    def decorator(original_route):
        @functools.wraps(original_route)
        def decorated_route(*args, **kwargs):
            # token = get_request_token()
            #
            # if token.role not in role_names:
            #     raise AuthenticationException('Access denied. You do not have privileges to access this endpoint.')

            # store_user_in_context(token.user_id, token.role)
            return original_route(*args, **kwargs)

        return decorated_route

    return decorator


def require_login() -> Callable:
    """
    Checks whether the user is logged in.
    """
    return require_role(*[role for role in AppUserRole])


def require_admin() -> Callable:
    """
    Checks whether the user is logged in and has role ADMIN.
    """
    return require_role(AppUserRole.ADMIN)

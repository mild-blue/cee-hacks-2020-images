from backend.error_handling.exceptions import BaseBackendException


class AuthenticationException(BaseBackendException):
    """
    Base class for Authentication related exceptions.
    """


class InvalidJWTException(AuthenticationException):
    """
    Exception indicating that JWT is invalid for some reason.
    """


class CredentialsMismatchException(AuthenticationException):
    """
    Email and password don't match.
    """

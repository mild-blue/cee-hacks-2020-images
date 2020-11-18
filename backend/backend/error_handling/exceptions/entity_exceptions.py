from backend.error_handling.exceptions import BaseBackendException


class EntityUpdateException(BaseBackendException):
    """
    Raised if it was not possible to update or create application entity such as user.
    """

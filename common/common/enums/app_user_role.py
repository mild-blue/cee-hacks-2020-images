from enum import Enum


class AppUserRole(str, Enum):
    ADMIN = 'ADMIN'
    SERVICE = 'SERVICE'

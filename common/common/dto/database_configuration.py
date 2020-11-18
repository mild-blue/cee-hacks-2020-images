from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfiguration:
    """
    Configuration of the DB.
    """
    postgres_user: str
    postgres_password: str
    postgres_url: str
    postgres_db: str

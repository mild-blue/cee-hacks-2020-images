from unittest import TestCase

from common.db.database import close_db, get_db_session, get_engine, init_db, build_db_connection_string
from common.dto.database_configuration import DatabaseConfiguration

DB_CONFIG = DatabaseConfiguration(
    postgres_url="postgres:5432",
    postgres_db="somedb",
    postgres_user="user",
    postgres_password="passwd"
)


class DatabaseTest(TestCase):
    """
    Base Db repository test class
    """

    def test_build_db_connection_string(self) -> None:
        expected_with_psycopg2 = f"postgresql+psycopg2://{DB_CONFIG.postgres_user}:" \
                                 f"{DB_CONFIG.postgres_password}@{DB_CONFIG.postgres_url}/" \
                                 f"{DB_CONFIG.postgres_db}"
        connection_string = build_db_connection_string(
            DB_CONFIG.postgres_user,
            DB_CONFIG.postgres_password,
            DB_CONFIG.postgres_url,
            DB_CONFIG.postgres_db
        )
        self.assertEqual(expected_with_psycopg2, connection_string)

        expected_without_psycopg2 = f"postgresql://{DB_CONFIG.postgres_user}:" \
                                    f"{DB_CONFIG.postgres_password}@{DB_CONFIG.postgres_url}/" \
                                    f"{DB_CONFIG.postgres_db}"
        connection_string = build_db_connection_string(
            DB_CONFIG.postgres_user,
            DB_CONFIG.postgres_password,
            DB_CONFIG.postgres_url,
            DB_CONFIG.postgres_db,
            False
        )
        self.assertEqual(expected_without_psycopg2, connection_string)

    def test_init_close_db(self) -> None:
        close_db()
        self.assertIsNone(get_db_session())
        self.assertIsNone(get_engine())

        init_db(DB_CONFIG)

        self.assertIsNotNone(get_db_session())
        self.assertIsNotNone(get_engine())

        close_db()

        self.assertIsNone(get_db_session())
        self.assertIsNone(get_engine())

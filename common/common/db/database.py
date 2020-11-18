import logging
import os
from typing import List, Union, Callable, TypeVar, Tuple, Optional

from sqlalchemy import create_engine  # pylint: disable=import-error
from sqlalchemy.engine.base import Engine  # pylint: disable=import-error
from sqlalchemy.orm import scoped_session, sessionmaker, Session  # pylint: disable=import-error
from yoyo import get_backend  # pylint: disable=import-error
from yoyo.backends import DatabaseBackend  # pylint: disable=import-error
from yoyo.migrations import MigrationList, read_migrations  # pylint: disable=import-error

from common.db.base import Base
from common.dto.database_configuration import DatabaseConfiguration

_db_session: Optional[scoped_session] = None
_db_engine: Optional[Engine] = None
InitDbCallback = Callable[[Session, Engine, str], None]
_on_init_db_callbacks: List[InitDbCallback] = []

META_DB_NAME = "postgres"

logger = logging.getLogger(__name__)


def get_db_session() -> Optional[scoped_session]:
    return _db_session


def get_engine() -> Optional[Engine]:
    return _db_engine


def close_db() -> None:
    logger.info("Closing DB.")
    session = get_db_session()
    if session is None:
        logger.info("DB session is None, DB could be already closed -> end.")
        return

    # pylint: disable=E1101
    session.close()  # type:ignore
    global _db_session  # pylint: disable=W0603
    _db_session = None
    global _db_engine  # pylint: disable=W0603
    _db_engine = None

    Base.query = None
    logger.info("DB closed.")


def build_db_connection_string(
        postgres_user: str,
        postgres_password: str,
        postgres_url: str,
        postgres_db: str,
        with_psycopg2: bool = True
) -> str:
    prefix = 'postgresql+psycopg2' if with_psycopg2 else 'postgresql'
    return f'{prefix}://{postgres_user}:{postgres_password}@{postgres_url}/{normalize_db_name(postgres_db)}'


def add_on_init_db_callback(callback: InitDbCallback) -> None:
    global _on_init_db_callbacks  # pylint: disable=W0603
    _on_init_db_callbacks.append(callback)


def clean_on_init_db_callback() -> None:
    global _on_init_db_callbacks  # pylint: disable=W0603
    _on_init_db_callbacks = []


def prepare_db_session(
        db_config: DatabaseConfiguration,
        db_name: Union[str, None],
        store: bool = True
) -> Tuple[scoped_session, Engine]:
    connection = build_db_connection_string(
        postgres_user=db_config.postgres_user,
        postgres_password=db_config.postgres_password,
        postgres_url=db_config.postgres_url,
        postgres_db=db_config.postgres_db if db_name is None else db_name
    )
    logger.info(f"Connecting to: '{db_config.postgres_url}/{db_config.postgres_db} as {db_config.postgres_user}'.")
    db_engine = create_engine(connection)

    db_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=db_engine
        )
    )

    if store:
        global _db_engine  # pylint: disable=W0603
        _db_engine = db_engine
        global _db_session  # pylint: disable=W0603
        _db_session = db_session

    return db_session, db_engine


# pylint: disable=unused-argument
def init_db(db_config: DatabaseConfiguration, db_name: Union[str, None] = None) -> None:
    """
    Initialize DB
    :param db_config: DB configuration
    :param db_name: Explicit DB name
    """

    logger.info("Initializing DB.")
    if get_db_session() is not None:
        close_db()

    db_session, db_engine = prepare_db_session(db_config, db_name)

    for callback in _on_init_db_callbacks:
        callback(
            db_session,
            db_engine,
            build_db_connection_string(
                db_config.postgres_user,
                db_config.postgres_password,
                db_config.postgres_url,
                db_config.postgres_db,
                False
            )
        )

    Base.query = db_session.query_property()  # type:ignore


A = TypeVar('A')


def normalize_db_name(client: str) -> str:
    """
    Normalize name of the client to the db name.
    :param client: client name
    :return: Database name - basically, lowercase of the client name.

    >>> normalize_db_name('AaBa')
    'aaba'
    """
    return client.lower()


def recreate_db(_session: Session, engine: Engine, db_url: str) -> None:
    logger.info("Recreating DB.")
    rollback_db(db_url)
    Base.metadata.drop_all(bind=engine)
    migrate_db(db_url)
    logger.info("DB recreated.")


def migrate_db(db_uri: Optional[str] = None) -> None:
    """
    Runs db migrations.
    :param db_uri
    :return:
    """
    migrations, backend = _prepare_migrations_and_backend(db_uri)

    with backend.lock():
        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))
    logger.info('DB migrations applied.')


def rollback_db(db_uri: Optional[str] = None) -> None:
    """
    Runs db rollback.
    :param db_uri
    :return:
    """
    migrations, backend = _prepare_migrations_and_backend(db_uri)

    with backend.lock():
        # Apply any outstanding migrations
        backend.rollback_migrations(backend.to_rollback(migrations))
    logger.info('DB migration rollbacks applied.')


def build_database_configuration_from_env() -> DatabaseConfiguration:
    """
    Get connection string from ENV.
    :return: Connection string to Postgres.
    """
    return DatabaseConfiguration(
        _get_env_var('POSTGRES_USER'),
        _get_env_var('POSTGRES_PASSWORD'),
        _get_env_var('POSTGRES_URL'),
        _get_env_var('POSTGRES_DB')
    )


def _prepare_migrations_and_backend(db_uri: Optional[str] = None) -> Tuple[MigrationList, DatabaseBackend]:
    """
    Prepares DB migrations and backend.
    :param db_uri
    :return:
    """
    if not db_uri:
        db_config = build_database_configuration_from_env()
        db_uri = build_db_connection_string(
            db_config.postgres_user,
            db_config.postgres_password,
            db_config.postgres_url,
            db_config.postgres_db
        )
    acceptable_db_uri = db_uri.replace('+psycopg2', '')
    directory = os.path.dirname(os.path.realpath(__file__))
    migration_directory = os.path.join(directory, 'migrations')
    logger.info(f'Applying DB migrations from {migration_directory}.')
    migrations = read_migrations(migration_directory)

    if len(migrations) == 0:
        logger.warning('No migrations found.')

    backend = get_backend(acceptable_db_uri)
    logger.info('Applying DB migrations:')
    for migration in migrations:
        logger.info(migration.id)

    return migrations, backend


def _get_env_var(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f'Environment variable "{name}" not set up, can not run migrations.')
    return value

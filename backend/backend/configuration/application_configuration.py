import logging
import os
import re
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from flask import current_app as app

logger = logging.getLogger(__name__)

_DEFAULT_VERSION = 'development'


class ApplicationEnvironment(str, Enum):
    """
    Enum representing the environment the code was build for.
    """
    PRODUCTION = 'PRODUCTION'
    STAGING = 'STAGING'
    DEVELOPMENT = 'DEVELOPMENT'
    UNKNOWN = 'UNKNOWN'


@dataclass(frozen=True)
class ApplicationConfiguration:
    """
    Configuration of the web application.
    """
    # pylint: disable=too-many-instance-attributes
    # because this is configuration, we need a lot of attributes

    code_version: str
    environment: ApplicationEnvironment

    # Postgres configuration
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_url: str

    # MinIO configuration
    minio_url: str
    minio_access_key: str
    minio_secret_key: str
    minio_secure: bool

    # auth configuration
    jwt_secret: str
    jwt_expiration_days: int

    # maximal size for one file in megabytes
    max_file_size_mb: int


def get_application_configuration() -> ApplicationConfiguration:
    """
    Obtains configuration from the application context.
    """
    place_holder = 'APPLICATION_CONFIGURATION'
    if not app.config.get(place_holder):
        app.config[place_holder] = _build_application_configuration()
    return app.config[place_holder]


def _build_application_configuration() -> ApplicationConfiguration:
    """
    Builds configuration from environment or from the Flask properties
    """
    logger.debug('Building configuration.')
    code_version, environment = _get_version()

    config = ApplicationConfiguration(
        code_version=code_version,
        environment=environment,
        postgres_user=_get_prop('POSTGRES_USER'),
        postgres_password=_get_prop('POSTGRES_PASSWORD'),
        postgres_db=_get_prop('POSTGRES_DB'),
        postgres_url=_get_prop('POSTGRES_URL'),
        minio_url=_get_prop('MINIO_URL'),
        minio_access_key=_get_prop('MINIO_ACCESS_KEY'),
        minio_secret_key=_get_prop('MINIO_SECRET_KEY'),
        minio_secure=_get_prop('MINIO_SECURE').lower() == 'true',
        jwt_secret=_get_prop('JWT_SECRET'),
        jwt_expiration_days=int(_get_prop('JWT_EXPIRATION_DAYS')),
        max_file_size_mb=int(_get_prop('MAX_FILE_SIZE_MB'))
    )
    return config


def _get_version() -> Tuple[str, ApplicationEnvironment]:
    """
    Retrieves version from the flask app.

    Returns version of the code and boolean whether the code runs in the production.
    """
    version = _read_version(_DEFAULT_VERSION)
    return version, _determine_application_environment(version)


def _determine_application_environment(version: str) -> ApplicationEnvironment:
    """
    Returns ApplicationEnvironment for the given version.
    >>> _determine_application_environment('1.2.3') == ApplicationEnvironment.PRODUCTION
    True
    >>> _determine_application_environment('10.20.30') == ApplicationEnvironment.PRODUCTION
    True
    >>> _determine_application_environment('10.20.30-dirty') == ApplicationEnvironment.UNKNOWN
    True
    >>> _determine_application_environment('development') == ApplicationEnvironment.DEVELOPMENT
    True
    >>> _determine_application_environment('e80d6319aac1b806cc9a625769d7a3259bcc7099') == ApplicationEnvironment.STAGING
    True
    """
    # match x.y.z semantic versioning
    is_production = bool(re.match(r'^\d+\.\d+\.\d+$', version))
    if is_production:
        return ApplicationEnvironment.PRODUCTION

    # match SHA-1 with 40 alpha numeric characters
    # git commit hash, used in the pipeline for build
    is_staging = bool(re.match(r'\b([a-f0-9]{40})\b', version))
    if is_staging:
        return ApplicationEnvironment.STAGING

    # try to match some development versions we're using
    # in docker, docker-compose and on local machines
    development_versions = {'development-docker', 'docker-compose', _DEFAULT_VERSION}
    if version in development_versions:
        return ApplicationEnvironment.DEVELOPMENT

    return ApplicationEnvironment.UNKNOWN


def _read_version(default: str) -> str:
    """
    Reads version from the file or returns default version.
    """
    file_path = _get_prop('RELEASE_FILE_PATH', optional=True)
    logger.debug(f'File path: {file_path}')

    version = None
    if file_path:
        with open(file_path, 'r') as file:
            version = file.readline().strip()
            logger.debug(f'Setting version as: {version}')

    return version if version else default


def _get_prop(name: str, optional: bool = False) -> str:
    """
    Gets property from environment or from the flask env.
    """
    config = os.environ.get(name, app.config.get(name))
    if not optional and not config:
        logger.error(f'It was not possible to retrieve configuration for property "{name}"!')
        raise EnvironmentError(f'No existing configuration for "{name}" found!')
    return str(config) if config is not None else ''

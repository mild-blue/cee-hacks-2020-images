import logging
from unittest import TestCase

import os
import pathlib
from dotenv import load_dotenv  # pylint: disable=import-error

from common.db.database import init_db, add_on_init_db_callback, recreate_db, build_database_configuration_from_env, \
    close_db, clean_on_init_db_callback
from common.logger import init_logging


class BaseRepositoryTest(TestCase):
    """
    Base Db repository test class
    """

    def setUp(self) -> None:
        load_dotenv(dotenv_path=os.path.join(pathlib.Path().absolute(), '../.env.test'))
        init_logging()
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        clean_on_init_db_callback()
        add_on_init_db_callback(recreate_db)
        init_db(build_database_configuration_from_env())

    def tearDown(self) -> None:
        close_db()

import logging
import os
import pathlib

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
from common.db.database import migrate_db, build_db_connection_string, build_database_configuration_from_env
from common.logger import init_logging
from dotenv import load_dotenv
from pytz import utc

from job_processor import process_job

jobstores = {
    'default': MemoryJobStore()
}
executors = {
    'default': ThreadPoolExecutor(1),
    'processpool': ProcessPoolExecutor(1)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1
}


def main():
    env_file = os.path.join(pathlib.Path().absolute(), '../.env')
    init_logging()
    logger = logging.getLogger(__name__)
    logger.info('Starting worker.')
    load_dotenv(dotenv_path=env_file, verbose=True)
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    conf = build_database_configuration_from_env()
    migrate_db(build_db_connection_string(
        postgres_user=conf.postgres_user,
        postgres_password=conf.postgres_password,
        postgres_url=conf.postgres_url,
        postgres_db=conf.postgres_db
    ))

    scheduler = BlockingScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone=utc
    )
    scheduler.add_job(process_job, 'interval', seconds=10, id='process_job')
    logger.info('Starting scheduler.')
    scheduler.start()


if __name__ == '__main__':
    main()

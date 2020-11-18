from tests.common.db.repository.base_repository_test import BaseRepositoryTest

from common.db.model.app_user import AppUser
from common.db.model.job import Job
from common.db.model.job_transition import JobTransition
from common.db.repository.job_repository import JobRepository
from common.db.repository.job_transition_repository import JobTransitionRepository
from common.enums.app_user_role import AppUserRole
from common.enums.job_status_enum import JobStatusEnum


class JobRepositoryTest(BaseRepositoryTest):

    def test_job_crud(self) -> None:
        """
        Creates and fetch data from db
        :return:
        """
        # Insert one
        app_user = AppUser('user1@example.org', 'pass', AppUserRole.ADMIN)
        job = Job(app_user)
        job1 = JobRepository.create(job)
        self.assertEqual(job, job1)

        jobs = JobRepository.get_all()
        self.assertEqual(1, len(jobs))
        self.assertEqual(jobs[0], job1)

        # Insert and get many
        JobRepository.create_many([
            Job(app_user),
            Job(app_user)
        ])
        jobs = JobRepository.get_all()
        self.assertEqual(3, len(jobs))

        # Get by id
        job1_from_db = JobRepository.get_by_id(job1.id)
        self.assertEqual(job1, job1_from_db)

    def test_get_queued_job_to_process(self) -> None:
        # Should get no job
        no_job = JobRepository.get_queued_job_to_process()
        self.assertIsNone(no_job)

        # Should get job1
        app_user = AppUser('user1@example.org', 'pass', AppUserRole.ADMIN)
        job1 = JobRepository.create(Job(app_user))
        JobTransitionRepository.create_many([JobTransition(JobStatusEnum.QUEUED, job1)]
                                            )
        queued_job = JobRepository.get_queued_job_to_process()
        self.assertEqual(job1, queued_job)

        # Should get job1 again even job2 is created
        job2 = JobRepository.create(Job(app_user))
        JobTransitionRepository.create_many([JobTransition(JobStatusEnum.QUEUED, job2)])
        queued_job = JobRepository.get_queued_job_to_process()
        self.assertEqual(job1, queued_job)

        # Should not get job1 cause it is finished, but job2
        JobTransitionRepository.create_many([
            JobTransition(JobStatusEnum.IN_PROGRESS, job1),
            JobTransition(JobStatusEnum.FINISHED, job1)
        ])

        finished_job = JobRepository.get_queued_job_to_process()
        self.assertEqual(job2, finished_job)

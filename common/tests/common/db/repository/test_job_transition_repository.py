from sqlalchemy.exc import IntegrityError
from tests.common.db.repository.base_repository_test import BaseRepositoryTest

from common.db.model.app_user import AppUser
from common.db.model.job import Job
from common.db.model.job_transition import JobTransition
from common.db.repository.job_transition_repository import JobTransitionRepository
from common.enums.app_user_role import AppUserRole
from common.enums.job_status_enum import JobStatusEnum


class JobTransitionRepositoryTest(BaseRepositoryTest):

    def test_job_transition_crud(self) -> None:
        """
        Creates and fetch data from db
        :return:
        """
        # Insert one

        app_user = AppUser('user1@example.org', 'pass', AppUserRole.ADMIN)
        job = Job(app_user)
        job_transition = JobTransition(JobStatusEnum.QUEUED, job)
        job_transition1 = JobTransitionRepository.create(job_transition)
        self.assertEqual(job_transition, job_transition1)

        job_transitions = JobTransitionRepository.get_all()
        self.assertEqual(1, len(job_transitions))
        self.assertEqual(job_transitions[0], job_transition1)

        # Insert and get many
        JobTransitionRepository.create_many([
            JobTransition(JobStatusEnum.IN_PROGRESS, job),
            JobTransition(JobStatusEnum.FINISHED, job)
        ])
        job_transitions = JobTransitionRepository.get_all()
        self.assertEqual(3, len(job_transitions))

        # Get by id
        job_transition_from_db = JobTransitionRepository.get_by_id(job_transition1.id)
        self.assertEqual(job_transition1, job_transition_from_db)

    def test_constraints(self) -> None:
        """
        Test constraints
        :return:
        """
        app_user = AppUser('user1@example.org', 'pass', AppUserRole.ADMIN)
        job = Job(app_user)
        JobTransitionRepository.create(JobTransition(JobStatusEnum.QUEUED, job))
        self.assertRaises(IntegrityError, JobTransitionRepository.create, JobTransition(JobStatusEnum.QUEUED, job))

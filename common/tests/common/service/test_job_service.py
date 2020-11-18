from tests.common.db.repository.base_repository_test import BaseRepositoryTest

from common.db.model.app_user import AppUser
from common.db.model.job import Job
from common.db.repository.app_user_repository import AppUserRepository
from common.db.repository.job_transition_repository import JobTransitionRepository
from common.enums.app_user_role import AppUserRole
from common.enums.job_status_enum import JobStatusEnum
from common.exceptions import InvalidArgumentException
from common.service.job_service import JobService


class JobServiceTest(BaseRepositoryTest):
    def test_create_job(self) -> None:
        job = self._create_job(self._create_app_user())
        self.assertEqual(1, len(job.transitions))
        self.assertEqual(JobStatusEnum.INITIAL, job.transitions[0].status)

    def test_add_job_status_for_initial(self) -> None:
        app_user = self._create_app_user()
        job = self._create_job(app_user)

        # Invalid transitions
        for status in [JobStatusEnum.INITIAL, JobStatusEnum.IN_PROGRESS, JobStatusEnum.FINISHED]:
            self.assertRaises(InvalidArgumentException, JobService.add_job_status, job.id, status)

        # Valid transitions
        JobService.add_job_status(job.id, JobStatusEnum.QUEUED)
        JobService.add_job_status(self._create_job(app_user).id, JobStatusEnum.FAILURE)

    def test_add_job_status_for_queued(self) -> None:
        app_user = self._create_app_user()
        job = self._create_job(app_user)
        JobService.add_job_status(job.id, JobStatusEnum.QUEUED)

        # Invalid transitions
        for status in [JobStatusEnum.INITIAL, JobStatusEnum.QUEUED, JobStatusEnum.FINISHED]:
            self.assertRaises(InvalidArgumentException, JobService.add_job_status, job.id, status)

        # Valid transitions
        JobService.add_job_status(job.id, JobStatusEnum.IN_PROGRESS)
        JobService.add_job_status(self._create_job(app_user).id, JobStatusEnum.FAILURE)

    def test_add_job_status_for_in_progress(self) -> None:
        app_user = self._create_app_user()
        job = self._create_job(app_user)
        JobService.add_job_status(job.id, JobStatusEnum.QUEUED)
        JobService.add_job_status(job.id, JobStatusEnum.IN_PROGRESS)

        # Invalid transitions
        for status in [JobStatusEnum.INITIAL, JobStatusEnum.QUEUED, JobStatusEnum.IN_PROGRESS]:
            self.assertRaises(InvalidArgumentException, JobService.add_job_status, job.id, status)

        # Valid transitions
        JobService.add_job_status(job.id, JobStatusEnum.FINISHED)
        job = self._create_job(app_user)
        JobService.add_job_status(job.id, JobStatusEnum.QUEUED)
        JobService.add_job_status(job.id, JobStatusEnum.IN_PROGRESS)
        JobService.add_job_status(job.id, JobStatusEnum.FAILURE)

    def test_add_job_status_for_finished(self) -> None:
        app_user = self._create_app_user()
        job = self._create_job(app_user)
        JobService.add_job_status(job.id, JobStatusEnum.QUEUED)
        JobService.add_job_status(job.id, JobStatusEnum.IN_PROGRESS)
        JobService.add_job_status(job.id, JobStatusEnum.FINISHED)

        # Invalid transitions
        for status in [JobStatusEnum.INITIAL, JobStatusEnum.QUEUED, JobStatusEnum.IN_PROGRESS, JobStatusEnum.FINISHED,
                       JobStatusEnum.FAILURE]:
            self.assertRaises(InvalidArgumentException, JobService.add_job_status, job.id, status)

    def test_add_job_status_for_failure(self) -> None:
        app_user = self._create_app_user()
        job = self._create_job(app_user)
        JobService.add_job_status(job.id, JobStatusEnum.FAILURE)

        # Invalid transitions
        for status in [JobStatusEnum.INITIAL, JobStatusEnum.QUEUED, JobStatusEnum.IN_PROGRESS, JobStatusEnum.FINISHED,
                       JobStatusEnum.FAILURE]:
            self.assertRaises(InvalidArgumentException, JobService.add_job_status, job.id, status)

    def test_get_queued_job_to_process_and_set_it_to_in_progress(self) -> None:
        # Should get no job
        no_job = JobService.get_queued_job_to_process_and_set_it_to_in_progress()
        self.assertIsNone(no_job)

        # Get proper one
        app_user = self._create_app_user()
        job1 = JobService.create_job(app_user.id)
        JobService.add_job_status(job1.id, JobStatusEnum.QUEUED)

        job = JobService.get_queued_job_to_process_and_set_it_to_in_progress()
        self.assertEqual(job1, job)
        new_transition = JobTransitionRepository.get_latest_job_transition(job.id)
        self.assertEqual(JobStatusEnum.IN_PROGRESS, new_transition.status)

    def _create_app_user(self) -> AppUser:
        return AppUserRepository.create(AppUser('user1@example.org', 'pass', AppUserRole.ADMIN))

    def _create_job(self, app_user: AppUser) -> Job:
        return JobService.create_job(app_user.id)

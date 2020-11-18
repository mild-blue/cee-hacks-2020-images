from sqlalchemy.exc import IntegrityError
from tests.common.db.repository.base_repository_test import BaseRepositoryTest

from common.db.model.app_user import AppUser
from common.db.repository.app_user_repository import AppUserRepository
from common.enums.app_user_role import AppUserRole


class AppUserRepositoryTest(BaseRepositoryTest):

    def test_app_user_crud(self) -> None:
        """
        Creates and fetch data from db
        :return:
        """
        # Insert one
        app_user = AppUser('user1@example.org', 'pass', AppUserRole.ADMIN)
        app_user1 = AppUserRepository.create(app_user)
        self.assertEqual(app_user, app_user1)

        app_users = AppUserRepository.get_all()
        self.assertEqual(1, len(app_users))
        self.assertEqual(app_users[0], app_user1)

        # Insert and get many
        AppUserRepository.create_many([
            AppUser('user2@example.org', 'pass', AppUserRole.SERVICE),
            AppUser('user3@example.org', 'pass', AppUserRole.ADMIN)
        ])
        app_users = AppUserRepository.get_all()
        self.assertEqual(3, len(app_users))

        # Get by id
        app_user1_from_db = AppUserRepository.get_by_id(app_user1.id)
        self.assertEqual(app_user1, app_user1_from_db)

    def test_constraints(self) -> None:
        """
        Test constraints
        :return:
        """
        AppUserRepository.create(AppUser('user1@example.org', 'pass', AppUserRole.ADMIN))
        self.assertRaises(IntegrityError, AppUserRepository.create, AppUser('user1@example.org', 'pass', AppUserRole.ADMIN))

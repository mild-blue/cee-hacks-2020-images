from typing import List, Optional, cast

from sqlalchemy.orm import Session  # pylint: disable=import-error

from common.db.database import get_db_session
from common.db.model.app_user import AppUser
from common.db.repository.base_repository import BaseRepository


class AppUserRepository(BaseRepository):
    """
    AppUser repository
    """

    @staticmethod
    def get_all() -> List[AppUser]:
        sup = super(AppUserRepository, AppUserRepository)
        return sup.base_get_all(AppUser)  # type: ignore

    @staticmethod
    def create(app_user: AppUser, commit: bool = True) -> AppUser:
        sup = super(AppUserRepository, AppUserRepository)
        return sup.base_create(app_user, commit)  # type: ignore

    @staticmethod
    def create_many(app_users: List[AppUser], commit: bool = True) -> List[AppUser]:
        sup = super(AppUserRepository, AppUserRepository)
        sup.base_create_many(app_users, commit)  # type: ignore
        return app_users

    @staticmethod
    def count(session: Optional[Session] = None) -> int:
        session = session if session else get_db_session()
        assert session is not None, "DB must be initialized at this point."
        return session.query(AppUser).count()  # type: ignore  # pylint: disable=no-member

    @staticmethod
    def get_by_id(idd: int) -> Optional[AppUser]:
        sup = super(AppUserRepository, AppUserRepository)
        return sup.base_get_by_id(AppUser, idd)  # type: ignore

    @staticmethod
    def get_by_username(username: str) -> Optional[AppUser]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101,C0301
        item = session.query(AppUser).filter(AppUser.username == username).first()  # type: ignore  # noqa: E501
        return cast(AppUser, item)

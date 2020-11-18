from typing import List, cast, Any, Callable, Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session  # pylint: disable=import-error

from common.db.base import Base
from common.db.database import get_db_session


class BaseRepository:
    @staticmethod
    def get_session() -> Optional[Session]:
        return get_db_session()

    @staticmethod
    def base_get_all(entity: Base) -> List[Base]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101
        items = session.query(entity).order_by(entity.id).all()  # type: ignore
        return cast(List[Base], items)

    @staticmethod
    def base_get_by_id(entity: Base, idd: Union[int, UUID]) -> Optional[Base]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101
        item = session.query(entity).get(idd)  # type: ignore
        return cast(Base, item)

    @staticmethod
    def base_filter(entity: Base, query_execution: Callable[[Any], Optional[Base]]) -> Optional[Base]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101
        item = query_execution(session.query(entity))  # type: ignore
        return cast(Base, item)

    @staticmethod
    def base_create(entity: Base, commit: bool = True) -> Base:
        session = BaseRepository.get_session()
        # pylint: disable=E1101
        session.add(entity)  # type: ignore
        if commit:
            # pylint: disable=E1101
            session.commit()  # type: ignore
        return entity

    @staticmethod
    def base_update(entity: Base, commit: bool = True) -> Base:
        session = BaseRepository.get_session()
        if commit:
            # pylint: disable=E1101
            session.commit()  # type: ignore
        return entity

    @staticmethod
    def base_update_all(entities: List[Base], commit: bool = True) -> List[Base]:
        session = BaseRepository.get_session()
        if commit:
            # pylint: disable=E1101
            session.commit()  # type: ignore
        return entities

    @staticmethod
    def base_create_many(entities: List[Base], commit: bool = True) -> List[Base]:
        session = BaseRepository.get_session()
        # pylint: disable=E1101
        session.add_all(entities)  # type: ignore
        if commit:
            # pylint: disable=E1101
            session.commit()  # type: ignore
        return entities

    @staticmethod
    def base_remove_all(entity: Base, commit: bool = True) -> int:
        session = BaseRepository.get_session()
        # pylint: disable=E1101
        num_deleted = session.query(entity).delete()  # type: ignore
        if commit:
            # pylint: disable=E1101
            session.commit()  # type: ignore
        return int(num_deleted)

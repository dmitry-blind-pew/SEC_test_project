from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from typing import Any

from src.core.domain_exc import ObjectNotFoundException


class BaseRepo:
    model = None
    mapper = None

    def __init__(self, session):
        self.session = session

    async def get_one(self, **filter_by: Any) -> Any:
        """Возвращает один объект по фильтрам или поднимает ObjectNotFoundException."""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model_orm = result.scalars().one()
        except NoResultFound as exc:
            raise ObjectNotFoundException() from exc
        return self.mapper.map_to_domain_entity(model_orm)

    async def get_filtered(self, limit: int, offset: int, **filter_by: Any) -> list[Any]:
        """Возвращает список объектов по заданным фильтрам."""
        query = select(self.model).filter_by(**filter_by).order_by(self.model.id).limit(limit).offset(offset)
        result = await self.session.execute(query)
        model_orm = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in model_orm]

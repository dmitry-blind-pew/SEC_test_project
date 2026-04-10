from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.core.domain_exc import ObjectNotFoundException


class BaseRepo:
    model = None
    mapper = None

    def __init__(self, session):
        self.session = session

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model_orm = result.scalars().one()
        except NoResultFound as exc:
            raise ObjectNotFoundException() from exc
        return self.mapper.map_to_domain_entity(model_orm)

    async def get_filtered(self, limit: int, offset: int, **filter_by):
        query = select(self.model).filter_by(**filter_by).order_by(self.model.id).limit(limit).offset(offset)
        result = await self.session.execute(query)
        model_orm = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in model_orm]



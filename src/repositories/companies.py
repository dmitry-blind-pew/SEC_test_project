from sqlalchemy import select, exists

from src.mappers.companies import CompaniesMapper
from src.models import CompaniesORM, ActivitiesORM
from src.models.companies_activities import CompaniesActivitiesORM
from src.repositories.base import BaseRepo


class CompaniesRepo(BaseRepo):
    model = CompaniesORM
    mapper = CompaniesMapper

    async def _get_by_activity_ids_query(self, activity_ids_query):
        stmt = (
            select(self.model)
            .distinct()
            .where(
                exists()
                .select_from(CompaniesActivitiesORM)
                .where(
                    (CompaniesActivitiesORM.company_id == self.model.id) &
                    (CompaniesActivitiesORM.activity_id.in_(activity_ids_query))
                )
            )
        )
        result = await self.session.execute(stmt)
        model_orm = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in model_orm]


    async def get_by_activity(self, *, activity_id: int):
        activity_ids_query = select(ActivitiesORM.id).where(ActivitiesORM.id == activity_id)
        return await self._get_by_activity_ids_query(activity_ids_query)


    async def get_in_activity(self, *, activity_id: int):
        cte = select(ActivitiesORM).where(ActivitiesORM.id == activity_id).cte(recursive=True)
        cte = cte.union_all(
            select(ActivitiesORM).where(ActivitiesORM.parent_id == cte.c.id)
        )
        activity_ids_query = select(cte.c.id)
        return await self._get_by_activity_ids_query(activity_ids_query)

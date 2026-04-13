from src.api.deps import PagDep
from src.schemas.companies import CompaniesOutDTO
from src.services.base import BaseService


class ActivitiesService(BaseService):
    async def get_by_activity(self, *, pagination: PagDep, activity_id: int) -> list[CompaniesOutDTO]:
        return await self.db.companies.get_by_activity(
            activity_id=activity_id, limit=pagination.per_page, offset=pagination.per_page * (pagination.page - 1)
        )

    async def get_in_activity(self, *, pagination: PagDep, activity_id: int) -> list[CompaniesOutDTO]:
        return await self.db.companies.get_in_activity(
            activity_id=activity_id, limit=pagination.per_page, offset=pagination.per_page * (pagination.page - 1)
        )

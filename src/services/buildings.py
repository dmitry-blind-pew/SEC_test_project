from src.api.deps import PagDep
from src.schemas.companies import CompaniesOutDTO
from src.services.base import BaseService


class BuildingsService(BaseService):
    async def get_by_building_id(self, *, pagination: PagDep, building_id: int) -> list[CompaniesOutDTO]:
        return await self.db.companies.get_filtered(
            building_id=building_id, limit=pagination.per_page, offset=pagination.per_page * (pagination.page - 1)
        )

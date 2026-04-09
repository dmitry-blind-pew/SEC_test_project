from src.services.base import BaseService


class BuildingsService(BaseService):
    async def get_by_address(self, *, building_id: int):
        return await self.db.companies.get_filtered(building_id=building_id)
from src.services.base import BaseService


class CompaniesService(BaseService):
    async def get_in_radius(self, *,  radius: float):
        pass

    async def get_in_rectangle(self, *, point: tuple[float,float]):
        pass

    async def get_by_id(self, *, company_id: int):
        return await self.db.companies.get_one(id=company_id)

    async def get_by_name(self, *, name: str):
        return await self.db.companies.get_one(neme=name)
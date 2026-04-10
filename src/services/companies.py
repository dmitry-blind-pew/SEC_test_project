from src.services.base import BaseService


class CompaniesService(BaseService):
    async def get_in_radius(self, *, lon: float, lat: float, radius_m: float):
        return await self.db.companies.get_in_radius(lon=lon, lat=lat, radius_m=radius_m)

    async def get_in_rectangle(self, *, min_lon: float, min_lat: float, max_lon: float, max_lat: float):
        return await self.db.companies.get_in_rectangle(min_lon=min_lon, min_lat=min_lat, max_lon=max_lon, max_lat=max_lat)

    async def get_by_id(self, *, company_id: int):
        return await self.db.companies.get_one(id=company_id)

    async def get_by_name(self, *, name: str):
        return await self.db.companies.get_one(name=name)
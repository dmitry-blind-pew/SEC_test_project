from src.api.deps import PagDep
from src.core.domain_exc import InvalidRectangleBoundsException, ObjectNotFoundException, CompanyNotFoundException
from src.services.base import BaseService


class CompaniesService(BaseService):
    async def get_in_radius(self, *, pagination: PagDep, lon: float, lat: float, radius_m: float):
        return await self.db.companies.get_in_radius(
            lon=lon,
            lat=lat,
            radius_m=radius_m,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )

    async def get_in_rectangle(
        self, *, pagination: PagDep, min_lon: float, min_lat: float, max_lon: float, max_lat: float
    ):
        if min_lon > max_lon or min_lat > max_lat:
            raise InvalidRectangleBoundsException()
        return await self.db.companies.get_in_rectangle(
            min_lon=min_lon,
            min_lat=min_lat,
            max_lon=max_lon,
            max_lat=max_lat,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )

    async def get_by_id(self, *, company_id: int):
        try:
            return await self.db.companies.get_one(id=company_id)
        except ObjectNotFoundException as exc:
            raise CompanyNotFoundException() from exc

    async def get_by_name(self, *, pagination: PagDep, name: str):
        return await self.db.companies.get_by_name(
            name=name, limit=pagination.per_page, offset=pagination.per_page * (pagination.page - 1)
        )

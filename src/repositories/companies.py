from sqlalchemy import exists, func, select
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement

from src.mappers.companies import CompaniesMapper
from src.models import ActivitiesORM, BuildingsORM, CompaniesORM
from src.models.companies_activities import CompaniesActivitiesORM
from src.repositories.base import BaseRepo


class CompaniesRepo(BaseRepo):
    model = CompaniesORM
    mapper = CompaniesMapper

    async def _fetch_companies(self, *, stmt):
        result = await self.session.execute(stmt)
        model_orm = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in model_orm]


    async def _get_by_activity_ids_query(self, *, activity_ids_query):
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
        return await self._fetch_companies(stmt=stmt)


    async def get_by_activity(self, *, activity_id: int):
        activity_ids_query = select(ActivitiesORM.id).where(ActivitiesORM.id == activity_id)
        return await self._get_by_activity_ids_query(activity_ids_query=activity_ids_query)


    async def get_in_activity(self, *, activity_id: int):
        cte = select(ActivitiesORM).where(ActivitiesORM.id == activity_id).cte(recursive=True)
        cte = cte.union_all(
            select(ActivitiesORM).where(ActivitiesORM.parent_id == cte.c.id)
        )
        activity_ids_query = select(cte.c.id)
        return await self._get_by_activity_ids_query(activity_ids_query=activity_ids_query)


    async def get_in_radius(self, *, lon: float, lat: float, radius_m: float):
        point = WKTElement(f"POINT({lon} {lat})", srid=4326)
        stmt = (
            select(self.model)
            .join(BuildingsORM, BuildingsORM.id == self.model.building_id)
            .where(func.ST_DWithin(BuildingsORM.location, point, radius_m))
            .distinct()
        )
        return await self._fetch_companies(stmt=stmt)


    async def get_in_rectangle(
            self,
            *,
            min_lon: float,
            min_lat: float,
            max_lon: float,
            max_lat: float,
    ):
        geom = func.cast(BuildingsORM.location, Geometry(geometry_type="POINT", srid=4326))
        lon_expr = func.ST_X(geom)
        lat_expr = func.ST_Y(geom)
        stmt = (
            select(self.model)
            .join(BuildingsORM, BuildingsORM.id == self.model.building_id)
            .where(lon_expr >= min_lon)
            .where(lon_expr <= max_lon)
            .where(lat_expr >= min_lat)
            .where(lat_expr <= max_lat)
            .distinct()
        )
        return await self._fetch_companies(stmt=stmt)

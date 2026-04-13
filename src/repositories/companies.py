from sqlalchemy import exists, func, select
from typing import Any
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement

from src.mappers.companies import CompaniesMapper
from src.models import ActivitiesORM, BuildingsORM, CompaniesORM
from src.models.companies_activities import CompaniesActivitiesORM
from src.schemas.companies import CompaniesOutDTO
from src.repositories.base import BaseRepo


class CompaniesRepo(BaseRepo):
    model = CompaniesORM
    mapper = CompaniesMapper

    async def _fetch_companies(self, *, stmt: Any) -> list[CompaniesOutDTO]:
        """Выполняет запрос в БД и мапит ORM в DTO."""
        result = await self.session.execute(stmt)
        model_orm = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in model_orm]

    async def _get_by_activity_ids_query(
        self, *, activity_ids_query: Any, limit: int, offset: int
    ) -> list[CompaniesOutDTO]:
        """Возвращает компании, связанные с любым id деятельности из подзапроса."""
        stmt = (
            select(self.model)
            .distinct()
            .where(
                exists()
                .select_from(CompaniesActivitiesORM)
                .where(
                    (CompaniesActivitiesORM.company_id == self.model.id)
                    & (CompaniesActivitiesORM.activity_id.in_(activity_ids_query))
                )
            )
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        return await self._fetch_companies(stmt=stmt)

    async def get_by_activity(self, *, activity_id: int, limit: int, offset: int) -> list[CompaniesOutDTO]:
        """Возвращает компании, напрямую связанные с указанной деятельностью."""
        activity_ids_query = select(ActivitiesORM.id).where(ActivitiesORM.id == activity_id)
        return await self._get_by_activity_ids_query(activity_ids_query=activity_ids_query, limit=limit, offset=offset)

    async def get_in_activity(self, *, activity_id: int, limit: int, offset: int) -> list[CompaniesOutDTO]:
        """
        Формирует рекурсивный CTE, начиная с переданного "activity_id". На каждой итерации рекурсии добавляет дочерние
        узлы по связи "ActivitiesORM.parent_id". Собирает итоговый набор "activity_id" из CTE.
        """
        cte = select(ActivitiesORM.id).where(ActivitiesORM.id == activity_id).cte(recursive=True)
        cte = cte.union_all(select(ActivitiesORM.id).where(ActivitiesORM.parent_id == cte.c.id))
        activity_ids_query = select(cte.c.id)
        return await self._get_by_activity_ids_query(activity_ids_query=activity_ids_query, limit=limit, offset=offset)

    async def get_in_radius(
        self, *, lon: float, lat: float, radius_m: float, limit: int, offset: int
    ) -> list[CompaniesOutDTO]:
        """Возвращает компании в радиусе (в метрах) от географической точки."""
        point = WKTElement(f"POINT({lon} {lat})", srid=4326)
        stmt = (
            select(self.model)
            .join(BuildingsORM, BuildingsORM.id == self.model.building_id)
            .where(func.ST_DWithin(BuildingsORM.location, point, radius_m))
            .distinct()
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        return await self._fetch_companies(stmt=stmt)

    async def get_in_rectangle(
        self, *, min_lon: float, min_lat: float, max_lon: float, max_lat: float, limit: int, offset: int
    ) -> list[CompaniesOutDTO]:
        """Возвращает компании в пределах прямоугольной области по долготе и широте."""
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
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        return await self._fetch_companies(stmt=stmt)

    async def get_by_name(self, *, name: str, limit: int, offset: int) -> list[CompaniesOutDTO]:
        """Возвращает компании по частичному регистронезависимому совпадению имени."""
        stmt = (
            select(self.model)
            .where(self.model.name.ilike(f"%{name}%"))
            .distinct()
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        return await self._fetch_companies(stmt=stmt)

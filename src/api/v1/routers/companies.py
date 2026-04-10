from fastapi import APIRouter, Query

from src.api.deps import DBDep
from src.services.companies import CompaniesService


router = APIRouter()


@router.get("/search/by-radius", summary="Получить компании в радиусе")
async def get_in_radius(
    *,
    lon: float = Query(ge=-180, le=180),
    lat: float = Query(ge=-90, le=90),
    radius_m: float = Query(gt=0),
    db: DBDep
):
    return await CompaniesService(db).get_in_radius(lon=lon, lat=lat, radius_m=radius_m)


@router.get("/search/by-rectangle", summary="Получить компании в области")
async def get_in_rectangle(
    *,
    min_lon: float = Query(ge=-180, le=180),
    min_lat: float = Query(ge=-90, le=90),
    max_lon: float = Query(ge=-180, le=180),
    max_lat: float = Query(ge=-90, le=90),
    db: DBDep
):
    return await CompaniesService(db).get_in_rectangle(
        min_lon=min_lon,
        min_lat=min_lat,
        max_lon=max_lon,
        max_lat=max_lat,
    )


@router.get("/{company_id}", summary="Получить компанию по ID")
async def get_by_id(*, company_id: int, db: DBDep):
    return await CompaniesService(db).get_by_id(company_id=company_id)


@router.get("", summary="Получить компании по названию")
async def get_by_name(*, name: str, db: DBDep):
    return await CompaniesService(db).get_by_name(name=name)
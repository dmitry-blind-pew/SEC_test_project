from fastapi import APIRouter

from src.api.deps import DBDep
from src.services.companies import CompaniesService


router = APIRouter()


@router.get("/search/by-radius", summary="Получить компании в радиусе")
async def get_in_radius(*, radius: float, db: DBDep):
    return await CompaniesService(db).get_in_radius(radius=radius)

@router.get("/search/by-rectangle", summary="Получить компании в области")
async def get_in_rectangle(*, point: tuple[float, float], db: DBDep):
    return await CompaniesService(db).get_in_rectangle(point=point)

@router.get("/{company_id}", summary="Получить компанию по ID")
async def get_by_id(*, company_id: int, db: DBDep):
    return await CompaniesService(db).get_by_id(company_id=company_id)

@router.get("", summary="Получить компании по названию")
async def get_by_name(*, name: str, db: DBDep):
    return await CompaniesService(db).get_by_name(name=name)
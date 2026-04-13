from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.deps import DBDep, PagDep
from src.schemas.companies import CompaniesOutDTO
from src.services.activities import ActivitiesService

router = APIRouter()


@router.get(
    "/{activity_id}/companies",
    summary="Получить компании по виду деятельности",
    description="Возвращает организации, напрямую относящиеся к указанному виду деятельности"
)
@cache(expire=120)
async def get_by_activity(*, pagination: PagDep, activity_id: int, db: DBDep) -> list[CompaniesOutDTO]:
    return await ActivitiesService(db).get_by_activity(activity_id=activity_id, pagination=pagination)


@router.get(
    "/{activity_id}/companies/tree",
    summary="Получить компании относящиеся к виду деятельности",
    description="""Возвращает список организаций по указанному виду деятельности с учетом вложенности. В результат 
    включаются организации, связанные как с выбранной деятельностью, так и со всеми ее дочерними видами деятельности в 
    дереве"""
)
@cache(expire=180)
async def get_in_activity(*, pagination: PagDep, activity_id: int, db: DBDep) -> list[CompaniesOutDTO]:
    return await ActivitiesService(db).get_in_activity(activity_id=activity_id, pagination=pagination)

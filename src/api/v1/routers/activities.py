from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.deps import DBDep, PagDep
from src.services.activities import ActivitiesService

router = APIRouter()


@router.get("/{activity_id}/companies", summary="Получить компании по виду деятельности")
@cache(expire=120)
async def get_by_activity(*, pagination: PagDep, activity_id: int, db: DBDep):
    return await ActivitiesService(db).get_by_activity(activity_id=activity_id, pagination=pagination)


@router.get("/{activity_id}/companies/tree", summary="Получить компании относящиеся к виду деятельности")
@cache(expire=180)
async def get_in_activity(*, pagination: PagDep, activity_id: int, db: DBDep):
    return await ActivitiesService(db).get_in_activity(activity_id=activity_id, pagination=pagination)

from fastapi import APIRouter

from src.api.deps import DBDep
from src.services.activities import ActivitiesService

router = APIRouter()


@router.get("/{activity_id}/companies", summary="Получить компании по виду деятельности")
async def get_by_activity(*, activity_id: int, db: DBDep):
    return await ActivitiesService(db).get_by_activity(activity_id=activity_id)

@router.get("/{activity_id}/companies/tree", summary="Получить компании относящиеся к виду деятельности")
async def get_in_activity(*, activity_id: int, db: DBDep):
    return await ActivitiesService(db).get_in_activity(activity_id=activity_id)
from fastapi import APIRouter, Depends
from src.api.deps import verify_api_key
from src.api.v1.routers import companies, buildings, activities


api_v1_router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(verify_api_key)],
)

api_v1_router.include_router(companies.router, prefix="/companies", tags=["Поиск по компаниям"])
api_v1_router.include_router(buildings.router, prefix="/buildings", tags=["Поиск по зданиям"])
api_v1_router.include_router(activities.router, prefix="/activities", tags=["Поиск по деятельности"])
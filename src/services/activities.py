from src.services.base import BaseService


class ActivitiesService(BaseService):
    async def get_by_activity(self, *, activity_id: int):
        return await self.db.companies.get_by_activity(activity_id=activity_id)

    async def get_in_activity(self, *, activity_id: int):
        return await self.db.companies.get_in_activity(activity_id=activity_id)

from src.mappers.activities import ActivitiesMapper
from src.models import ActivitiesORM
from src.repositories.base import BaseRepo


class ActivitiesRepo(BaseRepo):
    model = ActivitiesORM
    mapper = ActivitiesMapper

from src.mappers.base import DataMapper
from src.models import ActivitiesORM
from src.schemas.activities import ActivitiesDTO


class ActivitiesMapper(DataMapper):
    db_model = ActivitiesORM
    schema = ActivitiesDTO
from src.mappers.base import DataMapper
from src.models import ActivitiesORM
from src.schemas.activities import ActivitiesDTO, ActivitiesOutDTO


class ActivitiesMapper(DataMapper):
    model_ORM = ActivitiesORM
    schema_in = ActivitiesDTO
    schema_out = ActivitiesOutDTO

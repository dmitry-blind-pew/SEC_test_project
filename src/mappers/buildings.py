from src.mappers.base import DataMapper
from src.models import BuildingsORM
from src.schemas.buildings import BuildingsDTO


class BuildingsMapper(DataMapper):
    db_model = BuildingsORM
    schema = BuildingsDTO
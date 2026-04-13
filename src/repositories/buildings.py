from src.mappers.buildings import BuildingsMapper
from src.models import BuildingsORM
from src.repositories.base import BaseRepo


class BuildingsRepo(BaseRepo):
    model = BuildingsORM
    mapper = BuildingsMapper

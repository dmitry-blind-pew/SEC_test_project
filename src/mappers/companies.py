from src.mappers.base import DataMapper
from src.models import CompaniesORM
from src.schemas.companies import CompaniesDTO


class CompaniesMapper(DataMapper):
    db_model = CompaniesORM
    schema = CompaniesDTO
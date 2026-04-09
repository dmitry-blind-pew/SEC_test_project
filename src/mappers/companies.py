from src.mappers.base import DataMapper
from src.models import CompaniesORM
from src.schemas.companies import CompaniesDTO, CompaniesOutDTO


class CompaniesMapper(DataMapper):
    model_ORM = CompaniesORM
    schema_in = CompaniesDTO
    schema_out = CompaniesOutDTO
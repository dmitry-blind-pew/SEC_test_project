from src.mappers.companies import CompaniesMapper
from src.models import CompaniesORM
from src.repositories.base import BaseRepo


class CompaniesRepo(BaseRepo):
    model = CompaniesORM
    mapper = CompaniesMapper
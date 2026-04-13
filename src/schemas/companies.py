from pydantic import BaseModel


class CompaniesDTO(BaseModel):
    name: str
    building_id: int


class CompaniesOutDTO(CompaniesDTO):
    id: int


class CompanyPhonesDTO(BaseModel):
    company_id: int
    phone: str

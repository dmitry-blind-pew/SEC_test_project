from pydantic import BaseModel, Field


class BuildingsDTO(BaseModel):
    address: str
    lon: float = Field(ge=-180, le=180)
    lat: float = Field(ge=-90, le=90)


class BuildingsOutDTO(BuildingsDTO):
    id: int

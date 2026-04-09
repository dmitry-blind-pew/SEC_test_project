from pydantic import BaseModel, Field


class BuildingsDTO(BaseModel):
    address: str
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
from pydantic import BaseModel


class ActivitiesDTO(BaseModel):
    name: str
    level: int
    parent_id: int | None = None


class ActivitiesOutDTO(ActivitiesDTO):
    id: int

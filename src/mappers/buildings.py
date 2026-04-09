from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape

from src.mappers.base import DataMapper
from src.models import BuildingsORM
from src.schemas.buildings import BuildingsDTO, BuildingsOutDTO


class BuildingsMapper(DataMapper):
    model_ORM = BuildingsORM
    schema_in = BuildingsDTO
    schema_out = BuildingsOutDTO

    @classmethod
    def map_to_persistence_entity(cls, schema_data: BuildingsDTO) -> BuildingsORM:
        data = schema_data.model_dump()
        lon = data.pop("lon")
        lat = data.pop("lat")
        data["location"] = WKTElement(f"POINT({lon} {lat})", srid=4326)
        return cls.model_ORM(**data)

    @classmethod
    def map_to_domain_entity(cls, model_data: BuildingsORM) -> BuildingsOutDTO:
        point = to_shape(model_data.location)
        return BuildingsOutDTO(
            id=model_data.id,
            address=model_data.address,
            lon=float(point.x),
            lat=float(point.y),
        )

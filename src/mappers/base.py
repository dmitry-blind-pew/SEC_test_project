from typing import TypeVar, Type, Generic
from pydantic import BaseModel

from src.models import BaseORM


ModelType = TypeVar("ModelType", bound=BaseORM)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper(Generic[ModelType, SchemaType]):
    model_ORM: Type[ModelType]
    schema_in: Type[SchemaType]
    schema_out: Type[SchemaType]

    @classmethod
    def map_to_persistence_entity(cls, schema_data: SchemaType) -> ModelType:
        return cls.model_ORM(**schema_data.model_dump())

    @classmethod
    def map_to_domain_entity(cls, model_data: ModelType) -> SchemaType:
        return cls.schema_out.model_validate(model_data, from_attributes=True)

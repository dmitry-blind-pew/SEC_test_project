import typing
from typing import List

from geoalchemy2 import Geography
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseORM

if typing.TYPE_CHECKING:
    from src.models import CompaniesORM


class BuildingsORM(BaseORM):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    location = mapped_column(
        Geography(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )

    companies: Mapped[List["CompaniesORM"]] = relationship(
        back_populates="building",
        cascade="all, delete-orphan",
    )

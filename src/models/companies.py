from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseORM


class CompaniesORM(BaseORM):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    building: Mapped["BuildingsORM"] = relationship(back_populates="companies")
    phones: Mapped[List["CompanyPhonesORM"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    activities: Mapped[List["ActivitiesORM"]] = relationship(
        secondary="companies_activities",
        back_populates="companies",
    )

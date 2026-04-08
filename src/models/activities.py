from typing import List, Optional

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseORM


class ActivitiesORM(BaseORM):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="level_between_1_and_3"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    level: Mapped[int] = mapped_column(nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    parent: Mapped[Optional["ActivitiesORM"]] = relationship(
        remote_side="ActivitiesORM.id",
        back_populates="children",
    )
    children: Mapped[List["ActivitiesORM"]] = relationship(back_populates="parent")
    companies: Mapped[List["CompaniesORM"]] = relationship(
        secondary="companies_activities",
        back_populates="activities",
    )

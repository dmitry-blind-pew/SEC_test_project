from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseORM


class CompaniesActivitiesORM(BaseORM):
    __tablename__ = "companies_activities"

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)


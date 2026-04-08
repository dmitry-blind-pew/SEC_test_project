from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseORM


class CompanyPhonesORM(BaseORM):
    __tablename__ = "company_phones"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    phone: Mapped[str] = mapped_column(String(32), nullable=False)

    company: Mapped["CompaniesORM"] = relationship(back_populates="phones")

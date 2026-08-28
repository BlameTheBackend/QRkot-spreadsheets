from datetime import datetime

from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy.orm import declared_attr, Mapped, mapped_column


class InvestmentMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)
    close_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None)

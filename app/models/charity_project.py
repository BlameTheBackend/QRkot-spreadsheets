from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.mixins import InvestmentMixin
from app.core.db import Base


class CharityProject(InvestmentMixin, Base):
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

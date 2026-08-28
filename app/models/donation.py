from sqlalchemy import Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.mixins import InvestmentMixin
from app.core.db import Base


class Donation(InvestmentMixin, Base):
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), name='fk_donation_user_id_user')

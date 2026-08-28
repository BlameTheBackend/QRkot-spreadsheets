from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.investable import CRUDInvestable
from app.models import Donation, User


class DonationCRUD(CRUDInvestable):
    async def get_by_user(
        self, session: AsyncSession, user: User
    ):
        reservations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return reservations.scalars().all()


donation_crud = DonationCRUD(Donation)

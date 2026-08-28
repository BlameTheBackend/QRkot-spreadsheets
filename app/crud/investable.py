from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase


class CRUDInvestable(CRUDBase):

    async def get_objs_for_investing(self, session: AsyncSession):
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date, self.model.id)
        )
        return result.scalars().all()

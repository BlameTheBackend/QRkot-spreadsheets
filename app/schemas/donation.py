from typing import Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt, ConfigDict, NonNegativeInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None

    model_config = ConfigDict(extra='forbid')


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationBase):
    id: int
    create_date: datetime
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime] = None
    user_id: int

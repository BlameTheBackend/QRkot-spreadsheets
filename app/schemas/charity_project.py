from typing import Optional
from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict, PositiveInt, NonNegativeInt

from app.constants import (
    MIN_CHARITY_PROJECT_NAME_LENGTH,
    MAX_CHARITY_PROJECT_NAME_LENGTH,
    MIN_CHARITY_PROJECT_DESCRIPTION_LENGTH
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_CHARITY_PROJECT_NAME_LENGTH,
        max_length=MAX_CHARITY_PROJECT_NAME_LENGTH
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_CHARITY_PROJECT_DESCRIPTION_LENGTH)
    full_amount: Optional[PositiveInt] = None

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        min_length=MIN_CHARITY_PROJECT_NAME_LENGTH,
        max_length=MAX_CHARITY_PROJECT_NAME_LENGTH
    )
    description: str = Field(
        min_length=MIN_CHARITY_PROJECT_DESCRIPTION_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

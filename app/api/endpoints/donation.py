from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.models import User
from app.crud import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationFullInfoDB
)
from app.services.investing import run_investing_process

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: SessionDep,
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        session: SessionDep,
        user: Annotated[User, Depends(current_user)]
):
    new_donation = await donation_crud.create(
        donation, session, user)
    new_donation = await run_investing_process(new_donation, session)
    return await donation_crud.save(new_donation, session)


@router.get(
    '/my', response_model=list[DonationDB],
)
async def get_my_reservations(
        session: SessionDep,
        user: Annotated[User, Depends(current_user)]
):
    reservations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return reservations

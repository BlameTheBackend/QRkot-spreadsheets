from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_exists,
    check_project_status_and_amount,
    check_project_amount_before_delete
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.crud.charity_project import charity_project_crud
from app.services.investing import run_investing_process


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: SessionDep
):
    charity_project = await charity_project_crud.get_multi(session)
    return charity_project


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await run_investing_process(new_project, session)
    return await charity_project_crud.save(new_project, session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep
):
    project = await check_project_exists(charity_project_id, session)
    await check_project_status_and_amount(
        project, session, obj_in.name, obj_in.full_amount
    )
    project = await charity_project_crud.update(project, obj_in, session)
    await run_investing_process(project, session)
    return await charity_project_crud.save(project, session)


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
    charity_project_id: int,
    session: SessionDep
):
    charity_project = await check_project_exists(charity_project_id, session)
    await check_project_amount_before_delete(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project

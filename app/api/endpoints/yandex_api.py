from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.services.yandex_api import create_simple_report
from app.core.yandex_client import get_yandex_client


router = APIRouter()


@router.post(
    "/report",
    response_model=str,
    dependencies=[Depends(current_superuser)],
)
async def create_report(
        session: AsyncSession = Depends(get_async_session),
        yandex_client=Depends(get_yandex_client),
) -> str:
    try:
        projects = await charity_project_crud.get_projects_by_completion_rate(
            session
        )
        if not projects:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Закрытых проектов нет",
            )
        public_url = await create_simple_report(
            projects=projects,
            client=yandex_client,
        )
        return public_url
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось создать отчёт: {e}",
        )

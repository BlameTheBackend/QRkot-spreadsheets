from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.investable import CRUDInvestable
from app.models import CharityProject


class CRUDCharityProject(CRUDInvestable):

    async def get_charity_project_id_by_name(
            self, project_name: str, session: AsyncSession) -> Optional[int]:
        db_project_id_result = await session.execute(
            select(CharityProject.id)
            .where(CharityProject.name == project_name))
        db_project_id = db_project_id_result.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        result = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(True),
                CharityProject.close_date.isnot(None)
            )
        )
        projects = list(result.scalars().all())

        def sort_key(project):
            time_to_collect = project.close_date - project.create_date
            return time_to_collect.total_seconds()
        projects.sort(key=sort_key)
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)

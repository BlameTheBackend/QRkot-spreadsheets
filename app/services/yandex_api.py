from datetime import datetime, timedelta, UTC
from io import BytesIO

import xlsxwriter

from app.core.config import settings
from app.constants import (
    MINUTES_IN_HOUR, MINUTES_IN_DAY, STREAM_START_POSITION
)


def format_time_delta(delta: timedelta) -> str:
    total_minutes = int(delta.total_seconds() / MINUTES_IN_HOUR)
    days = total_minutes // MINUTES_IN_DAY
    remaining_minutes = total_minutes % MINUTES_IN_DAY
    hours = remaining_minutes // MINUTES_IN_HOUR
    minutes = remaining_minutes % MINUTES_IN_HOUR
    if days > 0:
        return f"{days} дн. {hours} ч."
    return f"{hours} ч. {minutes} мин."


async def create_simple_report(client, projects) -> str:
    current_date = datetime.now(UTC)
    date_string = current_date.strftime(settings.report_format)
    file_name = f"report_{date_string}"
    upload_url, file_path = await client.create_excel_file(file_name)
    output = BytesIO()
    with xlsxwriter.Workbook(output) as workbook:
        worksheet = workbook.add_worksheet("Отчёт")
        title_format = workbook.add_format({
            "bold": True,
            "border": 1,
        })
        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#D9EAF7",
            "border": 1,
        })
        cell_format = workbook.add_format({
            "border": 1,
        })
        worksheet.merge_range(
            "A1:C1",
            f"Отчёт за {date_string}",
            title_format,
        )
        headers = [
            "Название проекта",
            "Время сбора",
            "Описание",
        ]
        for column, header in enumerate(headers):
            worksheet.write(1, column, header, header_format)
        row = 2
        for project in projects:
            collection_time = timedelta(0)
            if project.close_date and project.create_date:
                collection_time = project.close_date - project.create_date
            worksheet.write(row, 0, project.name, cell_format)
            worksheet.write(
                row,
                1,
                format_time_delta(collection_time),
                cell_format,
            )
            worksheet.write(row, 2, project.description, cell_format)
            row += 1
        worksheet.write(row, 0, "Итого", title_format)
        worksheet.write(row, 1, len(projects), title_format)
        worksheet.write(row, 2, "проектов", title_format)
        worksheet.set_column("A:A", 30)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 50)
    output.seek(STREAM_START_POSITION)
    await client.upload_file(
        upload_url,
        output.read(),
    )
    public_url = await client.publish_file(file_path)

    return public_url

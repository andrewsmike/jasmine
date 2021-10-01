"""
Load tasks to / from jasmine tracker google sheet.
"""
from app_base import sheets_handle
from tasks import Task

__all__ = [
    "gsheet_jasmine_tasks",
    "update_gsheet_jasmine_tasks",
]


# Unusual to hardcode this, but I think it's acceptable.
# There are limited security implications of a leaked google docs token.
JASMINE_TRACKER_SPREADSHEET_ID = "1XUCr5NQFgXra_i8AaGkDckqA0mRxL5Bztvj969viPks"


def gsheet_jasmine_tasks() -> list[Task]:
    task_rows = (
        sheets_handle()
        .values()
        .get(
            spreadsheetId=JASMINE_TRACKER_SPREADSHEET_ID,
            range="User Stories!A2:M",
        )
        .execute()
        .get("values", [])
    )

    return [Task.from_row(row) for row in task_rows if row and len(row) > 1 and row[1]]


def update_gsheet_jasmine_tasks(tasks: list[Task]):
    task_rows = [task.row() for task in tasks]

    sheets_handle().values().update(
        spreadsheetId=JASMINE_TRACKER_SPREADSHEET_ID,
        valueInputOption="USER_ENTERED",
        range="User Stories!A2:M",
        body={"values": task_rows},
    ).execute()

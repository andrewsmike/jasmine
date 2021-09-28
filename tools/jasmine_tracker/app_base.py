"""
Get an authorized handle to google sheets' API.
"""
from functools import cache

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools  # type: ignore

__all__ = [
    "sheets_handle",
]


SCOPES = "https://www.googleapis.com/auth/spreadsheets"


@cache
def sheets_handle():
    store = file.Storage("token.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = build("sheets", "v4", http=creds.authorize(Http()))

    # Call the Sheets API
    return service.spreadsheets()

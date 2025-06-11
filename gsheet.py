import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_NAME

def get_sheet_by_name(sheet_name: str) -> gspread.Spreadsheet:
    """
    Retrieve a Google Sheet by its name.

    :param sheet_name: The name of the Google Sheet to retrieve.
    :return: gspread.models.Spreadsheet object.
    """
    client = init_client()
    return client.open(sheet_name)

def init_client() -> gspread.Client:
    """
    Initialize the Google Sheets client using service account credentials.
    """
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    return client

def read_from_worksheet(worksheet_number: int = 0):
    """"
    Read data from a specific worksheet in the Google Sheet.
    :param worksheet_number: The index of the worksheet to read from (default is 0).
    """
    sheet = get_sheet_by_name(SPREADSHEET_NAME)
    worksheet = sheet.get_worksheet(worksheet_number)
    data = worksheet.get_all_records()

    for row in data:
        print(row)

if __name__ == "__main__":
    read_from_worksheet(0)
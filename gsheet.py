import gspread
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_NAME

def init_client() -> gspread.Client:
    """
    Initialize the Google Sheets client using service account credentials.

    :return: An authorized gspread.Client instance.
    """
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes) # This file should contain your service account credentials.
    client = gspread.authorize(creds)
    return client

def get_active_sheet() -> gspread.Spreadsheet:
    """
    Retrieve the active Google Sheet using the configured name.

    :return: gspread.models.Spreadsheet object.
    """
    client = init_client()
    return client.open(SPREADSHEET_NAME)

def read_from_worksheet(worksheet_number: int = 0) -> list[dict]:
    """
    Read data from a specific worksheet in the Google Sheet.

    :param worksheet_number: The index of the worksheet to read from (default is 0).
    :return: A list of rows as dictionaries.
    """
    sheet = get_active_sheet()
    worksheet = sheet.get_worksheet(worksheet_number)
    data = worksheet.get_all_records()
    return data

def get_or_create_worksheet(sheet: gspread.Spreadsheet, sheet_name: str, rows: int = 100, cols: int = 20) -> gspread.Worksheet:
    """
    Get the worksheet by name or create it if it doesn't exist.

    :param sheet: The spreadsheet object.
    :param sheet_name: The title of the worksheet.
    :param rows: Number of rows for the new worksheet if created.
    :param cols: Number of columns for the new worksheet if created.
    :return: A gspread.Worksheet object.
    """
    try:
        return sheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        return sheet.add_worksheet(title=sheet_name, rows=rows, cols=cols)

def write_to_worksheet(sheet_name: str, data: list[dict]) -> None:
    """
    Append rows to a specific worksheet, creating the worksheet if needed.

    :param sheet_name: The name of the worksheet (tab) to write to.
    :param data: A list of dictionaries representing rows to write.
    """
    sheet = get_active_sheet()
    worksheet = get_or_create_worksheet(sheet, sheet_name)

    if not data:
        return  # No data to write

    # Get the headers from the first dictionary
    headers = list(data[0].keys())

    # Ensure the worksheet has headers
    existing_data = worksheet.get_all_values()
    if not existing_data or not any(existing_data[0]):
        worksheet.append_row(headers)

    # Append each row of data
    for row in data:
        worksheet.append_row([row.get(header, "") for header in headers])

def print_data_from_worksheet(worksheet_number: int = 0) -> None:
    """
    Print data from a specific worksheet.

    :param worksheet_number: The index of the worksheet to read from (default is 0).
    """
    data = read_from_worksheet(worksheet_number)
    for row in data:
        print(row)

if __name__ == "__main__":
    write_to_worksheet("sample_people_data_1", [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ])
    # print_data_from_worksheet(1)
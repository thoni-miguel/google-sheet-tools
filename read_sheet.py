import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
client = gspread.authorize(creds)

sheet = client.open("sample_people_data").sheet1

records = sheet.get_all_records()

for row in records:
    print(row)
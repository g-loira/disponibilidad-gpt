from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/disponibilidad")
def leer_disponibilidad():
    SERVICE_ACCOUNT_FILE = 'credenciales.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    SPREADSHEET_ID = '1mJ5LIG5yTAsnoz13TYE9C1_tlT0JTZpHn-qjDCOCc5s'  # 👈 Tu ID real
    RANGE_NAME = 'DISPONIBILIDAD!A1:Z1000'

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    headers = values[0]
    data = [dict(zip(headers, row)) for row in values[1:]]

    return {"apartamentos": data}

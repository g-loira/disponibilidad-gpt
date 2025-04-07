from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/disponibilidad")
def leer_disponibilidad():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    SERVICE_ACCOUNT_INFO = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    creds = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO, scopes=SCOPES
    )

    SPREADSHEET_ID = '1mJ5LIG5yTAsnoz13TYE9C1_tlT0JTZpHn-qjDCOCc5s'
    RANGE_NAME = 'DISPONIBILIDAD!A1:Z1000'

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return {"apartamentos": []}

    headers = values[0]
    rows = values[1:]

    apartamentos = [
        {
            "nombre": r[headers.index("Propiedad")],
            "disponible": True,  # Aquí puedes adaptar más lógica si tienes un campo real
            "desde": r[headers.index("Available from")],
            "hasta": r[headers.index("MES")]
        }
        for r in rows
        if len(r) >= len(headers)
    ]

    return {"apartamentos": apartamentos}


# 👇 Necesario para que funcione en Railway
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api_disponibilidad:app", host="0.0.0.0", port=port)

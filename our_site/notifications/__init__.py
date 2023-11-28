from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import os


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
]
try:
    flow = InstalledAppFlow.from_client_secrets_file(os.environ["GOOGLE_API_SECRET_FILE"], SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
except KeyError:
    print("Environment variable 'GOOGLE_API_SECRET_FILE' must be set to send notification emails.")
    service = None

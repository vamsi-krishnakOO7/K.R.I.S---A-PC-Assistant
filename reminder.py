from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os.path
from ui import update_ui, resource_path
from plyer import notification


SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    token_path = resource_path('token.pickle')
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(resource_path('resources/credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

def display_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,  # Path to an .ico file if you have one; otherwise, this can be None
        timeout=10,  # Duration in seconds before the notification disappears
    )

def create_reminder(service, summary, description, start_time, end_time):
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 24 * 60}, {'method': 'popup', 'minutes': 10}]},
    }
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        update_ui(f"Reminder created: {event.get('htmlLink')}")
        display_notification("Reminder Created", f"{summary} at {start_time.strftime('%d-%m-%Y %H:%M')}")
    except Exception as e:
        update_ui(f"Failed to create a reminder: {e}")
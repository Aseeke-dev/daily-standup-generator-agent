import os.path
from datetime import datetime, timedelta, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_calender():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
    return creds

def fetch_calendar_events():
    creds = authenticate_calender()
    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.now(timezone.utc)
    yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    time_min = yesterday_start.isoformat()
    time_max = today_end.isoformat()
    
    print(f"Fetching calender events from {yesterday_start.date()} to {today_end.date()}...\n")
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    formatted_events = []
    if not events:
        return "No meetings found for yesterday or today."
        
    for event in events:
        if event.get('status') == 'cancelled':
            continue
            
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No Title')
        formatted_events.append(f"- {start}: {summary}")
        
    return "\n".join(formatted_events)

if __name__ == "__main__":
    print("Starting Google Calendar Fetch Tool...")
    events_summary = fetch_calendar_events()
    print("--- FETCHED EVENTS ---")
    print(events_summary)
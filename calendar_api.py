import datetime
from mimetypes import init
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
import os

# This module requires credentials.json to be in the same directory.

SCOPES = ["https://www.googleapis.com/auth/calendar.app.created"]

# Map color codes to Google Calendar color IDs
COLOR_MAP = {
    'C': '7',   # Cyan
    'Y': '5',   # Yellow
    'M': '3',   # Magenta
    'G': '10',  # Green
    'R': '11',  # Red
    'B': '9',   # Blue
    'O': '6',   # Orange
    '.': '8'    # Grey
}

def get_service() -> Resource:
    """
    initialises the service object for the Google Calendar API.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


service = None
calendar_id = None


def init_new_calendar(summary="Tetris Calendar", time_zone="Europe/London") -> None:
    body = {
        "summary": summary,
        "timeZone": time_zone
    }
    calendar = service.calendars().insert(body=body).execute()
    return calendar["id"]


def init_joystick() -> None:
    center_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    center_start_datetime += datetime.timedelta(days=2)
    center_start_datetime += datetime.timedelta(hours=10)
    create_event("Joystick", "C", center_start_datetime, center_start_datetime + datetime.timedelta(hours=1))


def init_gui() -> None:
    global service
    global calendar_id
    service = get_service()
    calendar_id = init_new_calendar()
    init_joystick()


def create_event(name: str, color: str, start: datetime.datetime, end: datetime.datetime) -> None:
    """
    Creates a Google Calendar event with the specified color, start, and end times.
    
    Args:
        color: Event color code (C=cyan, Y=yellow, M=magenta, G=green, R=red, B=blue, O=orange, .=grey)
        start: Start datetime for the event
        end: End datetime for the event
        calendar_id: Calendar ID to create the event in (default: 'primary')
    """
    
    # Validate color code
    if color not in COLOR_MAP:
        raise ValueError(f"Invalid color code '{color}'. Use one of: C, Y, M, G, R, B, O, .")
    
    # Convert datetime objects to ISO 8601 format with timezone
    # If timezone-naive, assume UTC
    if start.tzinfo is None:
        start = start.replace(tzinfo=datetime.timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=datetime.timezone.utc)
    
    start_iso = start.isoformat()
    end_iso = end.isoformat()
    
    # Get timezone string for Google Calendar API
    # Google Calendar API expects IANA timezone names like "UTC" or "America/Los_Angeles"
    def get_timezone_str(dt):
        if dt.tzinfo == datetime.timezone.utc:
            return "UTC"
        # Try to get timezone name from tzinfo
        tz_name = str(dt.tzinfo)
        # Check if it looks like an IANA timezone name (contains '/')
        if '/' in tz_name:
            return tz_name
        # For offset-based timezones, default to UTC
        # Users should use zoneinfo or pytz for proper timezone names
        return "UTC"
    
    timezone_str = get_timezone_str(start)
    
    # Create event body
    event_body = {
        'summary': name,
        'start': {
            'dateTime': start_iso,
            'timeZone': timezone_str
        },
        'end': {
            'dateTime': end_iso,
            'timeZone': timezone_str
        },
        'colorId': COLOR_MAP[color]
    }
    
    # Insert the event into the calendar
    try:
        event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
        return event
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise


def edit_event(event_id: str, color: str) -> None:
    """
    Edits the event with the given ID to the given color.
    """
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    event["colorId"] = COLOR_MAP[color]
    service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()


def set_grid(grid: list[list[str]]) -> list[str]:
    """
    Sets the grid in the calendar for the given date.
    Returns a list of event IDs.

    Args:
        calendar_id: Calendar ID to create the events in
        grid: 24 x 10 grid of strings
        names: 24 x 10 grid of strings

    Returns:
        List of event IDs
    """
    date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    event_ids = []
    for y in range(24):
        for x in range(10):
            event = create_event(chr(ord('A') + x), grid[y][x], date + datetime.timedelta(hours=y), date + datetime.timedelta(hours=y+1))
            event_ids.append(event["id"])
    return event_ids


def update_grid(previous_grid: list[list[str]], previous_grid_event_ids: list[str], new_grid: list[list[str]]) -> None:
    """
    Updates the grid in the calendar for the given date.

    Args:
        previous_grid: 24 x 10 grid of strings
        previous_grid_event_ids: List of event IDs in the previous grid
        new_grid: 24 x 10 grid of strings
        date: Date to create the events for
    """
    for y in range(24):
        for x in range(10):
            print(f"Checking {y},{x}: {previous_grid[y][x]} != {new_grid[y][x]}")
            if previous_grid[y][x] != new_grid[y][x]:
                edit_event(calendar_id, previous_grid_event_ids[y * 10 + x], new_grid[y][x])


def check_joystick() -> int:
    """
    Checks the joystick and returns the following:
    0: No change
    1: Left
    2: Right
    3: Up
    4: Down
    """
    center_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    center_start_datetime += datetime.timedelta(days=2)
    center_start_datetime += datetime.timedelta(hours=10)
    
    # Ensure timezone-aware datetime for API call
    if center_start_datetime.tzinfo is None:
        center_start_datetime = center_start_datetime.replace(tzinfo=datetime.timezone.utc)

    time_min = (center_start_datetime - datetime.timedelta(days=1)).isoformat()
    time_max = (center_start_datetime + datetime.timedelta(days=2)).isoformat()

    events = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max
    ).execute()
    for event in events["items"]:
        event_start_datetime = datetime.datetime.fromisoformat(event["start"]["dateTime"])
        if event_start_datetime.date() == center_start_datetime.date() - datetime.timedelta(days=1):
            # Left
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 1
        elif event_start_datetime.date() == center_start_datetime.date() + datetime.timedelta(days=1):
            # Right
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 2
        elif event_start_datetime.date() == center_start_datetime.date() and event_start_datetime < center_start_datetime:
            # Up
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 3
        elif event_start_datetime.date() == center_start_datetime.date() and event_start_datetime > center_start_datetime:
            # Down
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 4
    return 0
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from googleapiclient.http import BatchHttpRequest
import os
from playwright.sync_api import sync_playwright

# This module requires credentials.json to be in the same directory.

SCOPES = ["https://www.googleapis.com/auth/calendar.app.created"]

# Browser control variables
_browser_context = None
_page = None

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
event_ids = []


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


def init_gui(newGame) -> None:
    global service
    global calendar_id
    global event_ids
    service = get_service()

    if newGame:
        calendar_id = init_new_calendar()
        #write to file
        with open("calendar_id.txt", "w") as file:
            file.write(calendar_id)

        event_ids = set_grid([['.'] * 10 for _ in range(24)])
        #write to file
        with open("event_ids.txt", "w") as file:
            file.write("\n".join(event_ids))
    
    else:
        #read from file
        with open("calendar_id.txt", "r") as file:
            calendar_id = file.read().strip()

        with open("event_ids.txt", "r") as file:
            event_ids = file.read().strip().split("\n")

    #print(f"Calendar ID: {calendar_id}")
    #print(f"Event IDs: {event_ids}")

    init_joystick()
    InitBrowser()


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
    Updates the grid in the calendar for the given date using batch requests.

    Args:
        previous_grid: 24 x 10 grid of strings
        previous_grid_event_ids: List of event IDs in the previous grid
        new_grid: 24 x 10 grid of strings
    """
    # Create a callback function for batch responses
    batch_results = []
    
    def BatchCallback(request_id, response, exception):
        if exception is not None:
            batch_results.append(("error", request_id, exception))
        else:
            batch_results.append(("success", request_id, response))
    
    # Create batch request
    batch = service.new_batch_http_request(callback=BatchCallback)
    
    # Collect all events that need updating
    events_to_fetch = {}
    cells_to_update = []
    
    for y in range(24):
        for x in range(10):
            if previous_grid[y][x] != new_grid[y][x]:
                event_id = previous_grid_event_ids[y * 10 + x]
                cells_to_update.append((y, x, event_id, new_grid[y][x]))
                # Only fetch each unique event once
                if event_id not in events_to_fetch:
                    events_to_fetch[event_id] = None
    
    # Fetch all events first (can't batch get requests efficiently, so do individually)
    for event_id in events_to_fetch.keys():
        events_to_fetch[event_id] = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    
    # Add all update requests to batch
    for y, x, event_id, new_color in cells_to_update:
        event = events_to_fetch[event_id].copy()
        event["colorId"] = COLOR_MAP[new_color]
        batch.add(service.events().update(calendarId=calendar_id, eventId=event_id, body=event))
    
    # Execute batch request
    if len(cells_to_update) > 0:
        batch.execute()
        # Refresh browser to show updates immediately
        RefreshBrowser()


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


def InitBrowser():
    """
    Connects to an existing Chrome browser that was launched with remote debugging.
    Chrome must be started with: chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
    
    On macOS: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
    On Linux: google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
    On Windows: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\Temp\\chrome-debug"
    """
    global _browser_context, _page
    try:
        playwright = sync_playwright().start()
        
        # Connect to existing browser on port 9222
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        contexts = browser.contexts
        if contexts:
            _browser_context = contexts[0]
            pages = _browser_context.pages
            _page = pages[0] if pages else None
            print("Connected to existing Chrome browser")
        else:
            print("Warning: No browser contexts found")
    except ImportError:
        print("Warning: Playwright not installed. Browser refresh disabled.")
    except Exception as e:
        print(f"Warning: Could not connect to browser: {e}")


def RefreshBrowser():
    """
    Refreshes the currently open page in the browser.
    """
    global _page
    if _page:
        try:
            _page.reload(wait_until="load")
        except Exception as e:
            print(f"Warning: Could not refresh browser: {e}")


def init_emotes():
    center_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    center_start_datetime += datetime.timedelta(days=2)
    center_start_datetime += datetime.timedelta(hours=15)
    create_event("Test Emote", "Y", center_start_datetime, center_start_datetime + datetime.timedelta(hours=1))

def check_emotes():
    # define emote cell
    center_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    emote_cell = center_start_datetime + datetime.timedelta(days=3)
    emote_cell = emote_cell + datetime.timedelta(hours=15)

    time_min = emote_cell
    time_max = emote_cell + datetime.timedelta(hours=1)

    # pull events data from emote cell
    events_data = service.events().list(
        calendar_id,
        timeMin = time_min,
        timeMax = time_max,
    ).execute()

    events = events_data.get(['items'])
    # play emote if is any emote event and reset afterwards, or ignore if is a random event

init_gui(False)
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from googleapiclient.http import BatchHttpRequest
import os

# This module requires credentials.json to be in the same directory.

SCOPES = ["https://www.googleapis.com/auth/calendar.app.created"]

# Browser control variables
_browser_context = None
_page = None
_playwright_available = False

# Try to import playwright
try:
    from playwright.sync_api import sync_playwright
    _playwright_available = True
except ImportError:
    pass

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

# Reverse map: Google Calendar color IDs to color codes
REVERSE_COLOR_MAP = {v: k for k, v in COLOR_MAP.items()}

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
score_event_id = None
joystick_event_id = None
emote_event_id = None


def init_new_calendar(summary="Tetris Calendar", time_zone="Europe/London") -> None:
    body = {
        "summary": summary,
        "timeZone": time_zone
    }
    calendar = service.calendars().insert(body=body).execute()
    return calendar["id"]


def init_joystick() -> None:
    global joystick_event_id
    
    joystick_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    joystick_start_datetime += datetime.timedelta(days=2)
    joystick_start_datetime += datetime.timedelta(hours=10)
    
    # Ensure timezone-aware datetime for API call
    if joystick_start_datetime.tzinfo is None:
        joystick_start_datetime = joystick_start_datetime.replace(tzinfo=datetime.timezone.utc)
    
    # First, check if joystick_event_id exists and get its current position
    if joystick_event_id:
        try:
            existing_event = service.events().get(calendarId=calendar_id, eventId=joystick_event_id).execute()
            existing_start = datetime.datetime.fromisoformat(existing_event["start"]["dateTime"])
            
            # Check if the existing event is at the correct center position
            if existing_start.date() == joystick_start_datetime.date() and \
               abs((existing_start - joystick_start_datetime).total_seconds()) < 60:  # Within 1 minute (exact position)
                # Already at the correct position, no need to do anything
                return
            else:
                # Event exists but is at wrong position - move it back to center
                existing_event["start"]["dateTime"] = joystick_start_datetime.isoformat()
                existing_event["end"]["dateTime"] = (joystick_start_datetime + datetime.timedelta(hours=1)).isoformat()
                service.events().update(calendarId=calendar_id, eventId=joystick_event_id, body=existing_event).execute()
                with open("log.txt", "a") as file:
                    file.write(f"Reset joystick event {joystick_event_id} back to center\n")
                return
        except HttpError:
            # Event doesn't exist or was deleted, will search for it or create new one below
            joystick_event_id = None
    
    # Search for joystick event in a wide time range (it might have been moved left/right/up/down)
    time_min = (joystick_start_datetime - datetime.timedelta(days=2)).isoformat()
    time_max = (joystick_start_datetime + datetime.timedelta(days=3)).isoformat()
    
    events = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max
    ).execute()
    
    # Look for existing "Joystick" events - prioritize finding it at center, but also find it if moved
    found_joystick_at_center = None
    found_joystick_moved = None
    
    for event in events["items"]:
        if event.get("summary") == "Joystick":
            event_start_datetime = datetime.datetime.fromisoformat(event["start"]["dateTime"])
            # If we find an existing joystick event at the expected time, reuse it
            if event_start_datetime.date() == joystick_start_datetime.date() and \
               abs((event_start_datetime - joystick_start_datetime).total_seconds()) < 60:  # Within 1 minute (exact position)
                found_joystick_at_center = event
            else:
                # Found a joystick event but it's been moved
                found_joystick_moved = event
    
    # If found at center, use it
    if found_joystick_at_center:
        joystick_event_id = found_joystick_at_center["id"]
        return
    
    # If found but moved, move it back to center
    if found_joystick_moved:
        joystick_event_id = found_joystick_moved["id"]
        found_joystick_moved["start"]["dateTime"] = joystick_start_datetime.isoformat()
        found_joystick_moved["end"]["dateTime"] = (joystick_start_datetime + datetime.timedelta(hours=1)).isoformat()
        service.events().update(calendarId=calendar_id, eventId=joystick_event_id, body=found_joystick_moved).execute()
        with open("log.txt", "a") as file:
            file.write(f"Found and reset moved joystick event {joystick_event_id} back to center\n")
        return
    
    # No existing joystick event found, create a new one
    joystick_event_id = create_event("Joystick", "C", joystick_start_datetime, joystick_start_datetime + datetime.timedelta(hours=1))
    with open("log.txt", "a") as file:
        file.write(f"Created new joystick event: {joystick_event_id}\n")
        file.write(f"Joystick start datetime: {joystick_start_datetime}\n")

def init_selection_joystick() -> None:
    center_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    center_start_datetime += datetime.timedelta(days=2)
    center_start_datetime += datetime.timedelta(hours=10)
    create_event("Select Game: Left - Tetris, Right - Pong", "C", center_start_datetime, center_start_datetime + datetime.timedelta(hours=1))


def init_gui(newGame, game: str) -> None:
    global service
    global calendar_id
    global event_ids
    global score_event_id
    global emote_event_id
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
        
        score_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        score_start_datetime += datetime.timedelta(days=2)
        score_start_datetime += datetime.timedelta(hours=2)
        #write to file
        score_event_id = create_event("Score: 0", "G", score_start_datetime, score_start_datetime + datetime.timedelta(hours=1))
        print(score_event_id)
        with open("score_event_id.txt", "w") as file:
            file.write(score_event_id)
    
    else:
        #read from file
        with open("calendar_id.txt", "r") as file:
            calendar_id = file.read().strip()

        with open("event_ids.txt", "r") as file:
            event_ids = file.read().strip().split("\n")
        previous_grid = get_grid()
        update_grid(previous_grid, [['.'] * 10 for _ in range(24)])

        with open("score_event_id.txt", "r") as file:
            score_event_id = file.read().strip()
        
        try:
            with open("emote_event_id.txt", "r") as file:
                emote_event_id = file.read().strip()
                # If file exists but is empty, treat as None
                if not emote_event_id:
                    emote_event_id = None
        except FileNotFoundError:
            emote_event_id = None
        
        update_score(0)

    #print(f"Calendar ID: {calendar_id}")
    #print(f"Event IDs: {event_ids}")
    if (game == "tetris"):
        init_joystick()
        init_emotes()
    elif (game == "pong"):
        init_joystick_pong(3)
    elif game == "selection":
        init_selection_joystick()
    InitBrowser()


def create_event(name: str, color: str, start: datetime.datetime, end: datetime.datetime) -> str:
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
        return event["id"]
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
            event_id = create_event(chr(ord('A') + x), grid[y][x], date + datetime.timedelta(hours=y), date + datetime.timedelta(hours=y+1))
            event_ids.append(event_id)
    return event_ids


def get_grid() -> list[list[str]]:
    """
    Gets the grid from the calendar based on event_ids using batch requests.
    Returns a 24 x 10 grid of color codes.

    Returns:
        24 x 10 grid of strings (color codes)
    """
    # Create a mapping from event_id to (y, x) position
    event_id_to_position = {}
    for y in range(24):
        for x in range(10):
            event_id = event_ids[y * 10 + x]
            event_id_to_position[event_id] = (y, x)
    
    # Create a callback function for batch responses
    batch_results = {}
    
    def BatchCallback(request_id, response, exception):
        if exception is not None:
            batch_results[request_id] = ("error", exception, None)
        else:
            event_id = response.get("id")
            batch_results[request_id] = ("success", response, event_id)
    
    # Create batch request
    batch = service.new_batch_http_request(callback=BatchCallback)
    
    # Add all get requests to batch
    for y in range(24):
        for x in range(10):
            event_id = event_ids[y * 10 + x]
            request = service.events().get(calendarId=calendar_id, eventId=event_id)
            batch.add(request)
    
    # Execute batch request
    batch.execute()
    
    # Build grid from batch results
    grid = [['.'] * 10 for _ in range(24)]
    
    for request_id, (status, result, event_id) in batch_results.items():
        if event_id and event_id in event_id_to_position:
            y, x = event_id_to_position[event_id]
            if status == "success":
                event = result
                color_id = event.get("colorId", "8")  # Default to grey if no colorId
                color_code = REVERSE_COLOR_MAP.get(color_id, ".")  # Default to '.' if unknown colorId
                grid[y][x] = color_code
            else:
                # On error, leave as default '.' (grey)
                grid[y][x] = '.'
    
    return grid


def update_grid(previous_grid: list[list[str]], new_grid: list[list[str]]) -> None:
    """
    Updates the grid in the calendar for the given date using batch requests.   

    Args:
        previous_grid: 24 x 10 grid of strings
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
                event_id = event_ids[y * 10 + x]
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

        #time.sleep(3)
        # Refresh browser to show updates immediately
        RefreshBrowser()

def update_score(score: int) -> None:
    """
    Updates the score in the calendar.
    """
    event = service.events().get(calendarId=calendar_id, eventId=score_event_id).execute()
    event["summary"] = f"Score: {score}"
    service.events().update(calendarId=calendar_id, eventId=score_event_id, body=event).execute()
    RefreshBrowser()


def check_joystick_pong() -> int:
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
    center_start_datetime += datetime.timedelta(hours=3)
    centre_start_datetime2 = center_start_datetime + datetime.timedelta(hours = 17)
    
    # Ensure timezone-aware datetime for API call
    if center_start_datetime.tzinfo is None:
        center_start_datetime = center_start_datetime.replace(tzinfo=datetime.timezone.utc)

    if centre_start_datetime2.tzinfo is None:
        centre_start_datetime2 = centre_start_datetime2.replace(tzinfo=datetime.timezone.utc)

    time_min = (center_start_datetime - datetime.timedelta(days=1)).isoformat()
    time_max = (center_start_datetime + datetime.timedelta(days=2)).isoformat()

    
    events = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max
    ).execute()
    for event in events["items"]:
        event_start_datetime = datetime.datetime.fromisoformat(event["start"]["dateTime"])
        if event_start_datetime.date() == centre_start_datetime2.date() - datetime.timedelta(days=1) and event_start_datetime.time().hour > 12:
            # Left
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 3
        elif event_start_datetime.date() == center_start_datetime.date() - datetime.timedelta(days=1) and event_start_datetime.time().hour < 12:
            # Left
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 1
        elif event_start_datetime.date() == centre_start_datetime2.date() + datetime.timedelta(days=1) and event_start_datetime.time().hour > 12:
            # Right
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 4
        elif event_start_datetime.date() == center_start_datetime.date() + datetime.timedelta(days=1) and event_start_datetime.time().hour < 12:
            # Right
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 2
    return 0

def init_joystick_pong(cont: int):
    center_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    center_start_datetime += datetime.timedelta(days=2)
    center_start_datetime += datetime.timedelta(hours=3)
    if cont == 1:
        create_event("Joystick", "C", center_start_datetime, center_start_datetime + datetime.timedelta(hours=1))
    elif cont == 2:
        center_start_datetime += datetime.timedelta(hours = 17)
        create_event("Joystick", "C", center_start_datetime, center_start_datetime + datetime.timedelta(hours=1))
    elif cont == 3:
        create_event("Joystick", "C", center_start_datetime, center_start_datetime + datetime.timedelta(hours=1))
        center_start_datetime += datetime.timedelta(hours = 17)
        create_event("Joystick", "C", center_start_datetime, center_start_datetime + datetime.timedelta(hours=1))


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
            # If this is the joystick event itself, we'll reset it in init_joystick(), don't delete it
            if event["id"] == joystick_event_id:
                return 1
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 1
        elif event_start_datetime.date() == center_start_datetime.date() + datetime.timedelta(days=1) and event["id"] != score_event_id and event["id"] != emote_event_id:
            # Right
            # If this is the joystick event itself, we'll reset it in init_joystick(), don't delete it
            if event["id"] == joystick_event_id:
                return 2
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return 2
        elif event_start_datetime.date() == center_start_datetime.date() and event_start_datetime < center_start_datetime and event["id"] != score_event_id and event["id"] != emote_event_id:
            # Up
            # If this is the joystick event itself, we'll reset it in init_joystick(), don't delete it
            if event["id"] == joystick_event_id:
                service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
                return 3
        elif event_start_datetime.date() == center_start_datetime.date() and event_start_datetime > center_start_datetime and event["id"] != score_event_id and event["id"] != emote_event_id:
            # Down
            # If this is the joystick event itself, we'll reset it in init_joystick(), don't delete it
            if event["id"] == joystick_event_id:
                service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
                return 4
            return 4
    return 0


def check_selection_joystick() -> str:
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
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return "tetris"
        elif event_start_datetime == center_start_datetime + datetime.timedelta(days=1):
            service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
            return "pong"
    return ""


def InitBrowser():
    """
    Connects to an existing Chrome browser that was launched with remote debugging.
    Chrome must be started with: chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
    
    On macOS: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
    On Linux: google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
    On Windows: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\Temp\\chrome-debug"
    """
    global _browser_context, _page, _playwright_available
    if not _playwright_available:
        print("Info: Playwright not installed. Browser refresh disabled.")
        return
    
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
    except Exception as e:
        print(f"Warning: Could not connect to browser: {e}")


def RefreshBrowser():
    """
    Refreshes the currently open page in the browser.
    """
    global _page
    if _page:
        try:
            print("Refreshing browser")
            _page.reload()
        except Exception as e:
            print(f"Warning: Could not refresh browser: {e}")

def init_emotes():
    global emote_event_id
    
    emote_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    emote_start_datetime += datetime.timedelta(days=2)
    emote_start_datetime += datetime.timedelta(hours=15)
    
    # Ensure timezone-aware datetime for API call
    if emote_start_datetime.tzinfo is None:
        emote_start_datetime = emote_start_datetime.replace(tzinfo=datetime.timezone.utc)
    
    # Always create a new emote button each game
    emote_event_id = create_event("Rage 😡", "M", emote_start_datetime, emote_start_datetime + datetime.timedelta(hours=1))
    # Write to file to persist the ID
    with open("emote_event_id.txt", "w") as file:
        file.write(emote_event_id)

def check_emotes():
    #emote selection
    emotes = []

    # define emote cell
    center_start_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    emote_cell = center_start_datetime + datetime.timedelta(days=3)
    emote_cell = emote_cell + datetime.timedelta(hours=15)
    
    # Ensure timezone-aware datetime for API call
    if emote_cell.tzinfo is None:
        emote_cell = emote_cell.replace(tzinfo=datetime.timezone.utc)

    time_min = emote_cell.isoformat()
    time_max = (emote_cell + datetime.timedelta(hours=1)).isoformat()

    # pull events data from emote cell
    events = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max
    ).execute()

    #define play emote function
    def play_emote(emote):
        print("playing some sort of emote")
        # Create an event at datetime.now().replace(hour=0, minute=0, second=0) + 2 days + 20 hours
        emote_datetime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        emote_datetime += datetime.timedelta(days=2)
        emote_datetime += datetime.timedelta(hours=20)
        create_event("🤬", "M", emote_datetime, emote_datetime + datetime.timedelta(hours=1))

    emote_chosen = events.get('items', [])
    
    # play emote if is any emote event, or ignore if is a random event
    if emote_chosen:
        for emote in emote_chosen:
            
            #### play the emote
            play_emote(emote)
            
            # delete emote
            service.events().delete(calendarId=calendar_id, eventId=emote["id"]).execute()
            init_emotes()

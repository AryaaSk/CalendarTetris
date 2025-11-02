# CalendarTetris

Games (Tetris and Pong) played through Google Calendar. Game state is displayed as calendar events, and controls work by moving events in the calendar.

## Concept

- Game state displayed as colored calendar events in a grid
- Controls: move calendar events to control the game
- Optional browser refresh using Playwright

## Games

### Tetris
- Tetris displayed as a 24x10 grid of calendar events
- Each cell is a colored calendar event
- Score tracked as a calendar event

### Pong
- Pong with dual joystick control
- Two paddles controlled by moving joystick events

## Requirements

- Python 3.13+
- Google Calendar API credentials
- Chrome browser (optional, for auto-refresh)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright (optional, for browser refresh):
```bash
playwright install chromium
```

3. Google Calendar API setup:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create credentials (OAuth 2.0 Client ID)
   - Download the credentials file and save it as `credentials.json` in the project root

4. Run the game:
```bash
python game.py
```

On first run, authenticate with Google. A `token.json` file will be created.

5. Chrome browser setup (optional, for auto-refresh):

To enable automatic browser refresh, launch Chrome with remote debugging:

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
```

**Linux:**
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
```

**Windows:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Temp\chrome-debug"
```

Then open your calendar in that Chrome window.

## How to Play

Start the game:
```bash
python game.py
```

Select a game by moving the selection event in the calendar.

### Tetris

- Move selection joystick event left (past dates) to select Tetris
- Control with joystick event:
  - Left: move event to previous day
  - Right: move event to next day
  - Up: move event earlier in same day
  - Down: move event later in same day

### Pong

- Move selection joystick event right (future dates) to select Pong
- Two joystick events control the paddles

## Project Structure

- `game.py` - Main game launcher
- `calendar_api.py` - Google Calendar API integration
- `tetris.py` - Tetris game logic
- `pong.py` - Pong game logic
- `credentials.json` - Google API credentials (not in repo)
- `token.json` - OAuth token (generated on first run)
- `calendar_id.txt` - Calendar ID
- `event_ids.txt` - Grid event IDs
- `score_event_id.txt` - Score event ID
- `emote_event_id.txt` - Emote button event ID
- `log.txt` - Application logs

## Calendar Event Mapping

Colors:
- `C` - Cyan (color 7)
- `Y` - Yellow (color 5)
- `M` - Magenta (color 3)
- `G` - Green (color 10)
- `R` - Red (color 11)
- `B` - Blue (color 9)
- `O` - Orange (color 6)
- `.` - Grey (color 8)

Tetris grid: 24 rows × 10 columns of calendar events

Control events:
- Joystick: cyan event for controls
- Score: green event showing score
- Emote button: magenta event
- Selection: event for game selection

## Troubleshooting

Authentication issues:
- Delete `token.json` and re-authenticate
- Ensure `credentials.json` is in project root
- Verify Calendar API is enabled in Google Cloud Console

Events not appearing:
- Check calendar write permissions
- Verify calendar ID in `calendar_id.txt`
- Check `log.txt` for errors

Browser refresh not working:
- Ensure Chrome launched with remote debugging flags
- Check Playwright is installed: `playwright install chromium`
- Browser refresh is optional

Controls not responding:
- Verify joystick events are in correct time range
- Check events are being moved in calendar
- Review `log.txt` for errors

## Development

To add a new game:
1. Create game file (e.g., `snake.py`)
2. Import functions from `calendar_api.py`
3. Use `update_grid()` for display updates
4. Use `check_joystick()` or custom control logic
5. Add game selection in `game.py`

Key API functions:
- `init_gui(newGame, game)` - Initialize calendar interface
- `update_grid(previous, new)` - Update grid display
- `check_joystick()` - Detect joystick movement
- `update_score(score)` - Update score event
- `create_event(name, color, start, end)` - Create event
- `delete_all_future_events()` - Clean up calendar

## Notes

- Events must be moved manually in Google Calendar
- Game state persists across sessions
- Future events are cleaned up on game start
- Do not commit `credentials.json` or `token.json`


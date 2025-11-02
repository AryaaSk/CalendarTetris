# CalendarTetris 🎮📅

A unique gaming experience where classic games (Tetris and Pong) are played entirely through Google Calendar! Control the games by moving calendar events, and watch the game state update in real-time on your calendar.

## 🎯 Concept

This project turns Google Calendar into a gaming interface:
- **Game State**: Displayed as colored calendar events in a grid
- **Controls**: Move calendar events to control the game (joystick, game selection, emotes)
- **Visual Feedback**: Real-time updates reflected directly in your Google Calendar
- **Browser Integration**: Optional automatic browser refresh using Playwright

## 🎮 Games

### Tetris
- Classic Tetris gameplay displayed as a 24x10 grid of calendar events
- Each cell is represented by a colored calendar event
- Clear lines, rack up points, and watch your score update as a calendar event
- Emote system for expressing reactions

### Pong
- Classic Pong gameplay with dual joystick control
- Two paddles controlled by moving joystick events in the calendar

## 🚀 Features

- **Calendar-Based Interface**: All game elements are calendar events
- **Game Selection**: Choose between Tetris and Pong via calendar navigation
- **Real-Time Updates**: Game state syncs automatically with Google Calendar
- **Score Tracking**: Score displayed as a calendar event
- **Emote System**: React to gameplay with calendar-based emotes
- **Auto-Refresh**: Optional browser refresh to see updates immediately
- **Joystick Control**: Move joystick events to control games
- **Color-Coded Grid**: Visual representation using Google Calendar color system

## 📋 Requirements

- Python 3.13+
- Google Calendar API credentials
- Chrome browser (for optional auto-refresh feature)

## 🔧 Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CalendarTetris
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Optional: For browser auto-refresh functionality:
```bash
playwright install chromium
```

### 3. Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials file and save it as `credentials.json` in the project root

### 4. First-Time Authentication

Run the game for the first time:

```bash
python game.py
```

On first run, you'll be prompted to:
- Authenticate with Google
- Grant calendar permissions
- A `token.json` file will be created for future sessions

### 5. Optional: Chrome Browser Setup (for auto-refresh)

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

## 🎮 How to Play

### Starting the Game

```bash
python game.py
```

The game launcher will:
1. Initialize the calendar interface
2. Show a game selection screen in the calendar
3. Wait for you to select a game by moving the selection event

### Playing Tetris

1. **Select Game**: Move the selection joystick event to the left (past dates) to select Tetris
2. **Control**: Move the joystick event in the calendar to control the falling piece:
   - **Left**: Move event to previous day
   - **Right**: Move event to next day
   - **Up**: Move event earlier in the same day
   - **Down**: Move event later in the same day
3. **Watch**: The game state updates automatically in the calendar grid
4. **Score**: Your score appears as a calendar event
5. **Emotes**: Move the emote button event to trigger reactions

### Playing Pong

1. **Select Game**: Move the selection joystick event to the right (future dates) to select Pong
2. **Control**: Two joystick events control the paddles
3. **Gameplay**: Move joysticks left/right to move paddles up/down

## 📁 Project Structure

```
CalendarTetris/
├── game.py              # Main game launcher
├── calendar_api.py      # Google Calendar API integration
├── tetris.py            # Tetris game logic
├── pong.py              # Pong game logic
├── requirements.txt     # Python dependencies
├── credentials.json     # Google API credentials (not in repo)
├── token.json          # OAuth token (generated on first run)
├── calendar_id.txt     # Stores calendar ID
├── event_ids.txt       # Stores grid event IDs
├── score_event_id.txt  # Stores score event ID
├── emote_event_id.txt  # Stores emote button event ID
└── log.txt             # Application logs
```

## 🎨 Calendar Event Mapping

### Colors
- `C` - Cyan (event color 7)
- `Y` - Yellow (event color 5)
- `M` - Magenta (event color 3)
- `G` - Green (event color 10)
- `R` - Red (event color 11)
- `B` - Blue (event color 9)
- `O` - Orange (event color 6)
- `.` - Grey (event color 8)

### Game Grid
- **Tetris Grid**: 24 rows × 10 columns of calendar events
- Each cell corresponds to one calendar event
- Events are positioned at specific times to form the grid

### Control Events
- **Joystick**: Cyan event that you move to control the game
- **Score**: Green event showing current score
- **Emote Button**: Magenta event to trigger emotes
- **Selection**: Event to choose between games

## 🔍 Troubleshooting

### Authentication Issues
- Delete `token.json` and re-authenticate
- Ensure `credentials.json` is in the project root
- Check that Calendar API is enabled in Google Cloud Console

### Events Not Appearing
- Check that you have calendar write permissions
- Verify the calendar ID in `calendar_id.txt`
- Check `log.txt` for error messages

### Browser Refresh Not Working
- Ensure Chrome is launched with remote debugging flags
- Check that Playwright is installed: `playwright install chromium`
- Browser refresh is optional - game works without it

### Game Controls Not Responding
- Verify joystick events are in the correct time range
- Check that events are being moved in the calendar
- Review `log.txt` for joystick detection errors

## 🛠️ Development

### Adding a New Game

1. Create a new game file (e.g., `snake.py`)
2. Import necessary functions from `calendar_api.py`
3. Use `update_grid()` to update the calendar display
4. Use `check_joystick()` or create custom control logic
5. Add game selection in `game.py`

### Calendar API Functions

Key functions in `calendar_api.py`:
- `init_gui(newGame, game)`: Initialize calendar interface
- `update_grid(previous, new)`: Update game grid display
- `check_joystick()`: Detect joystick movement
- `update_score(score)`: Update score event
- `create_event(name, color, start, end)`: Create calendar event
- `delete_all_future_events()`: Clean up calendar

## 📝 Notes

- The calendar is used as both input and output interface
- Events must be moved manually in Google Calendar
- Game state is persistent across sessions
- Future events are automatically cleaned up on game start
- All game data is stored in Google Calendar

## ⚠️ Important

- **Never commit `credentials.json` or `token.json`** - these contain sensitive authentication data
- The calendar created by this app should be dedicated to gaming
- Moving events manually in calendar is required for controls
- Some features require active internet connection for API calls

## 📄 License

[Add your license here]

## 👤 Author

[Add your name/contact here]

---

**Enjoy playing games through Google Calendar!** 🎉📅


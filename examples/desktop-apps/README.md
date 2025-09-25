# Desktop Applications Examples

This directory contains examples of desktop applications that can be created and managed using GitHub MCP integration.

## Socket Desktop Chat App

### Overview
A complete socket-based desktop chat application built with Python and Tkinter, demonstrating:
- Network socket programming with TCP connections
- Multi-threaded server-client architecture
- Real-time message broadcasting
- GUI application development with modern dark theme
- Connection management and error handling

### Features
- **Two Operating Modes**:
  - Server Mode: Host a chat server for multiple clients
  - Client Mode: Connect to an existing chat server

- **Real-time Communication**:
  - Instant message delivery using TCP sockets
  - Multi-client support with threaded connections
  - Message broadcasting to all connected users
  - Connection status monitoring

- **Interactive GUI**:
  - Clean, modern dark theme interface
  - Scrollable chat history with timestamps
  - Color-coded messages (self, others, system)
  - Real-time user count display
  - Connection settings configuration

- **Network Features**:
  - Configurable host and port settings
  - Username identification system
  - Automatic client disconnect handling
  - Server broadcast messaging
  - Error handling and reconnection support

### How to Run
1. Ensure Python with Tkinter is installed (included with most Python installations)
2. Navigate to the `examples/desktop-apps/` directory
3. Run the application:
   ```bash
   python socket_chat.py
   ```

### How to Use
1. **Starting a Server**:
   - Select "Start Server" mode
   - Configure host (leave as localhost for local testing) and port
   - Click "Start Server" button
   - Server will start accepting client connections

2. **Connecting as Client**:
   - Select "Connect to Server" mode
   - Enter server host IP and port
   - Click "Connect to Server"
   - Enter your username when prompted
   - Start chatting!

3. **Chatting**:
   - Type messages in the input field at the bottom
   - Press Enter or click "Send" to send messages
   - View chat history in the main display area
   - See connection status and user count (server mode)

### Technical Implementation
- **Language**: Python 3.x
- **GUI Framework**: Tkinter (built-in Python library)
- **Networking**: TCP sockets with threading
- **Architecture**: Multi-threaded client-server model
- **Styling**: Custom dark theme with professional appearance

### Code Structure
```python
class SocketChatApp:
    - __init__(): Initialize application state and UI
    - setup_ui(): Create and configure GUI elements
    - start_server(): Initialize TCP server and accept connections
    - start_client(): Connect to server as client
    - server_loop(): Main server thread for accepting clients
    - handle_client(): Thread for handling individual client messages
    - client_loop(): Client thread for receiving messages
    - broadcast_message(): Send messages to all connected clients
    - send_message(): Send message from current user
    - Connection management methods
```

### Learning Outcomes
This example demonstrates:
- Socket programming with TCP connections
- Multi-threaded network applications
- Client-server architecture patterns
- Real-time message broadcasting
- GUI development with Tkinter
- Network error handling and recovery
- Thread-safe GUI updates

### Potential Enhancements
- Add private messaging between users
- Implement chat rooms/channels
- Add file transfer capability
- Include emoji and rich text support
- Add user authentication system
- Implement message encryption
- Add chat history persistence
- Create mobile-responsive web version

---

## Tic-Tac-Toe Game

### Overview
A complete tic-tac-toe desktop application built with Python and Tkinter, demonstrating:
- GUI application development with Tkinter
- Game logic implementation
- AI opponent with strategic gameplay
- Modern UI design with dark theme
- Score tracking and game state management

### Features
- **Two Game Modes**:
  - Player vs Player: Two human players take turns
  - Player vs Computer: Play against an AI opponent

- **Smart AI Computer Player**:
  - Attempts to win when possible
  - Blocks player from winning
  - Uses strategic positioning (center, corners)
  - Provides challenging but fair gameplay

- **Interactive GUI**:
  - Clean, modern dark theme design
  - Color-coded players (X = red, O = blue)
  - Visual feedback for button interactions
  - Winning combination highlighting

- **Game Management**:
  - Score tracking for players and ties
  - New Game functionality
  - Reset Scores option
  - Current player indicator

### How to Run
1. Ensure Python with Tkinter is installed (included with most Python installations)
2. Navigate to the `examples/desktop-apps/` directory
3. Run the application:
   ```bash
   python tictactoe.py
   ```

### How to Play
1. Choose your preferred game mode (Player vs Player or Player vs Computer)
2. Click any empty square on the 3x3 grid to make your move
3. X always goes first (red color)
4. Get three symbols in a row (horizontal, vertical, or diagonal) to win
5. Use control buttons:
   - **New Game**: Start a fresh round
   - **Reset Scores**: Clear the scoreboard
   - **Quit**: Exit the application

### Technical Implementation
- **Language**: Python 3.x
- **GUI Framework**: Tkinter (built-in Python library)
- **Architecture**: Object-oriented design with single class structure
- **AI Algorithm**: Minimax-inspired strategy with priority-based decision making
- **Styling**: Custom color scheme with professional appearance

### Code Structure
```python
class TicTacToeGame:
    - __init__(): Initialize game state and UI
    - setup_ui(): Create and configure GUI elements
    - make_move(): Handle player moves and game logic
    - computer_move(): AI move generation
    - get_best_move(): AI strategy implementation
    - check_winner(): Win condition detection
    - Game management methods (reset, scoring, etc.)
```

### Learning Outcomes
This example demonstrates:
- Desktop GUI development with Python
- Event-driven programming patterns
- Game logic and state management
- AI algorithm implementation
- User interface design principles
- Error handling and input validation

### Potential Enhancements
- Add difficulty levels for AI
- Implement multiplayer over network
- Add game statistics and analytics
- Create custom themes and skins
- Add sound effects and animations
- Implement tournament mode

---

*This example showcases how GitHub MCP can facilitate rapid development and deployment of desktop applications through AI-assisted coding and repository management.*
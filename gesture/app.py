import streamlit as st
import threading
import webbrowser
import hill_climb
import temple_run

st.title("Gesture Control Gaming Dashboard")

# Dropdown for selecting a game
game = st.selectbox(
    "Select a game to control with gestures:",
    ["Hill Climb Racing", "Temple Run", "Ping Pong Ball", "Table Tennis", "Moto Rider"]
)

# Mapping games to URLs
game_urls = {
    "Hill Climb Racing": "https://poki.com/en/g/hill-climb-racing",
    "Temple Run": "https://poki.com/en/g/temple-run-2",
    "Ping Pong Ball": "https://playpong.io/",
    "Table Tennis": "https://king.com/game/candycrush",
    "Moto Rider": "https://play.google.com/store/apps/details?id=com.gun.sniper.game"
}

# Function to start gesture control based on selected game
def start_gesture_control(game_name):
    if game_name == "Hill Climb Racing":
        hill_climb.main()  # Start the hill climb gesture control
    elif game_name == "Temple Run":
        temple_run.main()  # Start the temple run gesture control
    # Add more gesture control functions for other games if needed

# Start the selected game when the button is clicked
if st.button("Start Game"):
    st.write(f"Starting {game} with gesture controls...")

    # Start gesture control in a separate thread
    gesture_thread = threading.Thread(target=start_gesture_control, args=(game,))
    gesture_thread.start()

    # Open the selected game's online version
    if game in game_urls:
        webbrowser.open(game_urls[game])

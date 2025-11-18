import requests
import time
import textwrap
# Removed 'feedparser' and 'random' as they were imported but not used.

# Vestaboard dimensions
ROWS = 6
COLS = 22

# --- CONFIGURATION (Load credentials) ---

def load_api_key(filename="vb.key"):
    """Reads the Vestaboard Local API Key from a file."""
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ API key file '{filename}' not found.")
        return None


def load_api_url(filename="vb.url"):
    """Reads the Vestaboard API URL from a file."""
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ API URL file '{filename}' not found.")
        return None

# --- TEXT TO CHARACTER MATRIX CONVERSION ---

def text_to_characters(text: str) -> list[list[int]]:
    """
    Convert plain text to a 6x22 Vestaboard character code matrix.
    It handles word wrapping and horizontal centering for the text.
    """
    # -----------------------------
    # Character mapping for Vestaboard (Duplicated from dashboard.py, 
    # ideally this would be a single, shared constant)
    # -----------------------------
    CHAR_MAP = {
        " ": 0,
        # Letters
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
        "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
        "K": 11, "L": 12, "M": 13, "N": 14, "O": 15,
        "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20,
        "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25,
        "Z": 26,
        # Numbers
        "0": 36, "1": 27, "2": 28, "3": 29, "4": 30,
        "5": 31, "6": 32, "7": 33, "8": 34, "9": 35,
        # Symbols
        "!": 37, "@": 38, "#": 39, "$": 40, "()": 41, # Keeping "()" as-is, though likely a symbol error
        ")": 42, "-": 44, "+": 46, "&": 47, "=": 48,
        ";": 49, ":": 50, "'": 52, '"': 53, "%": 54,
        ",": 55, ".": 56, "/": 59, "?": 60,  "°": 62,
        
        #### Color Blocks
        "]": 63, # Red Block
        "[": 66, # Green Block
        "^": 67  # Blue Block
    }

    # Split the text by newlines and wrap each line at COLS (22) width
    wrapped_lines = []
    for line in text.upper().split("\n"):
        # The textwrap module handles breaking long lines into word-wrapped segments
        wrapped_lines.extend(textwrap.wrap(line, width=COLS))

    # Fill the grid starting from the top row
    grid_lines = wrapped_lines[:ROWS]  # Truncate if too many lines
    while len(grid_lines) < ROWS:
        grid_lines.append("")  # Fill remaining rows with blank strings

    # Convert to Vestaboard numeric codes (0-67) with horizontal centering
    characters = []
    for line in grid_lines:
        # Calculate left padding for centering
        padding = (COLS - len(line)) // 2
        padded = " " * padding + line
        padded = padded.ljust(COLS, ' ') # Pad the right side with spaces if needed
        padded = padded[:COLS]  # Ensure exactly 22 columns (in case of uneven centering)
        
        # Convert each character in the padded line to its Vestaboard ID, defaulting to 0 (space)
        row = [CHAR_MAP.get(ch, 0) for ch in padded]
        characters.append(row)

    return characters

def send_to_vestaboard(text: str):
    """
    High-level function to convert text to a Vestaboard matrix and send it.
    (This function is not used in dashboard.py, but is kept for utility.)
    """
    characters = text_to_characters(text)
    print (characters)
    call_vestaboard_api(characters)

def call_vestaboard_api(characters: list[list[int]]):
    """
    Sends the 6x22 Vestaboard matrix (list of lists of character IDs)
    to the Vestaboard device via its local API.
    """
    try:
        api_key = load_api_key()
        api_url = load_api_url()

        if not api_key:
            print("⚠️ No Vestaboard API key available, skipping send.")
            return
        if not api_url:
            print("⚠️ No Vestaboard API URL available, skipping send.")
            return

        headers = {
            "X-Vestaboard-Local-Api-Key": api_key,
            "Content-Type": "application/json"
        }

        # The payload must contain the matrix under the "characters" key
        payload = {
            "characters": characters,
            "transition": "curtain" # Optional transition effect
        }

        response = requests.post(api_url, headers=headers, json=payload)
        # Check for successful response status code (2xx)
        response.raise_for_status()
        # print("✅ Vestaboard updated successfully.")

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error connecting to Vestaboard API (check URL/Key): {e}")
    except Exception as e:
        print(f"❌ General Error connecting to Vestaboard API: {e}")

# --- PROGRESS BAR UTILITY ---

def sleep_bar(sleep_seconds: int, position: int = 0, desc: str = "Sleeping {sleep_seconds:03d} Seconds"):
    """
    Pauses execution for a given number of seconds while displaying a
    TQDm progress bar in the console.
    """
    # Import tqdm here to keep it localized to this function
    from tqdm import tqdm
    # sys import is not needed for this usage

    # tqdm(range(int(sleep_seconds))) creates the progress bar
    # 'leave=False' ensures the bar disappears after completion
    for _ in tqdm(range(int(sleep_seconds)), leave=False, position=position, desc=desc, unit="s"):
        time.sleep(1) # Sleep for one second inside the loop

def progress_bar(sleep_seconds=10, position=0, desc="Sleeping"):
    """
    Alternative progress bar function, which is less ideal as it
    doesn't actually call time.sleep() itself (removed unused code).
    The 'sleep_bar' function is the one used in the main script.
    """
    from tqdm import tqdm

    if desc == "Sleeping":
        desc = f"{desc} {sleep_seconds:03d} Seconds"

    # Note: This function doesn't actually sleep, it just runs the bar fast.
    # It seems to be a partially implemented/redundant utility.
    # The 'sleep_bar' is preferred and used in dashboard.py.
    tqdm(range(int(sleep_seconds)), leave=False, position=position, desc=desc, unit="s")
import yfinance as yf
import requests
import json
import textwrap
import time

# Import necessary components from the common vestaboard.py
from vestaboard import send_to_vestaboard, load_api_key, load_api_url, text_to_characters, sleep_bar

# --- CONFIGURATION ---
tickers = {
    "DJI": "^DJI",
    "AAPL": "AAPL",
    "MSFT": "MSFT",
}

LINE_WIDTH = 22
LEFT_PADDING = 2
RIGHT_PADDING = 2

# --- VESTABOARD CHARACTER CODES (Now using placeholders for colored blocks) ---
# Use placeholders that will be mapped to the color codes in vestaboard.py
UP_ARROW_CHAR = 'GR' # Placeholder for Green Block (Code 66)
DOWN_ARROW_CHAR = 'RD' # Placeholder for Red Block (Code 63)
NEUTRAL_CHAR = '=' # Bullet for string display (will map to ? or be ignored)

# --- SUBROUTINE: Fetch and Prepare Stock Data ---
def fetch_and_prepare_stock_data(tickers):
    """
    Fetches stock data, checks for all-time high, and calculates price parts.
    Returns: (price_parts, max_dollar_len, change_symbols, all_time_high_flags)
    """
    price_parts = {}
    max_dollar_len = 0
    change_symbols = {}
    all_time_high_flags = {}

    # We now fetch the maximum historical data for all tickers to check the ATH
    full_data = yf.download(list(tickers.values()), period="max", auto_adjust=False)['Close']

    # We also fetch the 5-day period just for the last/previous close for the change calculation
    recent_data = yf.download(list(tickers.values()), period="5d", auto_adjust=False)['Close']


    for symbol_display, symbol in tickers.items():
        if symbol not in full_data.columns or symbol not in recent_data.columns:
            price_parts[symbol] = None
            all_time_high_flags[symbol] = False # Default to False if no data
            continue

        # Get latest and previous close from the recent_data (5 days)
        recent_closes = recent_data[symbol].dropna()

        if len(recent_closes) >= 1:
            latest = recent_closes.iloc[-1]

            # All-Time High Logic
            max_close = full_data[symbol].max()
            is_ath = (latest >= max_close) 
            all_time_high_flags[symbol] = is_ath


            if len(recent_closes) >= 2:
                previous = recent_closes.iloc[-2]
                change = latest - previous

                # Map change to a displayable STRING character placeholder
                change_symbol = (
                    UP_ARROW_CHAR if change > 0
                    else DOWN_ARROW_CHAR if change < 0
                    else NEUTRAL_CHAR
                )
                change_symbols[symbol] = change_symbol

            else: # Only one close available (change calculation not possible)
                change_symbols[symbol] = NEUTRAL_CHAR

            # Format price parts
            price_str = f"{latest:,.2f}"
            dollars, cents = price_str.split(".")
            max_dollar_len = max(max_dollar_len, len(dollars))
            price_parts[symbol] = (dollars, cents)

        else:
            price_parts[symbol] = None
            all_time_high_flags[symbol] = False

        print(f"{symbol}: {price_parts[symbol]}, ATH: {all_time_high_flags.get(symbol)}")

    return price_parts, max_dollar_len, change_symbols, all_time_high_flags

# --- SUBROUTINE: Format Lines as String (New implementation) ---
def format_lines_as_string(tickers, price_parts, max_dollar_len, change_symbols, all_time_high_flags):
    """
    Formats the prepared stock data into a single string with newlines,
    adhering to the specific column alignment requirements.
    Returns: single_string (str)
    """
    lines_text = []

    # REVISING UP_ARROW_CHAR/DOWN_ARROW_CHAR to single chars
    up_char = '['
    down_char = ']'
    neutral_char = '='
    ath_char = '°'

    for symbol_display, symbol in tickers.items():
        # --- 1. DETERMINE FIXED LEFT SIDE ---
        # Symbol should start in column 3. Since LEFT_PADDING is 2, the label starts at column 3.
        label = f"{symbol_display}:"
        label_text = " " * LEFT_PADDING + label
        # The label_text has a fixed length: LEFT_PADDING (2) + len(symbol_display) + 1 (for the colon)
        label_len = len(label_text) # e.g., "  AAPL:" is 8 characters long

        if price_parts[symbol] is None:
            line_text = f"{label_text} No data"
        else:
            dollars, cents = price_parts[symbol]
            is_ath = all_time_high_flags[symbol]

            change_symbol_placeholder = change_symbols[symbol]
            change_symbol = (
                up_char if change_symbol_placeholder == 'GR'
                else down_char if change_symbol_placeholder == 'RD'
                else neutral_char
            )

            padded_dollars = dollars.rjust(max_dollar_len)
            price_str = f"${padded_dollars}.{cents}"
            # Price string length is fixed by max_dollar_len: 1 (for $) + max_dollar_len + 1 (for .) + 2 (for cents)
            price_len = len(price_str)

            # --- 2. DETERMINE FIXED RIGHT SIDE ---
            # Column 21: Arrow (1 char)
            # Column 22: * or space (1 char)
            right_side_len = 2

            # --- 3. DETERMINE THE GAP ---
            # The price MUST end in column 19.
            # The total number of columns used by the right-hand block (Price + Blank + Arrow + *) 
            # is calculated from the right edge (Column 22) back to where the price starts.

            # Total width = 22
            # Target End Column of Price = 19
            # Col 20 = Blank (1 char)
            # Col 21 = Arrow (1 char)
            # Col 22 = * (1 char)

            # The entire block from price start to column 22 is:
            # (Price length) + 1 (blank) + 1 (arrow) + 1 (*)
            right_block_len = price_len + 3

            # The price block must start at: LINE_WIDTH (22) - right_block_len + 1
            # The total number of columns available for the label block and the gap is 22.
            # Gap = Total Width - (Label Length) - (Right Block Length)

            gap_len = LINE_WIDTH - label_len - right_block_len

            # Since the price block starts at a specific column to end at 19, let's verify:
            # Price starts at: 19 - price_len + 1
            # The label ends at: label_len
            # The gap must be: (Price start column) - (Label end column) - 1

            # Let's rely on the simpler calculation:
            # The final line must be 22 characters long.
            # Line = [Label Text (fixed)] + [Gap (calculated)] + [Price] + [Blank] + [Arrow] + [*]

            # Total components used: label_len + gap_len + price_len + 1 + 1 + 1 = 22
            # gap_len = 22 - (label_len + price_len + 3)
            # This is the correct gap calculation.

            # Assemble the line parts:
            line_text = (
                label_text
                + " " * gap_len
                + price_str
                + " " # Column 20 (Blank)
                + change_symbol # Column 21 (Arrow)
                + (ath_char if is_ath else ' ') # Column 22 (*)
            )

        # Ensure the line is exactly the width (22 chars)
        lines_text.append(line_text[:LINE_WIDTH].ljust(LINE_WIDTH))

    # Pad with blank lines to 6 rows
    while len(lines_text) < 6:
        lines_text.append(" " * LINE_WIDTH)

    # Join all lines into one string, separated by newlines
    single_string = "\n".join(lines_text)

    return single_string


# Note: The rest of ticker.py remains the same.
# We trust the data fetching logic remains correct for this modification.
# The main execution loop is omitted for brevity.

# =================================================================
# --- MAIN EXECUTION ---
# =================================================================

while True:
    # 1. Fetch and Prepare Data
    price_data, max_len, change_symbols, all_time_high_flags = fetch_and_prepare_stock_data(tickers)

    # 2. Format Lines into a single string
    formatted_string = format_lines_as_string(tickers, price_data, max_len, change_symbols, all_time_high_flags)

    # 3. Print for debug
    print("\nFormatted String for Vestaboard:")
    print(formatted_string)

    # 4. Send to Vestaboard using the string-based subroutine from vestaboard.py
    send_to_vestaboard(formatted_string)

    sleep_bar(60,0,"Sleeping 60 seconds")
import requests
import time
import textwrap
import random

# Import necessary components from the common vestaboard.py
# We only need send_to_vestaboard, which internally uses load_api_key.
from vestaboard import send_to_vestaboard, load_api_key, sleep_bar

# Replace with your Vestaboard Read/Write API key (No longer needed, handled by vestaboard.py)

def get_dad_joke():
    """Fetches a random dad joke from icanhazdadjoke.com."""
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = resp.json()
        return data.get("joke")
    except requests.RequestException as e:
        print(f"❌ Failed to fetch dad joke: {e}")
        return None


if __name__ == "__main__":

    while True:
        joke = get_dad_joke()

        # Original logic to filter out very long jokes (Vestaboard is 6x22 = 132 chars max)
        # Using a slightly different loop structure for robustness.
        while joke is None or len(joke) > 132: 
            if joke is None:
                print("⚠️ Joke fetch failed, retrying in 5 seconds...")
                time.sleep(5)
            elif len(joke) > 132:
                print(f"⚠️ Joke too long ({len(joke)} chars), fetching new joke.")

            # Fetch the next joke
            joke = get_dad_joke()

            # Prevent an infinite loop if the API keeps returning very long jokes
            # (though the limit is 132, the service usually returns short jokes)
            if joke is None:
                continue

        print("\n--- Joke to be Displayed ---")
        print(joke)

        # Send to Vestaboard using the common subroutine
        # The send_to_vestaboard in vestaboard.py handles text_to_characters 
        # (which includes wrapping and centering).
        send_to_vestaboard(joke)

        # Wait 45 seconds before fetching the next joke
        sleep_bar(45)
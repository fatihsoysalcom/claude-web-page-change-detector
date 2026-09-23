import requests
import hashlib
import time

# --- Configuration ---
URL_TO_MONITOR = "https://example.com" # Replace with the URL you want to monitor
CHECK_INTERVAL_SECONDS = 60 # How often to check the URL (in seconds)
# ---------------------

def get_page_hash(url):
    """Fetches the content of a URL and returns its SHA256 hash."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
        content = response.text
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def monitor_web_page(url, interval):
    """Continuously monitors a web page for changes."""
    print(f"Starting to monitor: {url}")
    print(f"Check interval: {interval} seconds")
    print("Press Ctrl+C to stop.")

    previous_hash = None

    while True:
        current_hash = get_page_hash(url)

        if current_hash is None:
            # If fetching failed, we can't determine a change, so skip this check
            pass
        elif previous_hash is None:
            # First check, just store the hash
            print(f"Initial content hash: {current_hash}")
            previous_hash = current_hash
        elif current_hash != previous_hash:
            # Content has changed!
            print("\n!!! CONTENT CHANGE DETECTED !!!")
            print(f"Previous hash: {previous_hash}")
            print(f"Current hash:  {current_hash}")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            # In a real-world scenario, you'd log this, send an alert, or store proof.
            previous_hash = current_hash # Update to the new hash
        else:
            # No change detected
            print(f".", end="", flush=True) # Print a dot to show it's still running

        time.sleep(interval)

if __name__ == "__main__":
    try:
        monitor_web_page(URL_TO_MONITOR, CHECK_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

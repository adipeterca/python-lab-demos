# Sauron - a price tracking demo app

A demo Python application that allows real-time price tracking, with colorful output & TTS notifications.

## Libraries used

1. [Colorama](https://pypi.org/project/colorama/)

For nice colored output.
For what colors to use, one can be inspired by rarity systems (usually found in games):

| Color | Description |
|-------|-------------|
| white | common objects / debug |
| green | uncommon objects / information |
| blue | rare objects / warnings |
| yellow | epic / errors |
| purple | legendary / critical |

Or, another idea is to use the following scheme:

| Color | Description |
|-------|-------------|
| gray / white | debug |
| blue | information |
| yellow | warnings |
| red | errors |
| bright red / magenta | critical errors |


2. [requests](https://pypi.org/project/requests)

Used for performing HTTP requests in a clean and reliable way.  
It allows the app to fetch the webpage that contains the price information you want to track.

Key capabilities:
- Sending GET requests to retrieve HTML content
- Handling timeouts and connection errors gracefully
- Spoofing headers (the most common is User-Agent) when needed
- Ensuring consistent, readable network code

This library acts as the foundation for obtaining data before parsing it with BeautifulSoup.

3. [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

Used for parsing HTML content retrieved from web pages.  
It allows the app to extract specific elements such as price, currency, or product details from the fetched webpage.

Common actions:
- Finding tags by ID or class
- Navigating the DOM
- Cleaning and structuring extracted data


4. `datetime` (standard library)

Used for generating timestamps, logging events, and storing historical price changes.  
Timestamps are saved in a human-readable format and also help order entries in the local database.


5. `sqlite3` (standard library)

Provides a lightweight, file-based SQL database used to store the price history.  
It enables:
- Creating a local database automatically if missing  
- Logging every tracked price with currency and timestamp  
- Querying previous values to detect changes or trends  


6. `os` (standard library)

Used primarily for filesystem checks, like verifying whether the database file exists before creating it.  
It also helps keep the app portable and OS-friendly.


7. `time` (standard library)

Responsible for timed execution.  
The application uses it to run periodic checks (e.g., every 5 minutes) by simply sleeping between cycles.


8. `http.server` → `BaseHTTPRequestHandler` & `HTTPServer` (standard library)

These modules allow the app to spin up a tiny local web server that serves a simple status page containing the latest tracked information.  
The HTML can be generated at runtime, letting you monitor the current price from a browser on the same machine.

Typical uses:
- Serving dynamic HTML
- Testing data endpoints locally
- Displaying results without a full frontend framework
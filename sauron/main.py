import colorama
import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3
import os
import time

############################################################################################################################

# Requiered on Windows
colorama.init()


############################################################################################################################

def log_debug(msg):
    print(f"{colorama.Fore.WHITE}{msg}{colorama.Fore.RESET}")

def log_info(msg):
    print(f"{colorama.Fore.BLUE}{msg}{colorama.Fore.RESET}")

def log_price_increased(msg):
    print(f"{colorama.Fore.RED}{msg}{colorama.Fore.RESET}")

def log_price_decreased(msg):
    print(f"{colorama.Fore.GREEN}{msg}{colorama.Fore.RESET}")

def log_critical(msg):
    print(f"{colorama.Fore.RED + colorama.Style.BRIGHT}{msg}{colorama.Fore.RESET + colorama.Style.RESET_ALL}")



############################################################################################################################

def database_setup() -> sqlite3.Connection:
    '''
    Makes sure the database exists. If not, create it.\n
    Return a cursor that can be later used for operations.

    @returns: sqlite3.Connection object
    '''
    DB_FILE = "history.db"

    db_exists = os.path.exists(DB_FILE)

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        if not db_exists:
            cursor.execute("""
                CREATE TABLE history (
                    price INT,
                    currency VARCHAR(10),
                    timestamp TEXT
                )
            """)
            conn.commit()
        
        return conn

    except Exception as e:
        log_critical(f"Failed to connect or operate on database: {e}")
        exit(1)

def track_price(conn: sqlite3.Connection):

    cursor = conn.cursor()

    try:

        log_debug("Connecting to website ...")

        response = requests.get(
            url="http://127.0.0.1:8000"
        )


        log_debug("Parsing price & currency ...")
        
        parser = BeautifulSoup(response.text, "html.parser")
        price = parser.find("span", id="amount")
        if price is None:
            raise RuntimeError("Could not find price in HTML body")
        price = price.text
        
        currency = parser.find(id="currency")
        if currency is None:
            raise RuntimeError("Could not find currency in HTML body")
        currency = currency.text

        log_info(f"Current price is {price} {currency}")
        
        log_debug("Inserting values into database...")

        # There is a difference between %d and %D (applies to all values)
        # %d -> day
        # %m -> month
        # %Y -> year
        # %H -> hour
        # %M -> minutes
        # %S -> seconds
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        cursor.execute(
            # f"INSERT INTO history (price, currency, timestamp) VALUES ({price}, {currency}, {timestamp})"         # Not the best approach because of how INT or STRING
                                                                                                                    # is mapped to sqlite values. Also, it enables SQL Injection
            "INSERT INTO history (price, currency, timestamp) VALUES (?, ?, ?)",
            (price, currency, timestamp)
        )

        conn.commit()


        # Now, try to query the last 2 prices and see if there was a difference
        cursor.execute("SELECT price FROM history ORDER BY timestamp DESC LIMIT 2")
        rows = cursor.fetchall()

        if len(rows) < 2:
            log_info("Not enough entries to compare.")
        else:
            price1, price2 = rows[1][0], rows[0][0]

            if price1 != price2:
                diff_procentage = abs(round(price2 * 100 / price1 - 100, 2))
                if price1 > price2:
                    log_price_decreased(f"Price decreased by {diff_procentage}%")
                else:
                    log_price_increased(f"Price increased by {diff_procentage}%")
            else:
                log_debug("No difference in prices")


    except RuntimeError as e:
        log_critical(e)

if __name__ == "__main__":

    conn = database_setup()

    while True:
        track_price(conn)
        
        log_debug("Waiting 30 seconds ...")
        time.sleep(30)

    
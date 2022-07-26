from time import sleep
from scraper import get_data
import sqlite3
from multiprocessing import Process
from tbot import main

user_database='users.db'

conn = sqlite3.connect(user_database, check_same_thread=False)

def run_scraper():
    ''' This function is a wrapper around the scraper to make things
    easier '''
    cursor = conn.execute("SELECT ID from USERS")
    for row in cursor:
        print(row[0])
        get_data(row[0])

if __name__ == '__main__':

    # Run the telegram bot.
    # Run the scraper every 30 minutes.
    p1 = Process(target=main, args=())
    p1.start()
    while True:
        run_scraper()
        print("Running scraper...")
        sleep(1800)
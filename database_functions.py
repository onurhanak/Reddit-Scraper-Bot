import sqlite3 
import sys 

# Defining database
user_database='users.db'

# Initial connection to database, necessary for some reason

def init_db():
    # Initialize the database
    conn = sqlite3.connect(user_database, check_same_thread=False)

    conn.execute('''CREATE TABLE USERS
            (ID INT PRIMARY KEY     NOT NULL,
            KEYWORDS           TEXT    NOT NULL,
            SUBREDDITS            TEXT     NOT NULL);''')
            
    conn.commit()
    conn.close()

# if the script is run with the argument 'init' initialize the database
initialize_database = sys.argv[1] if len(sys.argv) > 1 else '.'
if initialize_database == 'init':
    init_db()
else:
    pass

def insert_user(id, keywords, subreddits):
    ''' This function gets the parsed values of id, keywords and subreddits
    inserts them into the database table called USERS'''
    
    conn = sqlite3.connect(user_database, check_same_thread=False)

    conn.execute("INSERT OR REPLACE INTO USERS (ID, KEYWORDS, SUBREDDITS) \
        VALUES (?, ?, ?)", (id, keywords, subreddits))

    conn.commit()
    conn.close()

def create_user_table(userid):
    ''' This function creates a table with userid to store 
    subreddit preferences and sent posts, so we do not send them again
    and again and again and again...'''
    conn = sqlite3.connect(user_database, check_same_thread=False)
    
    command = "CREATE TABLE IF NOT EXISTS {tablename} (SENT_POSTS TEXT)".format(tablename=userid)
    print(userid)
    
    conn.execute(command)
    conn.commit()
    conn.close()

def insert_link(id, link):
    conn = sqlite3.connect(user_database, check_same_thread=False)

    '''This function inserts the links that are already sent to the user
    to the user's table in the database, so we can keep track of them.'''
    conn = sqlite3.connect(user_database, check_same_thread=False)
    conn.execute("INSERT INTO " + id + "(SENT_POSTS) VALUES(?)", (link,))
    conn.commit()

def update_user(id, keywords, subreddits):
    conn = sqlite3.connect(user_database, check_same_thread=False)

    ''' This function takes parsed values of id, keywords and subreddits 
    and updates the preferences of the user in the database if initiated through
    /settings command'''
    conn = sqlite3.connect(user_database, check_same_thread=False)
    conn.execute("UPDATE USERS SET KEYWORDS = ?, SUBREDDITS = ? WHERE ID = ?", (keywords, subreddits, id))
    conn.commit()
    conn.close()

    # Send a message to the user so they know we acquired and set the settings succesfully
    message1="Successfully set settings."
    message2="I am going to search for the keywords: {}".format(keywords.replace("|", ", "))
    message3="I am going to search the subreddits: {}".format(subreddits)
    from tbot import send_message # workaround for circular import, i know i know
    send_message(id, message1)
    send_message(id, message2)
    send_message(id, message3)


def read_user_settings(chat_id):
    conn = sqlite3.connect(user_database, check_same_thread=False)

    ''' This function reads the preferences of the user by querying the database with 
    the chat id'''
    subreddits = conn.execute("SELECT SUBREDDITS FROM USERS WHERE ID = ?", (chat_id,)).fetchone()[0].split(" ")
    keywords = conn.execute("SELECT KEYWORDS FROM USERS WHERE ID = ?", (chat_id,)).fetchone()[0].split("|")

    return subreddits, keywords

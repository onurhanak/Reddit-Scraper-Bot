import requests
from database_functions import read_user_settings, insert_link
from tbot import send_message
import sqlite3 

# Defining database
user_database='users.db'

# Initial connection to database, necessary for some reason
conn = sqlite3.connect(user_database, check_same_thread=False)

def construct_links(subreddits):
    ''' This function constructs a list of URLs using the settings of the user
    and returns the list'''
    subreddit_links = []

    for subreddit in subreddits:
        subreddit_link = "https://reddit.com/r/" + subreddit + "/new/.json"
        subreddit_links.append(subreddit_link)

    return subreddit_links

def get_data(chat_id):
    '''This is the function that gets data from 
    Reddit API'''

    # first we get the user's table id which is just
    # user + telegram chat id
    user_id = "user" + str(chat_id)

    print("Getting data for user id: {}".format(user_id))

    # to query the user preferences from the database
    subreddits, keywords = read_user_settings(chat_id)

    # construct links from subreddit names
    subreddit_links = construct_links(subreddits)

    for subreddit in subreddit_links:

        # get API response, load as json
        response = requests.get(subreddit, headers={
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'})
        data = response.json()

        for post in data['data']['children']:
            title = post['data']['title']
            # we get this so we can store the posts we have already checked in the database
            postid = post['data']['id']
            title = title.lower()  # to make it easier to check for keywords
            for keyword in keywords:
                keyword = keyword.lower()  # to make it easier to check for keywords
                if keyword in title:
                    cursor = conn.execute(
                        'SELECT 1 FROM "{}" WHERE SENT_POSTS = "{}"'.format(user_id, postid))

                    # check if we have not already sent the post to the user
                    if cursor.fetchone() is None:
                        # send the post
                        url = post['data']['url']  # post link to send
                        print("Found unsent post. Sending it to {} with chat id {}.".format(
                            user_id, chat_id))
                        send_message(chat_id, title + ' ' + url)
                        # add sent link to the database so we do not send it again
                        insert_link(user_id, postid)
                    else:
                        # just for debugging purposes
                        # log the action
                        print("Found post but it is already sent to user {} with chat id {}".format(
                            user_id, chat_id))

                # if keyword is not in title do not do anything
                else:
                    pass

    print("Finished getting data for user id: {}".format(user_id))

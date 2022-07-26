
<h1 align='center'>Reddit Scraper Bot</h1>

This is a Telegram bot that interacts with Reddit API to search for keywords in post titles in subreddits set by the user. All interaction with the bot happens through Telegram commands. Check the tbot.py file for more information.


## Deployment


1. Clone this repository by running:
    
         git clone https://github.com/onurhanak/Reddit-Scraper-Bot

or just download the zip from this page.

2. Second, install the requirements. This project only depends on python-telegram-bot package. Install it by running:

         pip install python-telegram-bot

3. Initialize the database to store user settings and preferences. To do this you need to run:

        python database_functions.py init

4. After initializing the database the bot will start running automatically but there will be no settings for it to do the actual scraping. Settings can be set through Telegram. You need to create a bot first using @BotFather on Telegram. 

5. After creating your Telegram bot, add its API key to tbot.py file. 

6. Start your bot by texting it /start . This will create the user database to store preferences.

7. Use /settings command to set keywords to search for and the subreddits to search:

        /settings ['keyword1' 'keyword2 with multiple words' 'keyword3'] - subreddit1 subreddit2 subreddit3 subreddit4

Example:

    /settings ['Intel' 'AMD' 'Thinkpad X1'] - laptopdeals buildapcsales 

8. Enjoy your bot. 


### License

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)




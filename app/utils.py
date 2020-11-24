import tweepy
from decouple import config
from instabot import Bot

MAX_CHAR = 248

def tweet(report_type, country, title, filename, url):
    """
    Publish a tweet in twitter.com/BuscaMascotapy about the specific report
    """
    # CONSUMER_KEY = config('TWITTER_CONSUMER_KEY')
    # CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET') 
    # ACCESS_KEY = config('TWITTER_ACCESS_KEY')
    # ACCESS_SECRET = config('TWITTER_ACCESS_SECRET')
    CONSUMER_KEY='CBLR701aqALxW22ZQMzITeirh'
    CONSUMER_SECRET='GmNbAxkSiHHmDMZkoBc7X8EalYuV2RmLdCDgXmMEfo7SEmsOBQ'
    ACCESS_KEY='1307068342042324993-26IGVEFG1qbl6HsOWTYI9h9nECBbAR'
    ACCESS_SECRET='LhKLpFBODLjd2rSLQPKkEXluLokwt6nson6Go5GKEeVRc'


    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    api = tweepy.API(auth)

    message = '#'+ report_type.upper() + ' #' + country.replace(' ', '').upper() + ' ' + title + ' ' + url
    
    #if message excess MAX_CHAR of twitter can't tweet so the message is shorten
    if len(message) > MAX_CHAR:
        excess = message - MAX_CHAR
        message = message[0:len(message)-len(url)-1] + ' ' + message[-len(url):]

    try:
        api.update_with_media(filename,status=message)
    except:
        api.update_status(message)

def post_instagram_facebook(report_type, country, title, filename, url):
    """
    Publish a post in instagram.com/buscamascotapy and in the official page at facebook about the specific report
    """

    username = 'buscamascotapy'
    INSTA_PASS = config('INSTAGRAM_PASSWORD')
    bot = Bot() 
    
    
    bot.login(username = username,  
            password = INSTA_PASS) 

    text = message = '#'+ report_type.upper() + ' #' + country.replace(' ', '').upper() + ' ' + title + ' ' + url
   
    bot.upload_photo(filename,  
            caption = text) 


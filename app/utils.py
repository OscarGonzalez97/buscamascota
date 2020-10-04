import tweepy
from decouple import config

MAX_CHAR = 248

def tweet(report_type, country, title, filename, url):
    """
    Publish a tweet in twitter.com/BuscaMascotapy about the specific report
    """
    # CONSUMER_KEY = config('TWITTER_CONSUMER_KEY')
    # CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET') 
    # ACCESS_KEY = config('TWITTER_ACCESS_KEY')
    # ACCESS_SECRET = config('TWITTER_ACCESS_SECRET')
    CONSUMER_KEY='uHw5zRJOWE3JV7rcClFia067j'
    CONSUMER_SECRET='uqeT8WoJf2yyxu7uJGJHASzZ2SkhbdW1Uye5mBmD1E68zqzBEJ'
    ACCESS_KEY='1307068342042324993-k3WlzZ5IrINHET9wmDELrAupIRCTRM'
    ACCESS_SECRET='FOlXu6K8moylynd4oh3IXgjR5zjk34BuxKGUdBGBJkxln'


    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    api = tweepy.API(auth)

    filename='../' + filename

    message = '#'+ report_type.upper() + ' #' + country.replace(' ', '').upper() + ' ' + title + ' ' + url
    
    #if message excess MAX_CHAR of twitter can't tweet so the message is shorten
    if len(message) > MAX_CHAR:
        excess = message - MAX_CHAR
        message = message[0:len(message)-len(url)-1] + ' ' + message[-len(url):]

    try:
        api.update_with_media(filename,status=message)
    except:
        api.update_status(message)
import base64

import tweepy
from decouple import config
from instabot import Bot

MAX_CHAR = 248


def tweet(report_type, country, title, base64_image, url):
    """
    Publish a tweet in twitter.com/BuscaMascotapy about the specific report
    """
    CONSUMER_KEY = config('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET')
    ACCESS_KEY = config('TWITTER_ACCESS_KEY')
    ACCESS_SECRET = config('TWITTER_ACCESS_SECRET')

    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_KEY,
        access_token_secret=ACCESS_SECRET
    )

    # api = tweepy.API(client)

    message = '#' + report_type.upper() + ' #' + country.replace(' ', '').upper() + ' ' + title + ' ' + url

    # if message excess MAX_CHAR of twitter can't tweet so the message is shorten
    if len(message) > MAX_CHAR:
        excess = message - MAX_CHAR
        message = message[0:len(message) - len(url) - 1] + ' ' + message[-len(url):]

    # Decode the base64 image data
    # image_data = base64.b64decode(base64_image)
    client.create_tweet(text=message)
    # try:
    #     api.update_status_with_media(filename='image.jpg', status=message, file=image_data)
    # except:


def post_instagram_facebook(report_type, country, title, filename, url):
    """
    Publish a post in instagram.com/buscamascotapy and in the official page at facebook about the specific report
    """

    username = 'buscamascotapy'
    INSTA_PASS = config('INSTAGRAM_PASSWORD')
    bot = Bot()

    bot.login(username=username,
              password=INSTA_PASS)

    text = message = '#' + report_type.upper() + ' #' + country.replace(' ', '').upper() + ' ' + title + ' ' + url

    bot.upload_photo(filename,
                     caption=text)

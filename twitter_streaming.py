import sys
import string
import time
import os
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


def get_twitter_auth():
    try:
        consumer_key = "6AAYBi2AHdcof4UP29WCNDSYj"
        consumer_secret = "C2jNmvz2KeyGJvqff69P65MvcYjlsJLiWYdXu8WNEADiaIdSHh"
        access_token = "1243746744476852224-qbCvO51uXteufR32iCHy5STqzKBqbM"
        access_secret = "dvG3qVWM8gz3sM0LMSqz6Pxyg8Mmg8wTVxv05k9JalW4u"
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def get_twitter_client():
    auth = get_twitter_auth()
    client = API(auth)
    return client

class CustomListener(StreamListener):
    def __init__(self, fname):
        safe_fname = format_filename(fname)
        self.outfile = "stream_%s.jsonl" % safe_fname

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            sys.stderr.write("Error on_data: {}\n".format(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n".format(status))
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True

def format_filename(fname):
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'
    
query = '#Trump'
query_fname = ' '.join(query) # string
auth = get_twitter_auth()
twitter_stream = Stream(auth, CustomListener(query_fname))
twitter_stream.filter(track=query)
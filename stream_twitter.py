import time
import sys
import json
from threading import Thread
from collections import OrderedDict

from tweepy.streaming import StreamListener
from tweepy.api import API
from tweepy import OAuthHandler
from tweepy import Stream

from key import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET




auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

class StdOutListener(StreamListener):

    def __init__(self, listener_id, callback=None):
        super(StdOutListener, self).__init__()
        self.listener_id = listener_id
        self.callback = callback
        self.count = 0

    def on_data(self, data):
        message = json.loads(data)['text']
        if self.count > 10:
            return False
        else:
            self.count += 1
        if self.callback:
            message = json.loads(data)['text']
            self.callback(message)

    def on_error(self, status_code):
        if status_code == 420: # Enhance Your Calm which means we are being rate limit.
            return False


def ListenerAction(auth, listener_id, callback=None, track=None):
    listener = StdOutListener(listener_id, callback)
    stream = Stream(auth, listener)

    def action():
        stream.filter(track=['trump'])

    return action()
    
if __name__ == '__main__':
    import json
    api = API(auth)
    print("Start searching New York trends topics...")
    trends = api.trends_place(2459115)
    with open("trends.json", "w+") as f:
        f.write(json.dumps(trends))
        


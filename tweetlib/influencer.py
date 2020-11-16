from tweetlib import utils
import pandas as pd

class Influencer:
    def __init__(self, profile, filepath):
        self.profile = profile
        self.filepath = filepath
        self.tweets = pd.read_csv(filepath)

    def filter_tweets(self, df_b3_companies):
        self.tweets = utils.filter_tweets(self.tweets, df_b3_companies)

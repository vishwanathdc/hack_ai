import re
import tweepy
import numpy as np
from tweepy import OAuthHandler
from textblob import TextBlob
import sys
import json
from urllib.request import urlopen
import requests
import pandas as pd
import numpy as np

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'BkmvNwrWZxTM4R2jrax8VDLqn'
        consumer_secret = 'iN3qv5C8bO1oC9UZx3NFuGA0JtMxYCGPxnNBFk78A78f1g463G'
        access_token = '2373980444-3LzLjKbtTYNUytGOBAaUG41PratvGSbkEk4T0o8'
        access_token_secret = 'DH63ziM2W4DkkWdHQH1vJrd3EVYMlfNe8ok4Ixz7W8LHv'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

class whois(object):
    #try:
    #    from urllib.request import urlopen
    #except ImportError:
    #    from urllib2 import urlopen
    def details(self, query):
        domainName = query;
        apiKey = 'at_8wt5pTmGtVGGUL0ErQazqir7RY9wy'

        url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService?'\
            + 'domainName=' + domainName + '&apiKey=' + apiKey + "&outputFormat=JSON"
        #rint(urlopen(url).read().decode('utf8'))
        d = json.loads(urlopen(url).read().decode('utf8'))
        orgname = (d['WhoisRecord']['registrant']['organization'])
        #if  not (d['WhoisRecord']['registrant']['telephone']):
        #    telephonenumber = ""
        #else:
        #    telephonenumber = (d['WhoisRecord']['registrant']['telephone'])
        #street = (d['WhoisRecord']['registrant']['street1'])
        #city = (d['WhoisRecord']['registrant']['city'])
        #state = (d['WhoisRecord']['registrant']['state'])
        #postalcode = (d['WhoisRecord']['registrant']['postalCode'])
        #country = (d['WhoisRecord']['registrant']['country'])
        #address = street + '\n' + city + '\n' + state + '\n' + postalcode + '\n' + country
        #return orgname + telephonenumber + address
        return orgname

class finance(object):
    #try:
    #    from urllib.request import urlopen
    #except ImportError:
    #    from urllib2 import urlopen
    def stockreview(self, query):
        url = 'http://autoc.finance.yahoo.com/autoc?query=' + query + '%20inc&region=US&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback'
        str = urlopen(url).read().decode('utf-8')
        str = str[39:]
        str = str[:-2]
        d = json.loads(str)
        name = (d['ResultSet']['Result'][0]['symbol'])
        #print(name)

        url2 = 'https://api.iextrading.com/1.0/stock/' + name + '/quote'
        str2 = urlopen(url2).read().decode('utf-8')
        d2 = json.loads(str2)
        peratio = (d2['peRatio'])
        year_low = (d2['week52High'])
        year_high = (d2['week52Low'])
        return peratio,year_low,year_high

class yelp_review(object):
    def review(self, query):
        df = pd.read_json('D:\hackai\yelp_academic_dataset_business.json', lines = True)
        df.drop(['business_id','address','attributes','city','hours','is_open','latitude','longitude','neighborhood','postal_code','state'],axis = 1, inplace = True)
        df = df[['name','stars','review_count','categories']]
        scores =  .5*df.stars + 5*(1-np.exp(-df.review_count/10)) 
        df['scores'] = scores
        df2=df[df['name'].str.contains(query)]
        score_1 = (np.sum(df2.scores)/len(df2))
        return score_1
 
def main():
    # creating object of TwitterClient Class
    user_query = input("enter the company name")
    #user_query = 'facebook'
    query_url = user_query + ".com"
    api = TwitterClient()
    # calling function to get tweets

    userdetails = whois()
    print(userdetails.details(query_url))
    
    tweets = api.get_tweets(query = user_query, count = 1000)
    #non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    pos_per = round((100*len(ptweets)/len(tweets)),2)
    pos_per = int(pos_per)
    print("Positive tweets percentage: ", pos_per, "%")
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    neg_per = round((100*len(ntweets)/len(tweets)),2)
    neg_per = int(neg_per)
    print("Negative tweets percentage: ", neg_per, "%")
    if(len(ptweets) > len(ntweets)):
        print('We have a positive twitter review')
    else:
        print('We have a negative twitter review')
 
    review = finance()
    pretio , highprice, Lowprice = review.stockreview(user_query)
    print("peratio: " , pretio)
    print("highest stock prce in 1 year: " , highprice)
    print("Lowest stock prce in 1 year : " , Lowprice)
    print("Generally a high P/E ratio means that investors are anticipating higher growth in the future.")
    print("The average market P/E ratio is 20-25 times earnings")
    yelpreview = yelp_review()
    print("yelp score: " , yelpreview.review(user_query))

 
if __name__ == "__main__":
    # calling main function
    main()

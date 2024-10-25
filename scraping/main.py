from twikit import Client, TooManyRequests
import time 
from datetime import datetime, timedelta
from Topic import Topic
import csv
from configparser import ConfigParser
from random import randint 
import asyncio

#------------------------------------Will Change---------------------------------------
MINIMUM_TWEETS = 20
client = Client(language='en-US')
now = datetime.now()
yesterday = now - timedelta(days=10)
since_date = yesterday.strftime('%Y-%m-%d')
until_date = now.strftime('%Y-%m-%d')
#--------------------------------------------------------------------------------------

async def get_tweets(tweets, url):        
    QUERY = f"from:{url} since:{since_date}"
    if tweets is None: 
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top') # does so in 20's so if wuery is 41 it will get 60
    else: 
        wait_time = randint(3,8)
        print(f'{datetime.now()} - Getting next teets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
    return tweets


async def tweet_caller(name, url):
    #getting tweets to populate the CSV
    tweet_count = 0
    tweets = None    
    while tweet_count < MINIMUM_TWEETS: 
        try: 
            tweets = await get_tweets(tweets, url)       
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue
        if not tweets: 
            print(f'{datetime.now()} - No more tweets found')
            break
        for tweet in tweets: 
            tweet_count += 1
            tweet_data = [tweet.id, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
            with open(f"{name}_tweets.csv", 'a', newline='', encoding='utf-8') as file: 
                writer = csv.writer(file)
                writer.writerow(tweet_data)
    print(f'{datetime.now()} - Done! {tweet_count} tweets found')

async def sign_in():
    username = "ThrowawayLate"  
    password = "LaterThrowMeAway1!"
    email = "ThrowawayLater01@gmail.com" 
    formatted_date = now.strftime("%d%m%Y")
     # Client Authentication and cookie storage
    await client.login(auth_info_1=username, auth_info_2=email, password=password)  
    client.save_cookies(f'{formatted_date}.json')


async def main_request(name, urls): 
    
    with open(f'{name}_tweets.csv', 'w', newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created_at', 'number_of_tweets', 'number_of_likes'])
    for url in urls:
        print(url)
        wait_time = randint(1,5)
        await asyncio.sleep(wait_time) 
        await tweet_caller(name, url)

def fetch_tweets(topics):
    asyncio.run(fetch_tweets_for_all(topics))

async def fetch_tweets_for_all(topics):
    firstRun = True
    for topic in topics:
        if firstRun:
            await sign_in()
        print(f"Fetching tweets for topic: {topic.name}")
        await main_request(topic.name, topic.urls)

topic_biology = Topic('Biology', ['edyong209', 'ImmunologyNews', 'NatureEcoEvo', 'TheScientistLLC', 'BMCBiology'])
topic_ai = Topic('Artificial Intelligence', ['lexfridman', 'DeepMind', 'OpenAI', 'AndrewYNg', 'MIT_CSAIL'])
topic_math = Topic('Mathematics', ['Mathologer', 'standupmaths', 'fermatslibrary', 'stevenstrogatz', 'MathematicsProf'])
topic_world_news = Topic('World News', ['BBCWorld', 'CNN', 'Reuters', 'AJEnglish', 'TheEconomist'])
topics = [topic_biology,topic_ai,topic_math,topic_math]

fetch_tweets(topics)


        

    
    

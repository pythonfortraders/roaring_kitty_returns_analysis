from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pickle
import time
import logging
import csv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

TWEET_ELEMENT = '//article[@data-testid="tweet"]'
TWEET_TEXT_ELEMENT = './/div[@data-testid="tweetText"]'
TWEET_TIME_ELEMENT = ".//time"


def get_tweets_selenium(username, tweet_limit=50):
    url = f"https://twitter.com/{username}"

    driver = webdriver.Chrome()
    driver.get("https://twitter.com")

    # Load cookies from the file
    with open("twitter_cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if "domain" in cookie:
                del cookie["domain"]
            driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(5)

    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    tweets = []

    while len(tweets) < tweet_limit:
        elements = driver.find_elements(By.XPATH, TWEET_ELEMENT)
        for element in elements:
            try:
                tweet_text_element = element.find_element(By.XPATH, TWEET_TEXT_ELEMENT)
                tweet_text = tweet_text_element.text
            except:
                tweet_text = None

            try:
                timestamp_element = element.find_element(By.XPATH, TWEET_TIME_ELEMENT)
                timestamp = timestamp_element.get_attribute("datetime")
            except:
                logging.error(f"Timestamp not found for tweet: {tweet_text}")
                timestamp = None

            tweet_data = {
                "username": username,
                "timestamp": timestamp,
                "text": tweet_text,
            }

            if tweet_data not in tweets:
                tweets.append(tweet_data)
                logging.info(
                    f"Found tweet: {tweet_data['timestamp']} - {tweet_data['text']}"
                )
                if len(tweets) >= tweet_limit:
                    break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    return tweets[:tweet_limit]


def write_tweets_to_csv(tweets, filename="roaring_kitty_tweets.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "timestamp", "text"])
        writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet)


# Usage
username = "TheRoaringKitty"
tweet_limit = 25
tweets = get_tweets_selenium(username, tweet_limit)

write_tweets_to_csv(tweets)

for i, tweet in enumerate(tweets, 1):
    print(f"{i}. {tweet['timestamp']} - {tweet['text']}")


import requests
import re
import praw
import logging
import yaml

# Load authentication details from YAML config file
with open("auth.yml", "r") as ymlfile:
    auth = yaml.safe_load(ymlfile)

# Submit GET request on Google and create list of Reddit restaurant threads URLs
city = "Seattle"
search_url = "https://www.google.com/search?q=" + city + "+restaurants+site%3reddit.com"
response = requests.get(search_url)
restaurant_list = [m.group(0) for m in re.finditer("https\:\/\/www\.reddit\.com[^\"\&]+", response.text)]

reddit_instance = praw.Reddit(client_id=auth["client_id"], client_secret=auth["client_secret"], password=auth["password"], user_agent=auth["user_agent"], username=auth["username"])

# Set up logging
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

# Loop through Reddit urls and capture top level Reddit comments
for url in restaurant_list:
    print(url)
    submission = reddit_instance.submission(url=url)
    for top_level_comments in submission.comments:
        print(top_level_comments.body)
        print("")
    break
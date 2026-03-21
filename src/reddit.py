# https://praw.readthedocs.io/en/v7.2.0/getting_started/quick_start.html
# https://www.reddit.com/r/reddit.com/wiki/api/
# https://www.reddit.com/r/learnpython/comments/kuwc3e/comment/giulflo/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://www.reddit.com/dev/api#GET_api_morechildren

'''
Idea: Build script that gets most recent 20 posts from reddit on vegan subreddit.
Decided against reddit API and PRAW because of the whole 

'''

import requests

url = 'https://www.reddit.com/r/learnpython/new/.json'
response = requests.get(url).json()
reddit_posts = response['data']['children']
print(len(reddit_posts))
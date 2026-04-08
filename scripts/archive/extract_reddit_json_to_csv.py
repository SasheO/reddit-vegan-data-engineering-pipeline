# https://praw.readthedocs.io/en/v7.2.0/getting_started/quick_start.html
# https://www.reddit.com/r/reddit.com/wiki/api/
# https://www.reddit.com/r/learnpython/comments/kuwc3e/comment/giulflo/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://www.reddit.com/dev/api#GET_api_morechildren
# https://www.reddit.com/r/redditdev/comments/1hx9zr7/how_does_ratelimit_seconds_work/#:~:text=Reddit%20has%20multiple%20rate%20limits,you're%20trying%20to%20do.
# https://github.com/reddit-archive/reddit/wiki/API#rules

"""
Get all posts per day for a week
Use before and after parameters to get paginated data: https://www.reddit.com/dev/api/#GET_new

rate limit: 10 queries per minute if you are not using OAuth authentication

TODO: set up cloudwatch to run this functionality once per day
TODO: change this to write data into postgresql database in AWS RDS, rename file appropriately
"""

import requests
import time
import os
import json
import re

def extract_src_url(text):
    match = re.search(r'src="([^"]*)"', text)
    if match:
        return match.group(1)
    return ""

subreddit_name = "vegan"
csv_output_file = f"{subreddit_name}_posts.csv"
json_output_file = f"{subreddit_name}_posts.json"
url = f"https://www.reddit.com/r/{subreddit_name}/new/.json"
params = {"limit":100}
count_of_posts_fetched = 0
if not os.path.exists(csv_output_file):
    with open(csv_output_file, "a+", encoding="utf-8", errors="replace") as f:
        f.write("post_id,created_utc,post_title,author_id,author_username,upvote_count,downvote_count,comments_count,crossposts_count,awards_received_count,post_text,post_url,has_media,media_type,media_title,media_src,media_url")
        f.write("\n")

# time.sleep(600)
response = requests.get(url, params=params)

for _ in range(10):
    if response.status_code == 200:
        response_json = response.json()
        with open(json_output_file, "a+", encoding="utf-8", errors="replace")as file:
            json.dump(response_json, file, indent=4)
            file.write("\n")

        pagination_after_key = response_json["data"]["after"] 
        params["after"] = pagination_after_key
        print("pagination_after_key:",pagination_after_key)
        reddit_posts = response_json["data"]["children"]
        print("number of posts fetched:", len(reddit_posts))
        count_of_posts_fetched += len(reddit_posts)
        for post in reddit_posts:
            if "id" not in post["data"]:
                post_id = ""
            else:
                post_id = post["data"]["id"]
            if "author_fullname" not in post["data"]:
                author_id = ""
            else:
                author_id = post["data"]["author_fullname"][3:]

            if "author" not in post["data"]:
                author_username = ""
            else:
                author_username = post["data"]["author"]

            if "ups" not in post["data"]:
                upvote_count = 0
            else:
                upvote_count = post["data"]["ups"]

            if "downs" not in post["data"]:
                downvote_count = 0
            else:
                downvote_count = post["data"]["downs"]

            if "total_awards_received" not in post["data"]:
                awards_received_count = 0
            else:
                awards_received_count = post["data"]["total_awards_received"]

            if "selftext" not in post["data"]:
                post_text = ""
            else:
                post_text = post["data"]["selftext"].replace(",", ";").replace("\n", "\t") 

            if "title" not in post["data"]:
                post_title = ""
            else:
                post_title = post["data"]["title"].replace(",", ";").replace("\n", "\t")

            if "num_comments" not in post["data"]:
                comments_count = 0
            else:
                comments_count = post["data"]["num_comments"]

            if "created_utc" not in post["data"]:
                created_utc = 0
            else:
                created_utc = post["data"]["created_utc"]

            if "url" not in post["data"]:
                url_to_post = ""
            else:
                url_to_post = post["data"]["url"]

            if "num_crossposts" not in post["data"]:
                crossposts_count = ""
            else:
                crossposts_count = post["data"]["num_crossposts"]
                 
            if "media" not in post["data"]:
                media_json = None 
            else:
                media_json = post["data"]["media"]

            if media_json:
                has_media = True
            else:
                has_media = False
            try:
                media_src = media_json["type"].replace(",", ";").replace("\n", "\t")
            except:
                media_src = ""
            try:
                media_url = extract_src_url(media_json["html"]) 
            except:
                media_url = ""
            try:
                media_type = media_json["oembed"]["type"].replace(",", ";").replace("\n", "\t")
            except:
                media_type = ""
            try:
                media_title = media_json["oembed"]["title"].replace(",", ";").replace("\n", "\t")
            except:
                media_title = ""
            
            
            # write data to csv file
            # try:
            with open(csv_output_file, "a+", encoding="utf-8", errors="replace") as f:
                f.write(post_id+"," +
                str(created_utc)+","
                +post_title+","
                +str(author_id)+","
                +author_username+","
                +str(upvote_count)+","
                +str(downvote_count)+","
                +str(comments_count)+","
                +str(crossposts_count)+","
                +str(awards_received_count)+","
                +post_text+","
                +url_to_post+","
                +str(has_media)+","
                +media_type+","
                +media_title+","
                +media_src+","
                +media_url
                )
                f.write("\n")


        time.sleep(130) # rate limit: 1000 items per 600 seconds, so 100 items per minute  (source: https://www.reddit.com/r/redditdev/comments/1hx9zr7/how_does_ratelimit_seconds_work/#:~:text=Reddit%20has%20multiple%20rate%20limits,you're%20trying%20to%20do.)
        response = requests.get(url, params=params)


    else:
        print(response.status_code, response.text)
        headers = dict(response.headers)
        print(headers)
        print(int(headers['x-ratelimit-reset']))
        time.sleep(int(headers['x-ratelimit-reset'])+1)
        response = requests.get(url, params=params)

print("total number of posts fetched:", count_of_posts_fetched)
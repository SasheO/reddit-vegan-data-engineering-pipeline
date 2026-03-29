# current issue: Getting 403 http response on lambda
# troubleshoot: https://repost.aws/knowledge-center/api-gateway-403-error-lambda-authorizer
# look into cloudwatch logs: https://stackoverflow.com/questions/33109122/aws-lambda-function-rest-api-end-point-403-error

import os
import pymysql 
import requests
import time
import json
import re
from datetime import datetime
from get_secrets import *

# get database credentials from AWS secrets: https://docs.aws.amazon.com/lambda/latest/dg/with-secrets-manager.html 
secret_name = "redditVeganDatabase2MySQLSecrets"
region_name = "us-east-1"
secrets = get_db_secrets(secret_name,region_name)
json_acceptable_string = secrets.replace("'", "\"")
secrets = json.loads(json_acceptable_string)

database = secrets['dbname']
user = secrets['username']
password= secrets['password']
table_name = os.getenv("TABLE_NAME")
host = secrets['host']

db_connection = pymysql.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

def extract_src_url(text):
    match = re.search(r'src="([^"]*)"', text)
    if match:
        return match.group(1)
    return None

def lambda_handler(event, context):
    subreddit_name = "vegan"
    url = f"https://www.reddit.com/r/{subreddit_name}/new/.json"
    print(os.getenv("MY_REDDIT_USERNAME")) # CHANGED
    # params = {"limit":100} # CHANGED
    params = {"limit":100, "User-Agent": f"MyRedditApp/1.0 (by u/{os.getenv("MY_REDDIT_USERNAME")})"} # CHANGED
    count_of_posts_fetched = 0
    count_of_success_response = 0

    response = requests.get(url, params=params)

    # while True:
    for _ in range(10): # it seems like there are usually less than 100 posts per day, so this can be hard limited to ten requests. at least one will go through. this will likely not miss too many posts.
        if response.status_code == 200:
            count_of_success_response += 1
            
            cursor = db_connection.cursor()

            # parse the json response and extract useful data
            print("response.text:", response.text)
            response_json = response.json()
            with open("output.json", "a+", encoding='utf-8') as f: # CHANGED
                json.dumps(response_json, f)
                f.write("\n")

            pagination_after_key = response_json["data"]["after"] 
            params["after"] = pagination_after_key
            print("pagination_after_key:",pagination_after_key)
            reddit_posts = response_json["data"]["children"]
            print("number of posts fetched:", len(reddit_posts))
            count_of_posts_fetched += len(reddit_posts)
            insert_values = []

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
                    post_text = None
                else:
                    post_text = post["data"]["selftext"].replace(",", ";").replace("'", "").replace('"', "").replace("\n", "\t") 
                if "title" not in post["data"]:
                    post_title = ""
                else:
                    post_title = post["data"]["title"].replace(",", ";").replace("'", "").replace('"', "").replace("\n", "\t")
                if "num_comments" not in post["data"]:
                    comments_count = 0
                else:
                    comments_count = post["data"]["num_comments"]
                if "created_utc" not in post["data"]:
                    created_utc = 0
                else:
                    created_utc = post["data"]["created_utc"]
                if "url" not in post["data"]:
                    url_to_post = None
                else:
                    url_to_post = post["data"]["url"]
                if "num_crossposts" not in post["data"]:
                    crossposts_count = 0
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
                    media_src = media_json["type"].replace(",", ";").replace("'", "").replace('"', "").replace("\n", "\t")
                except:
                    media_src = None
                try:
                    media_url = extract_src_url(media_json["oembed"]["html"]) 
                except:
                    media_url = None
                try:
                    media_type = media_json["oembed"]["type"].replace(",", ";").replace("'", "").replace('"', "").replace("\n", "\t")
                except:
                    media_type = None
                try:
                    media_title = media_json["oembed"]["title"].replace(",", ";").replace("'", "").replace('"', "").replace("\n", "\t")
                except:
                    media_title = None
                

                if has_media:
                    insert_value = (post_id, datetime.fromtimestamp(int(created_utc)), post_title[:130], author_id[:130], author_username[:30], upvote_count, downvote_count, comments_count, crossposts_count, awards_received_count, post_text[:1000], url_to_post[:130], has_media, media_type[:20], media_title[:130], media_src[:130], media_url[:130])
                else:
                    insert_value = (post_id, datetime.fromtimestamp(int(created_utc)), post_title[:130], author_id[:130], author_username[:30], upvote_count, downvote_count, comments_count, crossposts_count, awards_received_count, post_text[:1000], url_to_post[:130], has_media, media_type, media_title, media_src, media_url)
                insert_values.append(insert_value)
            
            cursor.executemany(f"INSERT IGNORE INTO {table_name} (post_id, created_utc, post_title, author_id, author_username, upvote_count, downvote_count, comments_count, crossposts_count, awards_received_count, post_text, post_url, has_media, media_type, media_title, media_src, media_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", insert_values)
            db_connection.commit()
            cursor.close()
            
            time.sleep(5) # rate limits
            response = requests.get(url, params=params)
        elif response.status_code == 429:
            # TODO: convert this to writing errors to log rather than print statements
            headers = dict(response.headers)
            print("x-ratelimit-reset:", headers['x-ratelimit-reset'])
            time.sleep(int(headers['x-ratelimit-reset'])+5)
            response = requests.get(url, params=params)
        else:
            headers = dict(response.headers)
            print(response.status_code, response.text)
            print(headers)
            time.sleep(10)
            
    # TODO: make this write logs to a table rather than printing
    print("total number of posts fetched:", count_of_posts_fetched) 

# db_connection.close() # TODO: figure out if i should close this or not?
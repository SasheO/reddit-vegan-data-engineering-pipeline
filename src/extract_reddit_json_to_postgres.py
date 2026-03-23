# https://www.youtube.com/watch?v=vyLvmPkQZkI

from dotenv import load_dotenv
import os
import psycopg2 
import requests
import time
import re

# get environment variables
load_dotenv()
database = os.getenv("DATABASE")
user = os.getenv("USER")
password= os.getenv("PASSWORD")
table_name = os.getenv("TABLE_NAME")

# Connect to PostgreSQL

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database=database,
        user=user,
        password=password
    )

def extract_src_url(text):
    match = re.search(r'src="([^"]*)"', text)
    if match:
        return match.group(1)
    return ""

def handler():
    subreddit_name = "vegan"
    url = f"https://www.reddit.com/r/{subreddit_name}/new/.json"
    params = {"limit":100}
    count_of_posts_fetched = 0
    count_of_success_response = 0

    response = requests.get(url, params=params)

    # while True:
    for _ in range(10): # it seems like there are usually less than 100 posts per day, so this can be hard limited to ten requests. at least one will go through. this will likely not miss too many posts.
        if response.status_code == 200:
            count_of_success_response += 1

            # open up connection to database and start preamble for sql query
            conn = get_db_connection()
            cursor = conn.cursor()
            sql_query_to_insert_table_values = f"insert into {table_name} (post_id, created_utc, post_title, author_id, author_username, upvote_count, downvote_count, comments_count, crossposts_count, awards_received_count, post_text, post_url, has_media, media_type, media_title, media_src, media_url)  values "

            # parse the json response and extract useful data
            response_json = response.json()
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
                    media_url = extract_src_url(media_json["html"]) 
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
                    has_media = 1
                else:
                    has_media = 0
                
                # 
                # TODO: ensure that null values (e.g. null media urls and other like fields) are not entered as 'null' strings
                insert_value = f"('{post_id}', to_timestamp({int(created_utc)}), '{post_title}'::varchar(130), '{author_id}'::varchar(20), '{author_username}'::varchar(30), {upvote_count}, {downvote_count}, {comments_count}, {crossposts_count}, {awards_received_count}, '{post_text}'::varchar(1000), '{url_to_post}'::varchar(130), {has_media}::bit, '{media_type}'::varchar(20), '{media_title}'::varchar(130), '{media_src}'::varchar(130), '{media_url}'::varchar(130)), " # ON CONFLICT (post_id) DO NOTHING;"
                insert_value = insert_value.replace("None", "null")
                sql_query_to_insert_table_values += insert_value
                # print(post_id)
            
            # run sql query, close connection to database
            sql_query_to_insert_table_values = sql_query_to_insert_table_values[:-2] + " ON CONFLICT (post_id) DO NOTHING;" # in case there are duplicate rows with primary key (post_id)
            cursor.execute(sql_query_to_insert_table_values)
            conn.commit()
            cursor.close()
            conn.close()

            if count_of_success_response >= 10: # because at most ten pages can be returned from reddit non-oauth api
                break
            else: # do it again!
                time.sleep(5) # rate limits
                response = requests.get(url, params=params)
        else:
            # TODO: convert this to writing errors to log rather than print statements
            headers = dict(response.headers)
            print(response.status_code, response.text)
            print("x-ratelimit-reset:", headers['x-ratelimit-reset'])
            time.sleep(int(headers['x-ratelimit-reset'])+5)
            response = requests.get(url, params=params)
            
    # TODO: make this write logs to a table rather than printing
    print("total number of posts fetched:", count_of_posts_fetched) 
    

handler()
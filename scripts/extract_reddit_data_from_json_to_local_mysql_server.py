from dotenv import load_dotenv
import os
import pymysql
import json
import re
from datetime import datetime

def extract_src_url(text):
    match = re.search(r'src="([^"]*)"', text)
    if match:
        return match.group(1)
    return None

def extract_reddit_data(post):
    """
    extract_reddit_data extracts relevant data from a reddit post into a tuple which it returns.

    parameters:
        post: (dict) the reddit API json response representing a single post on a subreddit
    
    returns: 
        post_data: (tup) a tuple with the following data in the following order: (post id, utc time post was created, post title, author id, author username, upvote count, downvote count, comments count, crossposts count, awards received count, post text, post url, boolean has_media, media type, media title, media src, media url)
    """
    
    if "id" not in post["data"]:
        post_id = None
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
    
    # TODO: modify all truncations [:130] or [:1000] or whatever to reflect what is accurate to the sql code
    if has_media:
        post_data = (post_id, datetime.fromtimestamp(int(created_utc)), post_title[:130], author_id[:130], author_username[:30], upvote_count, downvote_count, comments_count, crossposts_count, awards_received_count, post_text[:1000], url_to_post[:130], has_media, media_type[:20], media_title[:130], media_src[:130], media_url[:130])
    else:
        post_data = (post_id, datetime.fromtimestamp(int(created_utc)), post_title[:130], author_id[:130], author_username[:30], upvote_count, downvote_count, comments_count, crossposts_count, awards_received_count, post_text[:1000], url_to_post[:130], has_media, media_type, media_title, media_src, media_url)
    return post_data


INPUT_FILE = '../data/output1.json'

load_dotenv()
database = os.getenv("DATABASE")
user = os.getenv("USER")
password= os.getenv("PASSWORD")
table_name = os.getenv("TABLE_NAME")
host = os.getenv("ENDPOINT")

db_connection = pymysql.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

count_of_successful_writes_to_mysql_server = 0

with open(INPUT_FILE, "r", encoding='utf-8') as f:
    reddit_data_listings = f.readlines()

print("Number of listings:", len(reddit_data_listings))

for listing in reddit_data_listings:
    cursor = db_connection.cursor()
    response_json = json.loads(listing)
    reddit_posts = response_json["data"]["children"]

    # insert the posts into the mysql server
    post_data_values_list_for_sql_command = []
    for post in reddit_posts:
        post_data = extract_reddit_data(post)
        post_data_values_list_for_sql_command.append(post_data)
    cursor.executemany(f"INSERT IGNORE INTO {table_name} (post_id, created_utc, post_title, author_id, author_username, upvote_count, downvote_count, comments_count, crossposts_count, awards_received_count, post_text, post_url, has_media, media_type, media_title, media_src, media_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", post_data_values_list_for_sql_command)
    db_connection.commit()
    cursor.close()

    count_of_successful_writes_to_mysql_server += 1

db_connection.close()
print("Successful writes to mysql server:", count_of_successful_writes_to_mysql_server)
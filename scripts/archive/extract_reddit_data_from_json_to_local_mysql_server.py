from dotenv import load_dotenv
import os
import pymysql
import json
from extract_reddit_data_helpers import *

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
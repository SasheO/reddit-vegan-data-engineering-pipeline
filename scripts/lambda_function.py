# TODO: modify this to be triggered by uploading data to S3 bucket, modify this to ingest json from s3 bucket and update rds database
# TODO: put a requirements.txt file in the main directory with needed libraries, document setup requirements
# TODO: add an image of the data pipeline (from staging with raw json files to amazon s3 to lambda to sql to data analsis) in the readme
# TODO: add multiline string at the top of this script which describes what it does

import os
import pymysql 
import requests
import time
import json
import re
from datetime import datetime
from get_secrets import *
import boto3

s3 = boto3.client('s3')

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

# open this outside the handler function because opening db connections is resource heavy and i don't want this done every time the lambda function is triggered
# don't need to close this connection explicitly because Lambda automatically cleans up when container shuts down
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

def lambda_handler(event, context):
    # TODO: open file and read all lines. each line is a separate json object with multiple posts in json_object["data"]["children"]
    # TODO: for each post, extract the data using extract_reddit_data 
    # TODO: for each post, save the data to mysql
    # TODO: add multiline comment that explains what this does
    # extract data from bucket
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        # TODO: insert code for what you want to do here
        
        return json_data

    except Exception as e:
        print(f"Error getting object {key} from bucket {bucket}: {e}")
        raise e

    return
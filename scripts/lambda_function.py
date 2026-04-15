"""
This is the AWS lambda function
"""
# TODO: put a requirements.txt file in the main directory with needed libraries, document setup requirements
# TODO: add an image of the data pipeline (from staging with raw json files to amazon s3 to lambda to sql to data analsis) in the readme

import os
import pymysql 
import requests
import time
import json
from get_secrets import *
from extract_reddit_data_helpers import *
import urllib.parse
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

def lambda_handler(event, context):
    """
    lambda_handler is an AWS lambda function which is triggered when files are created in an s3 bucket. It fetches the file and writes the content of that file to a connected mysql server in AWS RDS.

    parameters:
        event: (dict) the data passed to the function when it is triggered
        context: (object) information about the invocation, function configuration, and execution environment
    
    returns: 
        None
    """
    # extract data from bucket
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    count_of_successful_writes_to_mysql_server = 0
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        
        for listing in response['Body'].iter_lines():
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
        
        print("Successful writes to mysql server:", count_of_successful_writes_to_mysql_server)

    except Exception as e:
        print(f"Error getting object {key} from bucket {bucket}: {e}")
        raise e

    return
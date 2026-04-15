# TODO: modify this to be triggered by uploading data to S3 bucket, modify this to ingest json from s3 bucket and update rds database
# TODO: put a requirements.txt file in the main directory with needed libraries, document setup requirements
# TODO: add an image of the data pipeline (from staging with raw json files to amazon s3 to lambda to sql to data analsis) in the readme
# TODO: add multiline string at the top of this script which describes what it does

import os
import pymysql 
import requests
import time
import json
from get_secrets import *
from extract_reddit_data_helpers import *
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
"""
This queries reddit's .json API and dumps the raw data into json files in the /../data/ folder.

Usage:
    Run `python extract_reddit_data_to_json.py` if you want to get the most recent data.
    Run `python extract_reddit_data_to_json.py {pagination_kay}` if you want to get paginated data earlier than the given pagination key.
"""

from dotenv import load_dotenv
import os
import requests
import time
import json
import sys

def extract_reddit_data_to_json(output_file, reddit_username, pagination_token=None):
    '''
    extract_reddit_data_to_json queries reddit's .json API and dumps the raw data into json files.

    parameters:
        output_file (str): the .json file to which the output data will be written
        reddit_username (str): the reddit username which will be used to identify this request within a custom User-Agent string) for non-authenticated API calls
        pagination_token (str): optional - the pagination token which data before will be queried.

    returns:
        None
    '''

    subreddit_name = "vegan"
    url = f"https://www.reddit.com/r/{subreddit_name}/new/.json"
    params = {"limit":100, "User-Agent": f"MyRedditApp/1.0 (by u/{reddit_username})"} 
    if pagination_token:
        params["after"] = pagination_token
    count_of_posts_fetched = 0

    response = requests.get(url, params=params)

    for _ in range(10): # it seems like there are usually less than 100 posts per day, so this can be hard limited to ten requests. at least one will go through. this will likely not miss too many posts.
        if response.status_code == 200:   
            print(response.status_code, "Success")
            response_json = response.json()
            with open(output_file, "a+", encoding='utf-8') as f: 
                json.dump(response_json, f)
                f.write("\n")
            pagination_token = response_json["data"]["after"] 
            params["after"] = pagination_token
            print("pagination_token:",pagination_token)
            reddit_posts = response_json["data"]["children"]
            print("number of posts fetched:", len(reddit_posts))
            count_of_posts_fetched += len(reddit_posts)
            
            time.sleep(5) # rate limits
            response = requests.get(url, params=params)
        elif response.status_code == 429:
            headers = dict(response.headers)
            print(response.status_code, "x-ratelimit-reset:", headers['x-ratelimit-reset'])
            time.sleep(int(headers['x-ratelimit-reset'])+5)
            response = requests.get(url, params=params)
        else:
            headers = dict(response.headers)
            print(response.status_code, response.text)
            print(headers)
            time.sleep(10)
            
    print("total number of posts fetched:", count_of_posts_fetched) 

if __name__=="__main__": 
    load_dotenv()
    reddit_username = os.getenv("MY_REDDIT_USERNAME")
    file_num = 1
    json_output_file = f"../data/output{file_num}.json"
    while True:
        if os.path.isfile(json_output_file):
            file_num += 1
            json_output_file = f"../data/output{file_num}.json"
        else:
            break  

    if len(sys.argv)>1: # if a pagination token is passed in as an argument
        pagination_token = sys.argv[1]
        print(pagination_token)
        extract_reddit_data_to_json(json_output_file, reddit_username, pagination_token)
    else:
        extract_reddit_data_to_json(json_output_file, reddit_username)
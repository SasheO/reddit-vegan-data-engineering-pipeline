# https://praw.readthedocs.io/en/v7.2.0/getting_started/quick_start.html
# https://www.reddit.com/r/reddit.com/wiki/api/
# https://www.reddit.com/r/learnpython/comments/kuwc3e/comment/giulflo/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://www.reddit.com/dev/api#GET_api_morechildren
# https://www.reddit.com/r/redditdev/comments/1hx9zr7/how_does_ratelimit_seconds_work/#:~:text=Reddit%20has%20multiple%20rate%20limits,you're%20trying%20to%20do.

'''
Get all posts per day for a week
Use before and after parameters to get paginated data: https://www.reddit.com/dev/api/#GET_new

rate limit: 10 queries per minute if you are not using OAuth authentication
'''

import requests
import time
import os

def extract_src_url(text):
    match = re.search(r'src="([^"]*)"', text)
    if match:
        return match.group(1)
    return ""

subreddit_name = "vegan"
csv_output_file = f"{subreddit_name}_posts.csv"
url = f'https://www.reddit.com/r/{subreddit_name}/new/.json'
params = {'limit':100}
count_of_posts_fetched = 0
if not os.path.exists(csv_output_file):
    with open(csv_output_file, "a+") as f:
        f.write("post_id,created_utc,post_title,author_id,author_username,upvote_count,downvote_count,comments_count,crossposts_count,awards_received_count,post_text,post_url,has_media,media_type,media_title,media_src,media_url") # TODO: write all the column names separated by commas
        f.write("\n")

response = requests.get(url, params=params)

while True:
    if response.status_code == 200:
        response_json = response.json()
        pagination_after_key = response_json['data']['after'] 
        params['after'] = pagination_after_key
        print(pagination_after_key)
        reddit_posts = response_json['data']['children']
        print("number of posts fetched:", len(reddit_posts))
        print()
        count_of_posts_fetched += len(reddit_posts)
        for post in reddit_posts:
            post_id = post['data']['id']
            author_id = post['data']['author_fullname'][3:]
            author_username = post['data']['author']
            upvote_count = post['data']['ups']
            downvote_count = post['data']['downs']
            awards_received_count = post['data']["total_awards_received"]
            # TODO: if saving values to csv file, ensure commas in text field are appropriately handled
            post_text = post['data']["selftext"].replace(",", ";") # replace commas to avoid errors in csv file
            post_title = post['data']["title"]
            comments_count = post['data']["num_comments"]
            created_utc = post['data']["created_utc"]
            media_json = post['data']["media"] # can be null value
            if media_json:
                has_media = True
                media_src = media_json["type"]
                media_url = extract_src_url(media_json["html"]) # TODO: ensure if this returns the right value
                media_type = media_json["oembed"]["type"]
                media_title = media_json["oembed"]["title"]
            else:
                has_media = False
                media_src = ""
                media_url = ""
                media_type = ""
                media_title = ""
            url_to_post = post['data']['url']
            crossposts_count = post['data']["num_crossposts"]
            
            # write data to csv file
            with open(csv_output_file, "a+") as f:
                f.write(str(post_id)+","
                +str(created_utc)+","
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

        if len(reddit_posts) < params['limit'] or count_of_posts_fetched >= 1000: # to exit while loop on the last page of data: if < 100 posts are returned or the max 1000 pages per listings has already been returned (source for maximum listing number: https://www.reddit.com/r/redditdev/comments/2uymft/comment/coe7xds/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)
            break

        time.sleep(70) # rate limit: 1000 items per 600 seconds, so 100 items per minute  (source: https://www.reddit.com/r/redditdev/comments/1hx9zr7/how_does_ratelimit_seconds_work/#:~:text=Reddit%20has%20multiple%20rate%20limits,you're%20trying%20to%20do.)

        response = requests.get(url, params=params)

        break # TODO: remove this. this is only for testing first 100 posts
    else:
        print(response.status_code)
        break
    
    
print("total number of posts fetched:", count_of_posts_fetched)
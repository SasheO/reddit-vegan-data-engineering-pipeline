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

# Reddit Vegan Data Engineering and Analysis Pipeline

This is a personal project that:
1. Extracts, transforms, and loads data from Reddit 'vegan' subreddit into a MySQL database using AWS S3 bucket, AWS Lambda Python function, and AWS RDS database. 
2. Analyses the data to get descriptive insights on the data, such as when subreddit users are more likely to post.

## Data Pipeline

## Tools and Services Used
Python scripts
* scripts/extract_reddit_data_to_json.py: Locally run scripts used for extraction from [Reddit JSON API](https://www.reddit.com/dev/api/) (unauthenticated)

AWS 
* AWS S3: Used to store raw data after extraction
* AWS Lambda: Used for transformation and loading into RDS MySQL database
* AWS RDS (MySQL): Ingests transformed data

Power BI
* Connects to RDS and provides visuals including:
   * Average number of comments
   * Average number of upvotes
   * Top posts in terms of upvotes
   * Number of posts to subreddit per dat

## Power BI Dashboard
[View PDF here](powerbi/posts_dashboard.pdf)

## Directory Structure
```
|- data/
   |- *.json
   |- README.md     
|- notebooks/
   |- analysis.txt
   |- exploratory_analysis.ipynb   
|- powerbi/
   |- Dashboard.pdf
|- scripts/
   |- extract_reddit_data_helpers.py
   |- extract_reddit_data_to_json.py
   |- get_secrets.py
   |- lambda_function.py
   |- archive/
      |- extract_reddit_data_from_json_to_local_mysql_server.py
      |- extract_reddit_data_from_json_to_local_postgresql_server.py
      |- extract_reddit_json_to_csv.py
      |- extract_reddit_json_to_postgres.py
      |- test_extract_src_url.py  
|- sql/
      |- create_table_mysql.sql
      |- get_average_number_of_posts_per_day.sql
      |- get_average_number_of_posts_per_day_of_the_week.sql
      |- get_number_of_posts_per_day.sql
      |- get_number_of_posts_per_day_of_the_week.sql
      |- get_number_of_posts_with_given_range_of_upvotes.sql
      |- get_top_20_upvoted_posts.sql
|- README.md
```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@SasheO](https://www.github.com/SasheO)


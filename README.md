# Reddit Vegan Data Engineering and Analysis Pipeline

This is a personal project that:
1. Extracts, transforms, and loads data from Reddit into a MySQL database using AWS S3 bucket, AWS CloudWatch triggers, AWS Lambda Python function, and AWS RDS database. 
2. Analyses the data to get descriptive insights on the data, such as when subreddit users are more likely to post.

## Directory Structure
```
|- data/
|- scripts/
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
   |- create_table_postgresql.sql
|- README.md 
|- reference_links.txt
|- requirements.txt
```

## Requirements
* Python >=3.10
* Python libraries found in requirements.txt

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@SasheO](https://www.github.com/SasheO)


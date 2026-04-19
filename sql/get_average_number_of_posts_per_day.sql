with t1 as 
    (select date(created_utc) as date_ from POSTS),
t2 as
	(select date_, count(*) as post_count from t1
	group by date_)
select avg(post_count) as average_daily_post_count
from t2;
with t1 as 
    (select date(created_utc) as date_, dayname(created_utc) as day_of_the_week from POSTS),
t2 as
	(select day_of_the_week, date_, count(*) as post_count from t1
	group by date_)
select day_of_the_week, avg(post_count) as average_post_count
from t2
group by day_of_the_week
;
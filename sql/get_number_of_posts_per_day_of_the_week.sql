with t1 as 
    (select date(created_utc) as date_, dayname(created_utc) as day_of_the_week from POSTS)
select day_of_the_week, date_, count(*) from t1
group by date_;
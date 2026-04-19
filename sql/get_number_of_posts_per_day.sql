with t1 as 
    (select date(created_utc) as date_ from POSTS)
select date_, count(*) from t1
group by date_;